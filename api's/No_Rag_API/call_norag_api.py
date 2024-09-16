import requests  
import json  
import os
from openai import AzureOpenAI

while True:
    # Make AOAI request
    api_key = os.getenv("OPENAI_API_KEY")
    endpoint = os.getenv("OPENAI_API_BASE")
    deployment_name = os.getenv("OPENAI_GPT_COMMERCIAL")
    system_prompt = "You are a funny Disney character. Make the user guess your name."
    user_prompt = input("You: ")
    client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=os.getenv("OPENAI_API_VERSION")
    )
    response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    )
    response = response.to_json()
    response = json.loads(response)
    response = response['choices'][0]['message']["content"]
    print(response)

    # Call MySQL API to capture metadata (make sure api is running locally)
    url = "http://127.0.0.1:8000/process"  
    
    data = {  
        "system_prompt": system_prompt,  
        "user_prompt": user_prompt,  
        "response": response,  
        "deployment_model": deployment_name, # Input your model's deployment name here
        "name_model": "gpt-4o",  # Input you model here
        "version_model": "2024-05-13",  # Input your model version here. NOT API VERSION.
        "region": "East US 2",  # Input your AOAI resource region here
        "project": "Disney Character (API Test)"  # Input your project name here. API Test is used for testing here :)
    }  
    
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))  
    
    print(response.status_code)  
    print(response.json())  