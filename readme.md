# Azure OpenAI MySQL API

This repository offers a complete solution to capturing essential metadata from Azure OpenAI API calls. 

## API's 
1. [MySQL_API](api/MySQL_API/readme.md): Created for capturing AOAI APi metadata into a MySQL server for chat (chat completions), RAG (Index), and RAG (Querying). 

## Getting started
To get started with this repository, please set up you environment in the following steps:

**Create .venv environment in code interpretor**
- Steps reflect creating .venv in VsCode
```
1. Open the command palette: CTRL + SHIFT + P
2. Search: Python: Create Environment
3. Select: Venv
4. Select the latest version of Python installed on your device.
5. .venv environment created
```

**Install the necessary libraries**
```sh
pip install -r requirements.txt  
```

**Set Env Variables**
```sh  
    OPENAI_API_BASE = "AOAI Endpoint"  
    OPENAI_API_VERSION = "AOAI API Version"  
    OPENAI_API_KEY = "AOAI API Key"  
    OPENAI_GPT_MODEL = "AOAI GPT Model deployment name" 
    OPENAI_ADA_MODEL = "AOAI ADA Model deployment name" 
    AZURE_AI_SEARCH_URL = "Azure AI Search endpoint"
    AZURE_AI_SEARCH_KEY = "Azure AI Search key"
    AZURE_AI_SEARCH_INDEX = 'Azure AI Search index name'
    azure_mysql_password = "MySQL server admin password"  
    azure_mysql_host = "MySQL server host"  
    azure_mysql_user = "MySQL admin user"  
    azure_mysql_schema = "MySQL schema (should be aoai_api)"  
```  

## Additional Resources  
  
For further reading and additional support, you might find the following resources helpful:  
  
- ['Azure OpenAI Models Pricing'](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)  
- ['Azure Database for MySQL'](https://learn.microsoft.com/en-us/azure/mysql/)  
- ['MySQL Workbench Installer'](https://dev.mysql.com/downloads/workbench/)  
- ['Azure OpenAI PTU'](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/provisioned-throughput-onboarding)  
- ['TikToken - OpenAI LLM Token Counter'](https://github.com/openai/tiktoken)
  