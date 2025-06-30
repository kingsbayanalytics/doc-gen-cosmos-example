#!/usr/bin/env python3
"""Convert natural language questions to Cosmos DB SQL queries using Azure OpenAI."""

import os
import json
from promptflow.core import tool
from openai import AzureOpenAI
from dotenv import load_dotenv
from schema_discovery import discover_schema


# Load environment variables when running locally
load_dotenv()


@tool
def query_interpreter(question: str) -> str:
    """
    Convert natural language question to Cosmos DB SQL query using dynamic schema discovery.
    
    Args:
        question: Natural language question about workout data
        
    Returns:
        SQL query string for Cosmos DB
    """
    # Initialize Azure OpenAI client with environment variables
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    
    # Discover schema dynamically
    schema = discover_schema()
    
    # Build dynamic system prompt with actual categorical values
    if schema and "categorical_values" in schema:
        exercise_values = schema["categorical_values"].get("Exercise", [])
        extype_values = schema["categorical_values"].get("ExType", [])
        
        exercise_list = ", ".join(f'"{ex}"' for ex in exercise_values[:20])  # Limit to first 20
        extype_list = ", ".join(f'"{et}"' for et in extype_values)
        
        system_prompt = f"""You are a SQL query generator for Azure Cosmos DB. 
Convert natural language questions into valid Cosmos DB SQL queries.

The database schema includes these fields:
- id: string (unique identifier)
- Exercise: string (exercise name)
- Set: string (set number stored as string)
- Reps: string (repetitions stored as string)
- Weight: string (weight used stored as string)
- ExType: string (exercise type)

ACTUAL EXERCISE NAMES IN DATABASE: {exercise_list}
ACTUAL EXERCISE TYPES IN DATABASE: {extype_list}

CRITICAL: Use EXACT exercise names from the database! 
- For "pushups" use "Pushup"
- For "jumping jacks" use "Jumping Jacks"
- For "bench press" use "Bench Press"
- Always match the exact capitalization and spelling from the database

CRITICAL: Numeric fields (Reps, Weight, Set) are stored as strings! 
- For counting: Use StringToNumber(c.Reps) or VALUE COUNT(1)
- For summing: SELECT VALUE SUM(StringToNumber(c.Reps)) FROM c
- For averaging: SELECT VALUE AVG(StringToNumber(c.Weight)) FROM c

Important Cosmos DB SQL notes:
- Use SELECT * or SELECT specific fields FROM c
- The collection alias is 'c'
- For counting records, use: SELECT VALUE COUNT(1) FROM c
- For aggregations with numeric fields, use StringToNumber: SELECT VALUE SUM(StringToNumber(c.Reps))
- All aggregate queries must use VALUE keyword
- CRITICAL: DO NOT use ORDER BY clauses - they cause syntax errors
- CRITICAL: Use TOP N instead of LIMIT for restricting results
- CRITICAL: Use exact case-sensitive exercise name matching: WHERE c.Exercise = "ExactName"
- For recent data, use TOP N without ORDER BY - let the client sort results

Return ONLY the SQL query without any explanation or markdown formatting."""
    else:
        # Fallback system prompt if schema discovery fails
        system_prompt = """You are a SQL query generator for Azure Cosmos DB. 
Convert natural language questions into valid Cosmos DB SQL queries.

The database schema includes fields like Exercise, Set, Reps, Weight, ExType.
CRITICAL: Use StringToNumber() for numeric operations on string fields.
Use exact case-sensitive matching for exercise names.

Return ONLY the SQL query without any explanation or markdown formatting."""
    
    # Create the query
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Convert this question to a Cosmos DB SQL query: {question}"}
        ],
        temperature=0.1,
        max_tokens=200
    )
    
    sql_query = response.choices[0].message.content.strip()
    
    # Remove any markdown code blocks if present
    if sql_query.startswith("```"):
        sql_query = sql_query.split("\n", 1)[1].rsplit("\n", 1)[0]
    
    return sql_query


# For local testing
if __name__ == "__main__":
    test_questions = [
        "How many sets of strength exercises did I do last week?",
        "What was my average weight for bench press?",
        "Show me all exercises from January 2024"
    ]
    
    for q in test_questions:
        print(f"Question: {q}")
        print(f"SQL: {query_interpreter(q)}")
        print("-" * 50)