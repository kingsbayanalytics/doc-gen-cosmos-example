#!/usr/bin/env python3
"""Convert natural language questions to Cosmos DB SQL queries using Azure OpenAI."""

import os
from promptflow.core import tool
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load environment variables when running locally
load_dotenv()


@tool
def query_interpreter(question: str) -> str:
    """
    Convert natural language question to Cosmos DB SQL query.
    
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
    
    # System prompt with schema information
    system_prompt = """You are a SQL query generator for Azure Cosmos DB. 
    Convert natural language questions into valid Cosmos DB SQL queries.
    
    The workout data schema includes these fields:
    - id: string (unique identifier)
    - ﻿"ExDate": string (exercise date) - NOTE: Field has BOM prefix
    - ﻿"Exercise": string (exercise name) - NOTE: Field has BOM prefix  
    - ﻿"Set": number (set number) - NOTE: Field has BOM prefix
    - ﻿"Reps": number (repetitions) - NOTE: Field has BOM prefix
    - ﻿"Weight": number (weight used) - NOTE: Field has BOM prefix
    - ﻿"ExType": string (exercise type, e.g., "Strength", "Cardio") - NOTE: Field has BOM prefix
    
    Important Cosmos DB SQL notes:
    - Use SELECT * or SELECT specific fields FROM c
    - The collection alias is 'c'
    - Date comparisons should use string comparison
    - For counting records, use: SELECT VALUE COUNT(1) FROM c
    - For aggregations, use VALUE keyword: SELECT VALUE SUM(c.﻿"Weight") FROM c
    - All aggregate queries must use VALUE keyword
    - CRITICAL: Field names have BOM characters - use c.﻿"Exercise" NOT c.Exercise
    - CRITICAL: Use UPPER() for case-insensitive exercise name matching: WHERE UPPER(c.﻿"Exercise") = UPPER("exercise_name")
    
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