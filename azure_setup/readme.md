To create the arm template in azure run the `mysql_arm.json` ARM file. 

1.  `az deployment group create --resource-group <insert your RG> --template-file mysql_arm.json`

2. `mysql -h <insert your host name> -u <input admin name>@<input server name> -p`
    - Will be prompted for password. 