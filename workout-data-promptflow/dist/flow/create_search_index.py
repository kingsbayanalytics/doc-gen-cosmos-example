#!/usr/bin/env python3
"""Create Azure AI Search index with vector embeddings for workout data."""

import os
import json
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    VectorSearchAlgorithmKind,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
    SemanticSearch
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_workout_index():
    """Create Azure AI Search index for workout data with vector search capabilities."""
    
    # Initialize Search Index Client
    search_client = SearchIndexClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY"))
    )
    
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
    
    # Define search fields
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="ExDate", type=SearchFieldDataType.String, filterable=True, sortable=True),
        SearchableField(name="Exercise", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="Set", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="Reps", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
        SimpleField(name="Weight", type=SearchFieldDataType.Double, filterable=True, sortable=True),
        SearchableField(name="ExType", type=SearchFieldDataType.String, filterable=True, facetable=True),
        
        # Combined searchable text field for better search
        SearchableField(name="SearchableText", type=SearchFieldDataType.String, analyzer_name="standard.lucene"),
        
        # Vector field for embeddings (3072 dimensions for text-embedding-3-large)
        SearchField(
            name="Embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="workout-vector-profile"
        )
    ]
    
    # Configure vector search
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="workout-vector-profile",
                algorithm_configuration_name="workout-hnsw-config"
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(
                name="workout-hnsw-config",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            )
        ]
    )
    
    # Configure semantic search
    semantic_config = SemanticConfiguration(
        name="workout-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            content_fields=[
                SemanticField(field_name="SearchableText"),
                SemanticField(field_name="Exercise")
            ],
            keywords_fields=[
                SemanticField(field_name="ExType"),
                SemanticField(field_name="Exercise")
            ]
        )
    )
    
    semantic_search = SemanticSearch(configurations=[semantic_config])
    
    # Create the index
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search
    )
    
    try:
        # Create or update the index
        result = search_client.create_or_update_index(index)
        print(f"Successfully created/updated index: {result.name}")
        print(f"Index has {len(result.fields)} fields")
        return True
    except Exception as e:
        print(f"Error creating index: {e}")
        return False


if __name__ == "__main__":
    print("Creating Azure AI Search index for workout data...")
    success = create_workout_index()
    if success:
        print("\n✅ Index created successfully!")
        print("Next step: Run 'python populate_search_index.py' to add embeddings and data")
    else:
        print("\n❌ Failed to create index")