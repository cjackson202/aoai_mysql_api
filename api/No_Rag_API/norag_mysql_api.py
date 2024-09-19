'''
Only compatibale with the following Azure OpenAI components: 

- Models: gpt-4o (2024-05-13 and 2024-08-06), gpt-4o-mini (2024-07-18)
- Regions: East US 2

UPDATES:
    -   Modified timestamp in MySQL for the user prompt time asked. This update
        allows you to see the time difference between asking prompt and receiving answer. 
        'prompt' table, column 'timestamp' updated as varchar type, accepting the datetime as a string in UTC format. 
         For example on implementing this change, please see 'call_norag_api.py' (must rerun sql script v2 to create schema with updates).

    -   Added 'python_api' to mysql schema. This table captures the api used to insert the data to mysql (eventually will have rag and norag api's).
        Insert statement for this table added, accepting the api url as string to go into the table column 'api_name'.
        For example on implementing this change, please see 'call_norag_api.py' (must rerun sql script v2 to create schema with updates).


To run this api use: uvicorn norag_mysql_api:app --reload

Last update: 9/18/2024
'''


from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel, Field 
import mysql.connector  
import os  
from dotenv import load_dotenv  
import re  
import tiktoken  
  
load_dotenv()  
app = FastAPI()  
  
class RequestData(BaseModel):  
    system_prompt: str  = Field(default="")  
    user_prompt: str  = Field(default="")  
    time_asked: str  = Field(default="")  
    response: str  = Field(default="")  
    deployment_model: str = Field(default="")  
    name_model: str = Field(default="")  
    version_model: str = Field(default="")    
    region: str = Field(default="")    
    project: str = Field(default="")    
    api_name: str = Field(default="")   
    retrieve: bool = Field(default=False)
  
def aoai_metadata(system_prompt, user_prompt, response, name_model, version_model, region, retrieve):  
    def token_amount(text, name_model):  
        if name_model in ['gpt-4o', 'gpt-4o-', 'gpt-4o-mini']:  
            encoding = tiktoken.get_encoding('o200k_base')  
            return len(encoding.encode(text)) 
        elif name_model in ['text-embedding-ada-002']:
            encoding = tiktoken.get_encoding('cl100k_base')
            return len(encoding.encode(text)) 
        return 0   
    if retrieve == False:
        prompt_token_count = token_amount(text=system_prompt, name_model=name_model) + token_amount(text=user_prompt, name_model=name_model)  
        response_token_count = token_amount(text=response, name_model=name_model) 
        if region == 'East US 2':  
            # Pricing gpt-4o - 2024-05-13  
            if name_model == 'gpt-4o' and version_model == '2024-05-13':  
                prompt_cost = round((prompt_token_count / 1000) * .005, 5)  
                completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .015, 5)  
            # Pricing gpt-4o-mini - 2024-07-18  
            elif name_model == 'gpt-4o-mini' and version_model == '2024-07-18':  
                prompt_cost = round((prompt_token_count / 1000) * .000165, 5)  
                completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .00066, 5)  
            # Pricing gpt-4o - 2024-08-06  
            elif name_model == 'gpt-4o' and version_model == '2024-08-06':  
                prompt_cost = round((prompt_token_count / 1000) * .00275, 5)  
                completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .011, 5) 
            elif name_model == 'text-embedding-ada-002' and version_model == '2':
                prompt_cost = round((prompt_token_count / 1000) * .0001, 5)
                completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .0001, 5) 
            else:  
                raise HTTPException(status_code=400, detail="Invalid model or version.")  
            return prompt_token_count, prompt_cost, response_token_count, completion_cost  
        else:  
            raise HTTPException(status_code=400, detail="East US 2 region only available.")  
    elif retrieve == True:
        split_models = name_model.split(',')  # must send gpt and ada model in the following string: 'gpt-4o, text-embedding-ada-002'
        split_models = [s.strip() for s in split_models] 
        gpt_model = split_models[0]  
        ada_model = split_models[1]  
        prompt_token_count = token_amount(text=system_prompt, name_model=gpt_model) + token_amount(text=user_prompt, name_model=gpt_model) 
        user_prompt_token_count_embeddings = token_amount(text=user_prompt, name_model=ada_model) 
        response_token_count = token_amount(text=response, name_model=gpt_model) 
        if region == 'East US 2':
            if gpt_model == 'gpt-4o' and ada_model == 'text-embedding-ada-002' and version_model == '2024-05-13, 2':
                 prompt_cost = round((prompt_token_count / 1000) * .005, 5) + round((user_prompt_token_count_embeddings / 1000) * .0001, 5)
                 completion_cost = round(((prompt_token_count + response_token_count) / 1000) * .015, 5)
            else:  
                raise HTTPException(status_code=400, detail="Invalid model or version.")  
            return prompt_token_count, prompt_cost, response_token_count, completion_cost 
        else:
            raise HTTPException(status_code=400, detail="East US 2 region only available.")  
  
def sql_connect(system_prompt, user_prompt, time_asked, prompt_cost, response, completion_cost, name_model, version_model, 
                deployment_model, prompt_token_count, response_token_count, project, api_name):  
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
            # Insert a new system_prompt into the aoaisystm table  
            print("Warning: System_id not found for this prompt. Creating new id and adding prompt!")  
            mycursor.execute("SELECT MAX(prompt_number) FROM aoaisystem")  
            result = mycursor.fetchone()  
            prompt_number = result[0] if result[0] else 0  
            prompt_number = prompt_number + 1  # Increment the latest prompt_number by 1  
            sql = "INSERT INTO aoaisystem (system_prompt, system_proj, prompt_number) VALUES (%s, %s, %s)"  
            val = (system_prompt, project, prompt_number)  
            mycursor.execute(sql, val)  
            system_id = mycursor.lastrowid  # Get the ID of the last inserted row  
  
        # Insert into prompt table with connection to system prompt  
        sql = "INSERT INTO prompt (system_id, user_prompt, tokens, price, timestamp) VALUES (%s, %s, %s, %s, %s)"  
        val = (system_id, user_prompt, prompt_token_count, prompt_cost, time_asked)  
        mycursor.execute(sql, val)  
        prompt_id = mycursor.lastrowid  
  
        # Check if api_name already exists in the python_api table  
        mycursor.execute("SELECT api_id FROM python_api WHERE api_name = %s", (api_name,))  
        result = mycursor.fetchone()  
        if result:  
            api_id = result[0]  
        else:  
            # Insert API Name into python_api table (since there will be an API for No Rag and Rag)  
            sql = "INSERT INTO python_api (api_name) VALUES (%s)"  
            val = (api_name,)  
            mycursor.execute(sql, val)  
            api_id = mycursor.lastrowid  
  
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
  
            if name_model == 'text-embedding-ada-002' and version_model == '2':  
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"  
                val = (deployment_model, None, 0.000100, 'cl100k_base')  
                mycursor.execute(sql, val)  
                model_id = mycursor.lastrowid  
            elif name_model == 'gpt-4o' and version_model == '2024-05-13': 
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"  
                val = (deployment_model, .005000, 0.015000, 'o200k_base')  
                mycursor.execute(sql, val)  
                model_id = mycursor.lastrowid  
            elif name_model == 'gpt-4o, text-embedding-ada-002' and version_model == "2024-05-13, 2":
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"  
                val = (deployment_model, .005100, 0.015000, 'o200k_base')  # prompt_price = prompt_price <text..ada-002> + prompt_price <gpt-4o>
                mycursor.execute(sql, val)  
                model_id = mycursor.lastrowid  
            else:  
                sql = "INSERT INTO models (model, prompt_price, completion_price, tiktoken_encoding) VALUES (%s, %s, %s, %s)"  
                val = (deployment_model, None, None, None)  
                mycursor.execute(sql, val)  
                model_id = mycursor.lastrowid  
  
        # Insert into chat_completions table based on model used  
        sql = "INSERT INTO chat_completions (model_id, prompt_id, api_id, chat_completion, tokens, price) VALUES (%s, %s, %s, %s, %s, %s)"  
        val = (model_id, prompt_id, api_id, response, response_token_count, completion_cost)  
        mycursor.execute(sql, val)  
  
        # Save the changes  
        mydb.commit()  
        return {"message": f"{mycursor.rowcount} record(s) inserted into {os.getenv('azure_mysql_schema')} database."}  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"Failed to access MySQL DB with error: {e}")  
  
def main(system_prompt, user_prompt, time_asked, prompt_cost, response, completion_cost, name_model, version_model, deployment_model, prompt_token_count, 
         response_token_count, project, api_name):  
    return sql_connect(system_prompt=system_prompt, user_prompt=user_prompt, time_asked=time_asked, prompt_cost=prompt_cost, response=response, 
                        completion_cost=completion_cost, name_model=name_model, version_model=version_model, deployment_model=deployment_model, 
                        prompt_token_count=prompt_token_count, response_token_count=response_token_count, project=project, api_name=api_name)  
 
  
@app.post("/norag_api_mysql")  
def process_data(data: RequestData):  
    prompt_token_count, prompt_cost, response_token_count, completion_cost = aoai_metadata(  
        system_prompt=data.system_prompt,  
        user_prompt=data.user_prompt,  
        response=data.response,  
        name_model=data.name_model,  
        version_model=data.version_model,  
        region=data.region, 
        retrieve=data.retrieve,  
    )  
  
    result = main(  
        system_prompt=data.system_prompt,  
        user_prompt=data.user_prompt,  
        time_asked=data.time_asked,  
        prompt_cost=prompt_cost,  
        response=data.response,  
        completion_cost=completion_cost,
        name_model=data.name_model,
        version_model=data.version_model,  
        deployment_model=data.deployment_model,  
        prompt_token_count=prompt_token_count,  
        response_token_count=response_token_count,  
        project=data.project,  
        api_name=data.api_name,  
    )  
  
    return result  