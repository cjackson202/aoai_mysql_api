# NO_RAG_API  
  
## Overview  
The NO_RAG_API is designed to capture metadata from each Azure OpenAI API call and store it in a MySQL database. The metadata captured includes prompts (system & user), tokens, completions, models, costs, and projects. This metadata is not limited and can be adjusted to capture more metadata based on needs. Inside the MySQL database, the data is organized in a relational schema, ensuring efficient storage and retrieval from the project level, meaning this database can be used for more than one application.   
***Note: ONLY FOR Azure OpenAI Solutions that do not include RAG methods***.  
  
## Contents  
This sub-directory contains two main Python scripts:  
1. `norag_mysql_api.py`: This is a FastAPI python application created to insert the Azure OpenAI metadata into the MySQL database after each completion from the API call.  
    To date, only the following Azure OpenAI components are compatible with this API:  
    - **Models**:  
        - gpt-4o (2024-05-13 and 2024-08-06)  
        - gpt-4o-mini (2024-07-18)  
    - **Regions**:  
        - East US 2  
2. `call_norag_api.py`: This python script serves as a tester script where you can test the API on your Azure OpenAI instance.  
    To use the tester python file, complete the following:  
    1. **Set .env variables for your AOAI instance**  
    ```sh  
    OPENAI_API_BASE = "AOAI Endpoint"  
    OPENAI_API_VERSION = "AOAI API Version"  
    OPENAI_API_KEY = "AOAI API Key"  
    OPENAI_GPT_MODEL = "AOAI Model"  
    azure_mysql_password = "MySQL server admin password"  
    azure_mysql_host = "MySQL server host"  
    azure_mysql_user = "MySQL admin user"  
    azure_mysql_schema = "MySQL schema (should be aoai_api)"  
    ```  
    2. **Run the API locally on your machine using this command:**  
    ```sh  
    uvicorn norag_mysql_api:app --reload  
    ```  
    Note: If you build the API from the docker file provided, you must switch to run on port 8000 with the following command (set docker .env variables in `/docker_env/.env`):  
    ```sh  
    docker run -p 8000:80 --env-file ./docker_env/.env mysql_aoai_api:v1  
    ```  
    3. **Navigate to the No_Rag_API Sub-Directory:**  
    ```sh  
    cd api/No_Rag_API  
    ```  
    4. **Run the python script from the terminal:**  
    ```sh  
    python call_norag_api.py  
    ```  
    
    Note - The following headers must be passed to the API's GET:
    ```python 
        data = {  
        "system_prompt": "", # System prompt given to the AOAI model.

        "user_prompt": "", # User prompt in which the end-user asks the model. 

        "response": "", # Model's answer to the user prompt

        "deployment_model": "", # Input your model's deployment name here

        "name_model": "", # Input you model here

        "version_model": "", # Input your model version here. NOT API VERSION.

        "region": "",  # Input your AOAI resource region here
        
        "project": ""  # Input your project name here. 
    }  
    ```
  
## Modifying Metadata Capturing  
  
If you want to modify the metadata captured, follow these steps:  
  
1. **Modify the SQL Schema**:  
    - For instance, if you want to start capturing a user credential, create a new table called `users` in the SQL database and create a relationship with the `prompt` table using `prompt_id`.  
    - Example SQL commands to create a `users` table and add a foreign key relationship:  
      ```sql  
      CREATE TABLE users (  
          user_id INT AUTO_INCREMENT PRIMARY KEY,  
          prompt_id INT,  
          username VARCHAR(50) NOT NULL,     
          CONSTRAINT fk_prompt FOREIGN KEY (prompt_id) REFERENCES prompt(prompt_id)  
      );  
      ```  
  
2. **Update the Python Script**:  
    - Modify the `norag_mysql_api.py` script to include the logic for capturing and inserting the new metadata:
        - Add new parameters to `sql_connect()` to accept `username`.    
      - Insert the `username` and `prompt_id` into the created `users` table. 
    - Example function modification:  
      ```python  
      def sql_connect(system_prompt, user_prompt, prompt_cost, response, completion_cost, deployment_model, prompt_token_count, response_token_count, project, username):  
          # Connect to MySQL  
          connection = mysql.connector.connect(  
              host=os.getenv("azure_mysql_host"),  
              user=os.getenv("azure_mysql_user"),  
              password=os.getenv("azure_mysql_password"),  
              database=os.getenv("azure_mysql_schema")  
          )  
          cursor = connection.cursor()  
  
          # Existing code...  
  
          # Insert user login information into the users table with prompt_id  
          sql = "INSERT INTO users (prompt_id, username) VALUES (%s, %s)"  
          val = (prompt_id, username)  
          cursor.execute(sql, val)  
  
          # Commit the changes  
          connection.commit()  
      ```  

