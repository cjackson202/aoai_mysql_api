'''
This script is designed to make calls to the Azure OpenAI Service (AOAI) through Azure API Management (APIM). 
It captures the API’s metadata within the policy and then sends this information to the apim_api API.

Notes:
- Additional params set in code must be passed to the POST in headers. 
- APIM will handle returning the response, url
- Line 33 APIM Completions URL: "https://<APIM Resource>.azure-api.net/<API>/deployments/{model}/chat/completions?api-version={version}"

Updated: 9/27/24
'''

import requests
import os 
from dotenv import load_dotenv
from datetime import datetime, timezone
import json

load_dotenv()

api_key = os.getenv("APIM_API_KEY")
endpoint = os.getenv("APIM_COMPLETIONS_URL")
deployment_name = os.getenv("OPENAI_GPT_MODEL")
api_version = os.getenv("OPENAI_API_VERSION")

def get_time():
    # Capture the current date and time in UTC (MySQL Native timezone)
    current_utc_time = datetime.now(timezone.utc)  
    # Format the date and time to the desired string format  
    formatted_time = current_utc_time.strftime('%Y-%m-%d %H:%M:%S') 
    return formatted_time 

# Using APIM url to make AOAI request 
endpoint = endpoint.replace("{model}", deployment_name).replace("{version}", api_version) 

system_prompt = "You are a funny Disney character. Make the user guess your name."

while True:
    user_prompt = input("\nYou: ")

    headers = {
        'Content-Type':'application/json',
        "system_prompt": system_prompt,  # System prompt given to the AOAI model.
        "user_prompt": user_prompt,  # User prompt in which the end-user asks the model. 
        "time_asked": get_time(), # Time in which the user prompt was asked.
        "deployment_model": deployment_name, # Input your model's deployment name here
        "name_model": "gpt-4o",  # Input you model here
        "version_model": "2024-05-13",  # Input your model version here. NOT API VERSION.
        "region": "East US 2",  # Input your AOAI resource region here
        "project": "Disney Character (API Test)",  # Input your project name here. Following the system prompt for this test currently :)
        "database": "mysqldb", # Specify here cosmosdb or mysql as database. 
        "retrieve": "False" # Must specify True or False here as string (will only be passed in header as string)
    }

    data = {    
        'messages':[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        }

    response = requests.post(endpoint, headers=headers, json=data)
    # print(type(response))
    response = response.json()
    response = response['choices'][0]['message']["content"]
    print(f"\nGPT: {response}\n")