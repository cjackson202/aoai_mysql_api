# APIM_API  
  
## Overview  
`apim_api` is designed to capture metadata from an Azure API Management (APIM) policy, which manages the Azure OpenAI API call. The APIM policy calls the api to store metadata in a MySQL or Cosmos database. The metadata captured includes prompts (system & user), tokens, completions, models, costs, and projects. This metadata is not limited and can be adjusted to capture more metadata based on needs. In the MySQL database, data is organized using a relational schema, ensuring efficient storage and retrieval at the project level. Conversely, in the Cosmos DB, data is stored in JSON format, allowing for flexible data types and eliminating the need for a rigid relational schema.
***Note: ONLY FOR Azure OpenAI Solutions that include regular chat and RAG methods***.  
  
## Contents  
This sub-directory contains 2 python API script and 3 python API tester scripts (Chat, RAG (Index), RAG (Query)):  
### Python API script
1. `apim_api.py`: Similiar API to #1 except, the response from API is handled differently, allowing APIM to pass response to API in a policy. 
***Use when calling in APIM policy***.
  
    To date, only the following Azure OpenAI components are compatible with both APIs:  
    - **Models**:  
        - ***gpt-4o (2024-05-13 and 2024-08-06)***: configured for regional API. Although API will still execute, pricing differs between Global & Regional deployments. 
        - ***gpt-4o-mini (2024-07-18)***: configured for regional API. Although API will still execute, pricing differs between Global & Regional deployments. 
        - ***gpt-4 (turbo-2024-04-09)***
        - ***text-embedding-ada-002 (2)***
    - **Regions**:  
        - ***East US***
        - ***East US 2***