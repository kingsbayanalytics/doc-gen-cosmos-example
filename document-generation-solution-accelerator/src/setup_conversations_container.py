#!/usr/bin/env python3
"""
Setup script to create the conversations container in Cosmos DB for template history.
"""

import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

def setup_conversations_container():
    """Create the conversations container if it doesn't exist."""
    
    # Cosmos DB configuration from environment
    account_uri = f"https://{os.getenv('AZURE_COSMOSDB_ACCOUNT')}.documents.azure.com:443/"
    account_key = os.getenv('AZURE_COSMOSDB_ACCOUNT_KEY')
    database_name = os.getenv('AZURE_COSMOSDB_DATABASE', 'sql-test')
    container_name = os.getenv('AZURE_COSMOSDB_CONVERSATIONS_CONTAINER', 'conversations')
    
    print(f"🔗 Connecting to Cosmos DB...")
    print(f"   Account: {os.getenv('AZURE_COSMOSDB_ACCOUNT')}")
    print(f"   Database: {database_name}")
    print(f"   Container: {container_name}")
    
    try:
        # Initialize Cosmos client
        client = CosmosClient(account_uri, account_key)
        
        # Get database
        database = client.get_database_client(database_name)
        print(f"✅ Connected to database: {database_name}")
        
        # Check if conversations container exists
        try:
            container = database.get_container_client(container_name)
            # Try to read container properties to verify it exists
            container_properties = container.read()
            print(f"✅ Container '{container_name}' already exists")
            print(f"   Partition Key: {container_properties['partitionKey']['paths']}")
            return True
            
        except exceptions.CosmosResourceNotFoundError:
            print(f"📝 Container '{container_name}' not found, creating...")
            
            # Create conversations container with userId as partition key
            container = database.create_container(
                id=container_name,
                partition_key=PartitionKey(path="/userId"),
                offer_throughput=400  # Minimum throughput
            )
            
            print(f"✅ Successfully created container: {container_name}")
            print(f"   Partition Key: /userId")
            print(f"   Throughput: 400 RU/s")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Setting up CosmosDB conversations container for template history...")
    success = setup_conversations_container()
    if success:
        print("\n🎉 Setup complete! Template history should now work properly.")
    else:
        print("\n💥 Setup failed. Please check your Cosmos DB configuration.")