#!/usr/bin/env python3
"""Execute SQL queries against Azure Cosmos DB and return results."""

import os
import json
from promptflow.core import tool
from azure.cosmos import CosmosClient
from dotenv import load_dotenv


# Load environment variables when running locally
load_dotenv()


@tool
def cosmos_query_runner(sql_query: str) -> str:
    """
    Execute SQL query against Cosmos DB and return results.
    
    Args:
        sql_query: SQL query string to execute
        
    Returns:
        JSON string containing query results or error message
    """
    try:
        # Initialize Cosmos client
        client = CosmosClient(
            url=os.getenv('COSMOS_URI'),
            credential=os.getenv('COSMOS_KEY')
        )
        
        # Get database and container references
        database = client.get_database_client(os.getenv('COSMOS_DB'))
        container = database.get_container_client(os.getenv('COSMOS_CONTAINER'))
        
        # Execute query
        print(f"Executing query: {sql_query}")
        
        # Enable aggregate queries 
        items = list(container.query_items(
            query=sql_query,
            enable_cross_partition_query=True,
            populate_query_metrics=True,
            max_integrated_cache_staleness_in_ms=0
        ))
        
        # Format results
        if not items:
            return json.dumps({
                "status": "success",
                "message": "Query executed successfully but returned no results",
                "count": 0,
                "results": []
            }, indent=2)
        
        # For aggregation queries that return a single value
        if len(items) == 1 and isinstance(items[0], dict):
            # Check if it's an aggregation result
            keys = list(items[0].keys())
            if len(keys) == 1 and keys[0].startswith('$'):
                return json.dumps({
                    "status": "success",
                    "message": "Query executed successfully",
                    "count": 1,
                    "value": items[0][keys[0]],
                    "results": items
                }, indent=2)
        
        # For regular queries
        return json.dumps({
            "status": "success",
            "message": f"Query returned {len(items)} results",
            "count": len(items),
            "results": items[:100]  # Limit to first 100 results
        }, indent=2)
        
    except Exception as e:
        error_message = f"Error executing query: {str(e)}"
        print(error_message)
        
        return json.dumps({
            "status": "error",
            "message": error_message,
            "query": sql_query
        }, indent=2)


# For local testing
if __name__ == "__main__":
    test_queries = [
        "SELECT COUNT(1) FROM c WHERE c.ExType = 'Strength'",
        "SELECT TOP 5 c.Exercise, c.Weight FROM c ORDER BY c.Weight DESC",
        "SELECT AVG(c.Reps) FROM c WHERE c.Exercise = 'Bench Press'"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        result = cosmos_query_runner(query)
        print(f"Result: {result}")
        print("-" * 80)