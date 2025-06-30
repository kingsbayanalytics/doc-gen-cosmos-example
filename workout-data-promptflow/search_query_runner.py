#!/usr/bin/env python3
"""Execute semantic and vector searches against Azure AI Search."""

import os
import json
from promptflow.core import tool
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@tool
def search_query_runner(question: str, search_type: str = "hybrid") -> str:
    """
    Execute search against Azure AI Search using semantic, vector, or hybrid search.
    
    Args:
        question: Natural language question about workout data
        search_type: Type of search - "semantic", "vector", "hybrid", or "keyword"
        
    Returns:
        JSON string containing search results
    """
    try:
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
        
        print(f"Executing {search_type} search for: {question}")
        
        if search_type in ["vector", "hybrid"]:
            # Get embedding for the question
            response = openai_client.embeddings.create(
                model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                input=question
            )
            query_embedding = response.data[0].embedding
        else:
            query_embedding = None
        
        # Configure search parameters based on type
        search_params = {
            "search_text": question,
            "top": 20,
            "include_total_count": True
        }
        
        if search_type == "semantic":
            search_params.update({
                "query_type": "semantic",
                "semantic_configuration_name": "workout-semantic-config",
                "query_caption": "extractive",
                "query_answer": "extractive"
            })
        elif search_type == "vector":
            search_params = {
                "vector_queries": [{
                    "kind": "vector",  # <-- MISSING! This fixes the error
                    "vector": query_embedding,
                    "k_nearest_neighbors": 20,
                    "fields": "Embedding"
                }],
                "top": 20,
                "include_total_count": True
            }
        elif search_type == "hybrid":
            search_params.update({
                "vector_queries": [{
                    "kind": "vector",  # <-- MISSING! This fixes the error
                    "vector": query_embedding,
                    "k_nearest_neighbors": 20,
                    "fields": "Embedding"
                }],
                "query_type": "semantic",
                "semantic_configuration_name": "workout-semantic-config"
            })
        
        # Execute search
        results = search_client.search(**search_params)
        
        # Process results
        search_results = []
        total_count = getattr(results, 'get_count', lambda: 0)()
        
        for result in results:
            search_result = {
                "id": result.get("id"),
                "exercise": result.get("Exercise"),
                "exercise_type": result.get("ExType"),
                "date": result.get("ExDate"),
                "weight": result.get("Weight"),
                "reps": result.get("Reps"),
                "set": result.get("Set"),
                "searchable_text": result.get("SearchableText"),
                "score": result.get("@search.score", 0)
            }
            
            # Add semantic fields if available
            if hasattr(result, '@search.captions'):
                search_result["captions"] = [caption.text for caption in result['@search.captions']]
            if hasattr(result, '@search.answers'):
                search_result["answers"] = [answer.text for answer in result['@search.answers']]
                
            search_results.append(search_result)
        
        # Format response
        response_data = {
            "status": "success",
            "search_type": search_type,
            "query": question,
            "total_count": total_count,
            "returned_count": len(search_results),
            "results": search_results[:10]  # Limit to top 10 for readability
        }
        
        return json.dumps(response_data, indent=2)
        
    except Exception as e:
        error_message = f"Error executing search: {str(e)}"
        print(error_message)
        
        return json.dumps({
            "status": "error",
            "search_type": search_type,
            "message": error_message,
            "query": question
        }, indent=2)


# For local testing
if __name__ == "__main__":
    test_queries = [
        "bench press exercises with heavy weight",
        "cardio workouts from January",
        "squats with high repetitions"
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        result = search_query_runner(query, "hybrid")
        print(f"Result: {result}")
        print("-" * 80)