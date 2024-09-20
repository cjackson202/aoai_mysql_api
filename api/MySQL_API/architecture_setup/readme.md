# Architecture Design 
To create the architecture needed for this API, please follow the below steps:

1. [Download the MySQL Installer](https://dev.mysql.com/downloads/workbench/):
Use the MySQl Installer to download MySQL Workbench. MySQL Workbench is a unified visual tool that helps you manage and design MySQL databases efficiently. ***This is how you will view and edit all the sql schema captured from the MySQL API.***

2. [Execute the ARM Template](mysql_arm.json): To create all the Azure resources for this API, execute the following ARM template from Azure CLI `mysql_arm.json`. The created resources will include:
    - [Azure MySQL Flexible Server](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview) : The estimated monthly cost for this service is $14.71, including a Standard_B1ms instance, 20 GiB of storage, and potential additional charges for auto scale IOPS, backup retention, and outbound data transfer between regions. This estimate is subject to change and final charges will be in your local currency.
    - [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/)
    - [App Service Plan](https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans)
    - [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/overview)
    
    To deploy the resources in azure run the `azure_resources_mysql_api.json` ARM template file. 
    1.  `az deployment group create --resource-group <insert your RG> --template-file mysql_arm.json`

    2. `mysql -h <insert your host name> -u <input admin name>@<input server name> -p`
        - Will be prompted for password. 

3. [Connect Flexible Server to MySQL Workbench](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/connect-workbench): Please click the URL to be directed to Microsoft Learn documentation on connecting the server to Workbench. 

4. [Create aoai_api Schema in MySQL Server](aoai_api.sql) : To create the scehma for the aoai api database, please follow these steps:

    `aoai_api.sql` vs. `aoai_api_v2.sql`:
    - **aoai_api.sql** executes the sql schema without the capturing of the API url and exact timestamp of prompt asking. 
    Useful if you only are working with one API in the sql server and are not looking for different timestamps between prompt asking and answering.
    - **aoai_api_v2.sql** executes the sql schema with capturing of the API url and exact timestamp of prompt asking. 
    Useful if you are working with multiple API's in the sql server and are looking for exact timestamps for prompt asking and the promp answer 
        - EX: ask prompt at 2024-09-18 15:32:12 and LLM api responds at 2024-09-18 15:32:16. ***Notice there is a 4 sec gap in between***.

    1. In the top left menu bar, select **File**. 
    2. From the dropdown menu, select **Open SQL Script**.
    3. Search for and select one of the sql scripts found in `architecture_setup/...`.
    4. Click the lighting bolt icon, without cursor icon, to execute the script. 
    5. At this point, the schema `aoai_api` should be created in your server. 

Extra:
Docker build command **MySQL_API**: `docker build -f api/MySQL_API/Dockerfile -t your_image_name .` 



