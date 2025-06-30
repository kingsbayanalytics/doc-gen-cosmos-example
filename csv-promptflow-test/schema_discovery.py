#!/usr/bin/env python3
"""Discover database schema and categorical values for dynamic query generation."""

import os
import json
from azure.cosmos import CosmosClient
from promptflow.core import tool
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Cache for schema information
_schema_cache = None


def get_distinct_values(container, field_name, limit=100):
    """Get distinct values for a field from Cosmos DB."""
    try:
        # Query for distinct values
        query = f"SELECT DISTINCT VALUE c.{field_name} FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items[:limit]  # Limit to prevent too many values
    except Exception as e:
        logging.warning(f"Could not get distinct values for {field_name}: {e}")
        return []


def discover_schema():
    """Discover the database schema including field types and categorical values."""
    global _schema_cache
    
    # Return cached schema if available
    if _schema_cache is not None:
        return _schema_cache
    
    try:
        # Initialize Cosmos DB client
        client = CosmosClient(
            url=os.getenv("COSMOS_URI"),
            credential=os.getenv("COSMOS_KEY")
        )
        database = client.get_database_client(os.getenv("COSMOS_DB"))
        container = database.get_container_client(os.getenv("COSMOS_CONTAINER"))
        
        # Get a sample document to understand structure
        query = "SELECT TOP 1 * FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if not items:
            return None
            
        sample_doc = items[0]
        
        # Build schema information
        schema = {
            "fields": {},
            "categorical_values": {}
        }
        
        # Analyze each field
        for field_name, value in sample_doc.items():
            # Skip system fields
            if field_name.startswith("_"):
                continue
                
            # Determine field type
            field_type = type(value).__name__
            schema["fields"][field_name] = {
                "type": field_type,
                "sample_value": str(value)[:50]  # Truncate long values
            }
            
            # For string fields that might be categorical, get distinct values
            if field_type == "str" and field_name in ["Exercise", "ExType"]:
                distinct_values = get_distinct_values(container, field_name)
                if distinct_values:
                    schema["categorical_values"][field_name] = distinct_values
        
        # Cache the schema
        _schema_cache = schema
        return schema
        
    except Exception as e:
        logging.error(f"Error discovering schema: {e}")
        return None


@tool
def get_schema_context() -> str:
    """
    Get schema context including categorical values for query generation.
    
    Returns:
        JSON string with schema information
    """
    schema = discover_schema()
    
    if schema is None:
        return json.dumps({
            "error": "Could not discover schema",
            "fields": {
                "Exercise": "string (exercise name)",
                "ExType": "string (exercise type)",
                "Reps": "string (repetitions)",
                "Weight": "string (weight)",
                "Set": "string (set number)"
            }
        })
    
    # Format schema for LLM consumption
    context = {
        "fields": schema["fields"],
        "categorical_values": schema["categorical_values"],
        "notes": {
            "Exercise": f"Valid exercise names include: {', '.join(schema['categorical_values'].get('Exercise', [])[:20])}",
            "ExType": f"Valid exercise types: {', '.join(schema['categorical_values'].get('ExType', []))}",
        }
    }
    
    return json.dumps(context, indent=2)


# For local testing
if __name__ == "__main__":
    schema_json = get_schema_context()
    print("Schema Context:")
    print(schema_json)