# Architecture Design 

## MySQL Setup
To create the architecture needed for this API, please follow the below steps:

1. [Download the MySQL Installer](https://dev.mysql.com/downloads/workbench/):
Use the MySQl Installer to download MySQL Workbench. MySQL Workbench is a unified visual tool that helps you manage and design MySQL databases efficiently. ***This is how you will view and edit all the sql schema captured from the MySQL API.***

2. [Execute the ARM Template](mysql/mysql_arm.json): To create all the Azure resources for this API, execute the following ARM template from Azure CLI `mysql_arm.json`. The created resources will include:
    - [Azure MySQL Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview)
    
    To deploy the resources in azure run the `azure_resources_mysql_api.json` ARM template file. 
    1.  `az deployment group create --resource-group <insert your RG> --template-file mysql_arm.json`

3. [Connect Flexible Server to MySQL Workbench](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/connect-workbench): Please click the URL to be directed to Microsoft Learn documentation on connecting the server to Workbench. 

4. [Create aoai_api Schema in MySQL Server](mysql/aoai_api_v2.sql) : To create the scehma for the aoai api database, please follow these steps:
    - **aoai_api_v2.sql** executes the sql schema with capturing of the API url and exact timestamp of prompt asking. 
    Useful if you are working with multiple API's in the sql server and are looking for exact timestamps for prompt asking and the promp answer 
        - EX: ask prompt at 2024-09-18 15:32:12 and LLM api responds at 2024-09-18 15:32:16. ***Notice there is a 4 sec gap in between***.

    1. In the top left menu bar, select **File**. 
    2. From the dropdown menu, select **Open SQL Script**.
    3. Search for and select one of the sql scripts found in `architecture_setup/...`.
    4. Click the lighting bolt icon, without cursor icon, to execute the script. 
    5. At this point, the schema `aoai_api` should be created in your server. 

## CosmosDB Setup

1. [Execute the ARM Template](mysql/cosmos_arm.json): To create all the Azure resources for this API, execute the following ARM template from Azure CLI `cosmos_arm.json`. The created resources will include:
    - [Azure CosmosDB](https://learn.microsoft.com/en-us/azure/cosmos-db/)
    
    To deploy the resources in azure run the `azure_resources_mysql_api.json` ARM template file. 
    1.  `az deployment group create --resource-group <insert your RG> --template-file cosmos_arm.json`

---



