#!/usr/bin/env python3
"""Debug CosmosDB chat history configuration."""

import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

# Load environment variables
load_dotenv('.env')

def test_cosmos_chat_connection():
    """Test if we can connect to CosmosDB for chat history."""
    
    print("🔍 Debug CosmosDB Chat History Configuration")
    print("=" * 50)
    
    # Check environment variables
    account = os.getenv("AZURE_COSMOSDB_ACCOUNT")
    key = os.getenv("AZURE_COSMOSDB_ACCOUNT_KEY") 
    database = os.getenv("AZURE_COSMOSDB_DATABASE")
    container = os.getenv("AZURE_COSMOSDB_CONVERSATIONS_CONTAINER")
    
    print(f"Account: {account}")
    print(f"Key: {'***' + key[-10:] if key else 'MISSING'}")
    print(f"Database: {database}")
    print(f"Container: {container}")
    print()
    
    if not all([account, key, database, container]):
        print("❌ Missing required environment variables!")
        return False
    
    try:
        # Test connection
        print("🔌 Testing CosmosDB connection...")
        client = CosmosClient(url=account, credential=key)
        
        # Test database access
        print(f"📁 Testing database '{database}'...")
        db = client.get_database_client(database)
        
        # Test container access
        print(f"📦 Testing container '{container}'...")
        chat_container = db.get_container_client(container)
        
        # Try a simple query to verify access
        print("🔍 Testing container query access...")
        query = "SELECT TOP 1 * FROM c"
        items = list(chat_container.query_items(query=query, enable_cross_partition_query=True))
        
        print(f"✅ SUCCESS! Container has {len(items)} items")
        if items:
            print(f"Sample item keys: {list(items[0].keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        
        # Specific error handling
        if "Unauthorized" in str(e):
            print("🔑 Issue: Invalid credentials or access denied")
        elif "NotFound" in str(e):
            print("📁 Issue: Database or container doesn't exist")
        elif "Forbidden" in str(e):
            print("🚫 Issue: Access forbidden - check permissions")
        
        return False

def test_settings_validation():
    """Test if the backend settings validation works."""
    
    print("\n🔧 Testing Backend Settings Validation")
    print("=" * 50)
    
    try:
        # Import the settings to see if they validate
        import sys
        sys.path.append('src/backend')
        from settings import _ChatHistorySettings
        
        print("📋 Testing _ChatHistorySettings validation...")
        chat_settings = _ChatHistorySettings()
        
        print("✅ Chat history settings validation PASSED")
        print(f"Account: {chat_settings.account}")
        print(f"Database: {chat_settings.database}")
        print(f"Container: {chat_settings.conversations_container}")
        print(f"Feedback enabled: {chat_settings.enable_feedback}")
        
        return True
        
    except Exception as e:
        print(f"❌ Settings validation FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting CosmosDB Chat History Debug...")
    print()
    
    # Test 1: Direct connection
    connection_ok = test_cosmos_chat_connection()
    
    # Test 2: Settings validation  
    settings_ok = test_settings_validation()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"CosmosDB Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"Settings Validation: {'✅ PASS' if settings_ok else '❌ FAIL'}")
    
    if connection_ok and settings_ok:
        print("\n🎉 Chat history should work! Try restarting your backend.")
    else:
        print("\n🔧 Fix the above issues and try again.")