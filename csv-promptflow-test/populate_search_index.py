#!/usr/bin/env python3
"""Populate Azure AI Search index with workout data and embeddings."""

import os
import json
import asyncio
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()


def create_searchable_text(record):
    """Create a searchable text field combining all relevant workout information."""
    parts = []
    
    if record.get('Exercise'):
        parts.append(f"Exercise: {record['Exercise']}")
    if record.get('ExType'):
        parts.append(f"Type: {record['ExType']}")
    if record.get('Weight'):
        parts.append(f"Weight: {record['Weight']} lbs")
    if record.get('Reps'):
        parts.append(f"Reps: {record['Reps']}")
    if record.get('Set'):
        parts.append(f"Set: {record['Set']}")
    if record.get('ExDate'):
        parts.append(f"Date: {record['ExDate']}")
    
    return " | ".join(parts)


def get_embedding(text, openai_client, deployment_name):
    """Get embedding for text using Azure OpenAI."""
    try:
        response = openai_client.embeddings.create(
            model=deployment_name,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding for text '{text[:50]}...': {e}")
        return None


def populate_search_index():
    """Populate the search index with workout data and embeddings."""
    
    # Initialize clients
    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY"))
    )
    
    openai_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    jsonl_file = os.getenv("JSONL_FILE")
    
    # Read workout data
    documents = []
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            try:
                record = json.loads(line.strip())
                
                # Create searchable text
                searchable_text = create_searchable_text(record)
                
                # Get embedding
                print(f"Processing record {line_num}: {record.get('Exercise', 'Unknown')}...")
                embedding = get_embedding(searchable_text, openai_client, embedding_deployment)
                
                if embedding:
                    # Prepare document for search index
                    search_doc = {
                        "id": record["id"],
                        "ExDate": record.get("ExDate", ""),
                        "Exercise": record.get("Exercise", ""),
                        "Set": int(record.get("Set", 0)) if record.get("Set") else 0,
                        "Reps": int(record.get("Reps", 0)) if record.get("Reps") else 0,
                        "Weight": float(record.get("Weight", 0)) if record.get("Weight") else 0.0,
                        "ExType": record.get("ExType", ""),
                        "SearchableText": searchable_text,
                        "Embedding": embedding
                    }
                    
                    documents.append(search_doc)
                
                # Add small delay to avoid rate limiting
                if line_num % 10 == 0:
                    time.sleep(1)
                    
                # Upload in batches of 100
                if len(documents) >= 100:
                    print(f"Uploading batch of {len(documents)} documents...")
                    try:
                        result = search_client.upload_documents(documents)
                        print(f"Uploaded {len([r for r in result if r.succeeded])} documents successfully")
                        documents = []
                    except Exception as e:
                        print(f"Error uploading batch: {e}")
                        documents = []
                        
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON on line {line_num}: {e}")
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
    
    # Upload remaining documents
    if documents:
        print(f"Uploading final batch of {len(documents)} documents...")
        try:
            result = search_client.upload_documents(documents)
            print(f"Uploaded {len([r for r in result if r.succeeded])} documents successfully")
        except Exception as e:
            print(f"Error uploading final batch: {e}")
    
    print("\n✅ Search index population complete!")


if __name__ == "__main__":
    print("Populating Azure AI Search index with workout data and embeddings...")
    populate_search_index()