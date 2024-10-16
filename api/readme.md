# API Comparison: `apim_api` vs. `code_api`  
  
This README provides a comparison between `apim_api` and `code_api`, helping you decide which approach best suits your needs.  
  
## Overview  
  
- **`code_api`**: Provides high flexibility and customization for handling data payloads.  
- **`apim_api`**: Streamlines data handling within API Management (APIM) policies, reducing the need for frequent code changes.  
  
## Key Considerations  
  
### Flexibility and Customization  
- **`code_api`**: Greater flexibility, ideal for projects requiring frequent adjustments or custom logic.  
- **`apim_api`**: Less flexible, better for stable scenarios with infrequent changes. However, you still need to write code for `apim_api`, especially when creating new projects or updating the API to handle new responses.  
  
### Development and Maintenance Overhead  
- **`code_api`**: Higher overhead due to the need for custom code in each instance.  
- **`apim_api`**: Lower overhead by centralizing metadata handling within APIM policies, but some code updates are still necessary.  
  
### Complexity of Implementation  
- **`code_api`**: More complex, requires developers to manage parsing and data insertion.  
- **`apim_api`**: Simplified, APIM handles the response body and metadata insertion, though initial setup and occasional updates are required.  
  
### Frequency of Deployment  
- **`code_api`**: Suitable for environments with frequent updates.  
- **`apim_api`**: Better for stable environments with less frequent updates, but still requires updates for new projects or significant changes.  
  
### Use Case Scenarios  
- **`code_api`**: Recommended for projects needing high customization and complex logic.  
- **`apim_api`**: Ideal for projects requiring stability and a streamlined approach, with occasional code updates for new requirements.  
  
## Decision Matrix  
  
| Criteria                        | `code_api`                         | `apim_api`                         |  
|---------------------------------|------------------------------------|------------------------------------|  
| Flexibility                     | High                               | Low                                |  
| Customization                   | High                               | Low                                |  
| Development Overhead            | Higher                             | Lower                              |  
| Maintenance Overhead            | Higher                             | Lower                              |  
| Complexity of Implementation    | Higher                             | Lower                              |  
| Frequency of Deployment         | Frequent updates acceptable        | Stable, less frequent updates      |  
| Use Case                        | High customization and complexity  | Stability and streamlined approach |  

## Environment setup 
At a minimum, set the following .env variables to execute ***/api_testers*** for both api's:
```sh  
    OPENAI_API_BASE = "AOAI Endpoint"  
    OPENAI_API_VERSION = "AOAI API Version"  
    OPENAI_API_KEY = "AOAI API Key"  
    OPENAI_GPT_MODEL = "AOAI GPT Model deployment name" 
    OPENAI_ADA_MODEL = "AOAI ADA Model deployment name" 
    AZURE_AI_SEARCH_URL = "Azure AI Search endpoint"
    AZURE_AI_SEARCH_KEY = "Azure AI Search key"
    AZURE_AI_SEARCH_INDEX = 'Azure AI Search index name'
```  
## Conclusion  
  
By considering the factors listed above, you can determine whether `code_api` or `apim_api` is the best fit for your project.   
  
- Choose **`code_api`** if your project requires high flexibility, customization, and can handle higher development and maintenance overhead.  
- Choose **`apim_api`** if your project benefits from a stable, streamlined approach with lower overhead and less frequent need for customization. Note that while `apim_api` reduces the need for frequent code changes, you still need to update the API to handle new responses or projects.  
