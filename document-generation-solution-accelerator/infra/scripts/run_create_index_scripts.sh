#!/bin/bash

# Variables
# baseUrl="$1"
keyvaultName="$1"
resourceGroupName="$2"
aiFoundryName="$3"
managedIdentityClientId="$4"
# requirementFile="infra/scripts/index_scripts/requirements.txt"
# requirementFileUrl=${baseUrl}"infra/scripts/index_scripts/requirements.txt"

echo "Script Started"

# Authenticate with Azure
if az account show &> /dev/null; then
    echo "Already authenticated with Azure."
else
    if [ -n "$managedIdentityClientId" ]; then
        # Use managed identity if running in Azure
        echo "Authenticating with Managed Identity..."
        az login --identity --client-id ${managedIdentityClientId}
    else
        # Use Azure CLI login if running locally
        echo "Authenticating with Azure CLI..."
        az login
    fi
    echo "Not authenticated with Azure. Attempting to authenticate..."
fi

echo "Getting signed in user id"
signed_user_id=$(az ad signed-in-user show --query id -o tsv)
if [ $? -ne 0 ]; then
    if [ -z "$managedIdentityClientId" ]; then
        echo "Error: Failed to get signed in user id."
        exit 1
    else
        signed_user_id=$managedIdentityClientId
    fi
fi

# # Download the create_index and create table python files
# curl --output "01_create_search_index.py" ${baseUrl}"infra/scripts/index_scripts/01_create_search_index.py"
# curl --output "02_process_data.py" ${baseUrl}"infra/scripts/index_scripts/02_process_data.py"

# Define the scope for the Key Vault (replace with your Key Vault resource ID)
echo "Getting key vault resource id"
key_vault_resource_id=$(az keyvault show --name $keyvaultName --query id --output tsv)

# Check if the user has the Key Vault Administrator role
echo "Checking if user has the Key Vault Administrator role"
role_assignment=$(MSYS_NO_PATHCONV=1 az role assignment list --assignee $signed_user_id --role "Key Vault Administrator" --scope $key_vault_resource_id --query "[].roleDefinitionId" -o tsv)
if [ -z "$role_assignment" ]; then
    echo "User does not have the Key Vault Administrator role. Assigning the role."
    MSYS_NO_PATHCONV=1 az role assignment create --assignee $signed_user_id --role "Key Vault Administrator" --scope $key_vault_resource_id --output none
    if [ $? -eq 0 ]; then
        echo "Key Vault Administrator role assigned successfully."
    else
        echo "Failed to assign Key Vault Administrator role."
        exit 1
    fi
else
    echo "User already has the Key Vault Administrator role."
fi

### Assign Azure AI User role to the signed in user ###

    echo "Getting Azure AI resource id"
    aif_resource_id=$(az cognitiveservices account show --name $aiFoundryName --resource-group $resourceGroupName --query id --output tsv)

    # Check if the user has the Azure AI User role
    echo "Checking if user has the Azure AI User role"
    role_assignment=$(MSYS_NO_PATHCONV=1 az role assignment list --role 53ca6127-db72-4b80-b1b0-d745d6d5456d --scope $aif_resource_id --assignee $signed_user_id --query "[].roleDefinitionId" -o tsv)
    if [ -z "$role_assignment" ]; then
        echo "User does not have the Azure AI User role. Assigning the role."
        MSYS_NO_PATHCONV=1 az role assignment create --assignee $signed_user_id --role 53ca6127-db72-4b80-b1b0-d745d6d5456d --scope $aif_resource_id --output none
        if [ $? -eq 0 ]; then
            echo "Azure AI User role assigned successfully."
        else
            echo "Failed to assign Azure AI User role."
            exit 1
        fi
    else
        echo "User already has the Azure AI User role."
    fi

# RUN apt-get update
# RUN apt-get install python3 python3-dev g++ unixodbc-dev unixodbc libpq-dev
# apk add python3 python3-dev g++ unixodbc-dev unixodbc libpq-dev
 
# # RUN apt-get install python3 python3-dev g++ unixodbc-dev unixodbc libpq-dev
# pip install pyodbc

# Download the requirement file
# curl --output "$requirementFile" "$requirementFileUrl"

# echo "Download completed"

#Replace key vault name 
sed -i "s/kv_to-be-replaced/${keyvaultName}/g" "infra/scripts/index_scripts/01_create_search_index.py"
sed -i "s/kv_to-be-replaced/${keyvaultName}/g" "infra/scripts/index_scripts/02_process_data.py"
if [ -n "$managedIdentityClientId" ]; then
    sed -i "s/mici_to-be-replaced/${managedIdentityClientId}/g" "infra/scripts/index_scripts/01_create_search_index.py"
    sed -i "s/mici_to-be-replaced/${managedIdentityClientId}/g" "infra/scripts/index_scripts/02_process_data.py"
fi

# Determine the correct Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Python is not installed on this system. Or it is not added in the PATH."
    exit 1
fi

# create virtual environment
# Check if the virtual environment already exists
if [ -d "infra/scripts/scriptenv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    echo "Creating virtual environment"
    $PYTHON_CMD -m venv infra/scripts/scriptenv
fi

# Activate the virtual environment
if [ -f "infra/scripts/scriptenv/bin/activate" ]; then
    echo "Activating virtual environment (Linux/macOS)"
    source "infra/scripts/scriptenv/bin/activate"
elif [ -f "infra/scripts/scriptenv/Scripts/activate" ]; then
    echo "Activating virtual environment (Windows)"
    source "infra/scripts/scriptenv/Scripts/activate"
else
    echo "Error activating virtual environment. Requirements may be installed globally."
fi

# Install the requirements
echo "Installing requirements"
pip install --quiet -r infra/scripts/index_scripts/requirements.txt
echo "Requirements installed"

error_flag=false
# Run the scripts
echo "Running the python scripts"
echo "Creating the search index"
python infra/scripts/index_scripts/01_create_search_index.py
if [ $? -ne 0 ]; then
    echo "Error: 01_create_search_index.py failed."
    error_flag=true
fi

if [ "$error_flag" = false ]; then
    echo "Processing the data"
    python infra/scripts/index_scripts/02_process_data.py
    if [ $? -ne 0 ]; then
        echo "Error: 02_process_data.py failed."
        error_flag=true
    fi
fi

# revert the key vault name and managed identity client id in the python files
sed -i "s/${keyvaultName}/kv_to-be-replaced/g" "infra/scripts/index_scripts/01_create_search_index.py"
sed -i "s/${keyvaultName}/kv_to-be-replaced/g" "infra/scripts/index_scripts/02_process_data.py"
if [ -n "$managedIdentityClientId" ]; then
    sed -i "s/${managedIdentityClientId}/mici_to-be-replaced/g" "infra/scripts/index_scripts/01_create_search_index.py"
    sed -i "s/${managedIdentityClientId}/mici_to-be-replaced/g" "infra/scripts/index_scripts/02_process_data.py"
fi

if [ "$error_flag" = true ]; then
    echo "Error: One or more scripts failed during the script execution."
    exit 1
fi

echo "Scripts completed"
