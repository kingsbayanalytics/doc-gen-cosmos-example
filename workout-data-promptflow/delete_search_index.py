#!/usr/bin/env python3
"""Delete Azure AI Search index to allow recreation with correct dimensions."""

import os
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def delete_search_index():
    """Delete the existing search index."""
    
    # Initialize Search Index Client
    search_client = SearchIndexClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY"))
    )
    
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    
    try:
        # Delete the index
        search_client.delete_index(index_name)
        print(f"Successfully deleted index: {index_name}")
        return True
    except Exception as e:
        print(f"Error deleting index: {e}")
        return False


if __name__ == "__main__":
    print("Deleting Azure AI Search index...")
    success = delete_search_index()
    if success:
        print("\n✅ Index deleted successfully!")
        print("Run 'python create_search_index.py' to recreate with correct dimensions")
    else:
        print("\n❌ Failed to delete index")