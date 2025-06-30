#!/usr/bin/env python3
"""Load JSONL workout data into Azure Cosmos DB."""

import json
import os
import sys
from pathlib import Path
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    env_path = Path('.env')
    if not env_path.exists():
        print("Error: .env file not found. Please create it from .env.template")
        sys.exit(1)
    
    load_dotenv(env_path)
    
    required_vars = ['COSMOS_URI', 'COSMOS_KEY', 'COSMOS_DB', 'COSMOS_CONTAINER', 'JSONL_FILE']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)


def create_cosmos_client():
    """Create and return Cosmos DB client."""
    try:
        client = CosmosClient(
            url=os.getenv('COSMOS_URI'),
            credential=os.getenv('COSMOS_KEY')
        )
        return client
    except Exception as e:
        print(f"Error creating Cosmos client: {e}")
        sys.exit(1)


def get_or_create_database(client, database_name):
    """Get or create database."""
    try:
        database = client.create_database_if_not_exists(id=database_name)
        print(f"Using database: {database_name}")
        return database
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error accessing database: {e}")
        sys.exit(1)


def get_or_create_container(database, container_name):
    """Get or create container with 'id' as partition key."""
    try:
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key={'paths': ['/id'], 'kind': 'Hash'}
        )
        print(f"Using container: {container_name}")
        return container
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error accessing container: {e}")
        sys.exit(1)


def load_jsonl_to_cosmos(container, jsonl_file_path):
    """Load JSONL records into Cosmos DB container."""
    if not Path(jsonl_file_path).exists():
        print(f"Error: JSONL file not found: {jsonl_file_path}")
        sys.exit(1)
    
    success_count = 0
    error_count = 0
    
    with open(jsonl_file_path, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                # Parse JSON record
                record = json.loads(line.strip())
                
                # Ensure 'id' field exists
                if 'id' not in record:
                    print(f"Warning: Line {line_num} missing 'id' field, skipping")
                    error_count += 1
                    continue
                
                # Upsert record
                container.upsert_item(body=record)
                success_count += 1
                
                if success_count % 100 == 0:
                    print(f"Progress: {success_count} records uploaded...")
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON on line {line_num}: {e}")
                error_count += 1
            except exceptions.CosmosHttpResponseError as e:
                print(f"Error uploading record on line {line_num}: {e}")
                error_count += 1
            except Exception as e:
                print(f"Unexpected error on line {line_num}: {e}")
                error_count += 1
    
    print(f"\nUpload complete!")
    print(f"Successfully uploaded: {success_count} records")
    print(f"Errors: {error_count} records")
    
    return success_count, error_count


def main():
    """Main function to orchestrate the upload process."""
    print("Loading Cosmos DB workout data...")
    
    # Load environment variables
    load_env()
    
    # Create Cosmos client
    client = create_cosmos_client()
    
    # Get or create database
    database = get_or_create_database(client, os.getenv('COSMOS_DB'))
    
    # Get or create container
    container = get_or_create_container(database, os.getenv('COSMOS_CONTAINER'))
    
    # Load JSONL data
    jsonl_file = os.getenv('JSONL_FILE')
    success, errors = load_jsonl_to_cosmos(container, jsonl_file)
    
    # Exit with error code if there were failures
    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()