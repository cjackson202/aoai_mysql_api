'''
To run this api, use: uvicorn norag_mysql_api:app --reload
'''

from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
import mysql.connector  
import os  
from dotenv import load_dotenv  
import re  
import tiktoken

load_dotenv()

app = FastAPI()

class RequestData(BaseModel):  
    system_prompt: str  
    user_prompt: str  
    response: str 
    deployment_model: str 
    name_model: str  
    version_model: str  
    region: str  
    project: str  

def aoai_metadata(system_prompt, user_prompt, response, name_model, version_model, region):
    def token_amount(text, name_model):
        if name_model == 'gpt-4o' or "gpt-4o-" or 'gpt-4o-mini':
            encoding = tiktoken.get_encoding('o200k_base')
            return len(encoding.encode(text))
        else:
            encoding = tiktoken.get_encoding('cl100k_base')
            return len(encoding.encode(text))
    prompt_token_count = token_amount(text=system_prompt, name_model=name_model) + token_amount(text=user_prompt, name_model=name_model) + token_amount(response, name_model=name_model) 
    response_token_count = token_amount(text=response, name_model=name_model)
    if region == 'East US 2':
        # Pricing gpt4o - 2024-05-13 
        if name_model == 'gpt-4o' and version_model == '2024-05-13':
            prompt_cost = round((prompt_token_count / 1000) * .005, 5) 
            completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .015, 5)
        # Pricing gpt-4o-mini - 2024-07-18
        elif name_model == 'gpt-4o-mini' and version_model == '2024-07-18':
            prompt_cost = round((prompt_token_count / 1000) * .000165, 5) 
            completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .00066, 5)
        # Pricing gpt4o - 2024-08-06
        elif name_model == 'gpt-4o' or "gpt-4o-" and version_model == '2024-08-06':
            prompt_cost = round((prompt_token_count / 1000) * .00275, 5) 
            completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .011, 5)
        else:  
            raise HTTPException(status_code=400, detail="Invalid model or version.")  
        return prompt_token_count, prompt_cost, response_token_count, completion_cost
    else:
        raise HTTPException(status_code=400, detail="East US 2 region only available.")  

def sql_connect(system_prompt, user_prompt, prompt_cost, response, completion_cost, deployment_model, prompt_token_count, response_token_count, project):
    try:
        # Establish a connection to the MySQL server  
        mydb = mysql.connector.connect(  
        host=os.getenv("azure_mysql_host"),  
        user=os.getenv("azure_mysql_user"),  
        password=os.getenv("azure_mysql_password"),  
        database=os.getenv("azure_mysql_schema")  
        )  
        
        # Define a cursor object  
        mycursor = mydb.cursor()  

        # Check if system_prompt already exists in the aoaisystm table  
        mycursor.execute("SELECT system_id FROM aoaisystem WHERE system_prompt = %s", (system_prompt,))  
        result = mycursor.fetchone()  
    
        # If the system_prompt exists, use the corresponding system_id, otherwise create a new one  
        if result:  
            system_id = result[0]  
        else:  
            print("Warning: System_id not found for this prompt. Creating new id and adding prompt!")
            mycursor.execute("SELECT MAX(prompt_number) FROM aoaisystem")  
            result = mycursor.fetchone()  
            prompt_number = result[0] if result[0] else 0  
            # Increment the latest prompt_number by 1  
            prompt_number = prompt_number + 1  
            # Insert a new system_prompt into the aoaisystm table and get the new system_id  
            sql = "INSERT INTO aoaisystem (system_prompt, system_proj, prompt_number) VALUES (%s, %s, %s)"
            val =  (system_prompt, project, prompt_number)
            mycursor.execute(sql, val)
            system_id = mycursor.lastrowid 
        # Insert into prompt table with connection to system prompt
        sql = "INSERT INTO prompt (system_id, user_prompt, tokens, price) VALUES (%s, %s, %s, %s)"  
        val = (system_id, user_prompt, prompt_token_count, prompt_cost)  
        mycursor.execute(sql, val)  
        # Get the ID of the last inserted row  
        prompt_id = mycursor.lastrowid  
        
        mycursor.execute("SELECT model_id FROM models WHERE model = %s", (deployment_model,))  
        result = mycursor.fetchone()  
    
        # If the model exists, use the corresponding model_id, otherwise create a new one  
        if result:  
            model_id = result[0]  
        else:  
            print("Warning: Model_id not found for this model. Creating new id and adding model!")
            mycursor.execute("SELECT MAX(model_id) FROM models")  
            result = mycursor.fetchone()  
            model_id = result[0] if result[0] else 0  
            # Increment the latest model_id by 1  
            model_id = model_id + 1 

            # Define regex patterns for models
            ada_pattern = re.compile(r'(?i)ada')  # Case insensitive match for 'ada' anywhere in the string  
            gpt4o_pattern = re.compile(r'(?i)gpt-?4o')  # Case insensitive match for 'gpt-4o' or 'gpt4o' anywhere in the string


            if ada_pattern.search(deployment_model):
                # Insert a new system_prompt into the aoaisystm table and get the new system_id  
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"
                val =  (deployment_model, None, 0.000100, 'cl100k_base')
                mycursor.execute(sql, val)
                model_id = mycursor.lastrowid 
            elif  gpt4o_pattern.search(deployment_model): 
                # Insert a new system_prompt into the aoaisystm table and get the new system_id  
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"
                val =  (deployment_model, .005000, 0.015000, 'o200k_base')
                mycursor.execute(sql, val)
                model_id = mycursor.lastrowid 
            else:
                # Insert a new system_prompt into the aoaisystm table and get the new system_id  
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"
                val =  (deployment_model, None, None, None)
                mycursor.execute(sql, val)
                model_id = mycursor.lastrowid 
        
        # Insert into chat_completions table based on model used 
        sql = "INSERT INTO chat_completions (model_id, prompt_id, chat_completion, tokens, price) VALUES (%s, %s, %s, %s, %s)"  
        val = (model_id, prompt_id, response, response_token_count, completion_cost)  
        mycursor.execute(sql, val)  
        
        # Save the changes  
        mydb.commit()  
        return {"message": f"{mycursor.rowcount} record(s) inserted into aoai database."} 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to access MySQL DB with error: {e}")

@app.post("/process")  
def process_data(data: RequestData):  
    prompt_token_count, prompt_cost, response_token_count, completion_cost = aoai_metadata(  
        system_prompt=data.system_prompt,  
        user_prompt=data.user_prompt,  
        response=data.response,  
        name_model=data.name_model,  
        version_model=data.version_model,  
        region=data.region  
    )  
    result = sql_connect(  
        system_prompt=data.system_prompt,  
        user_prompt=data.user_prompt,  
        prompt_cost=prompt_cost,  
        response=data.response,  
        completion_cost=completion_cost,  
        deployment_model=data.deployment_model,  
        prompt_token_count=prompt_token_count,  
        response_token_count=response_token_count,  
        project=data.project  
    )  
    return result  