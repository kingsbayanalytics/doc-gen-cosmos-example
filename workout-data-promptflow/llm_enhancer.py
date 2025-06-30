#!/usr/bin/env python3
"""LLM node to enhance and analyze query results with insights and summaries."""

import os
import json
from promptflow.core import tool
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@tool
def llm_enhancer(question: str, sql_results: str, search_results: str = None) -> str:
    """
    Enhance query results with LLM-powered analysis, insights, and natural language summaries.
    
    Args:
        question: Original user question
        sql_results: Results from SQL query against Cosmos DB
        search_results: Optional results from Azure AI Search
        
    Returns:
        Enhanced analysis with insights, summaries, and recommendations
    """
    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
        
        # Parse the input data
        try:
            sql_data = json.loads(sql_results) if sql_results else None
        except:
            sql_data = {"raw": sql_results}
            
        try:
            search_data = json.loads(search_results) if search_results else None
        except:
            search_data = None
        
        # Create enhanced system prompt
        system_prompt = """You are a fitness data analyst AI that provides insightful analysis of workout data.
        
        Your role is to:
        1. Analyze the provided workout data and results
        2. Provide clear, actionable insights about fitness patterns and trends
        3. Offer personalized recommendations based on the data
        4. Present information in a friendly, motivational way
        5. Identify interesting patterns, achievements, or areas for improvement
        
        When analyzing workout data, consider:
        - Progress over time (strength gains, volume increases)
        - Exercise variety and muscle group balance
        - Frequency and consistency patterns
        - Performance metrics and personal records
        - Training volume and intensity
        
        Always be encouraging and focus on helping the user improve their fitness journey."""
        
        # Build the user message with context
        user_message_parts = [
            f"User Question: {question}",
            "\n--- SQL Query Results ---"
        ]
        
        if sql_data:
            if sql_data.get("status") == "success":
                user_message_parts.append(f"Query returned {sql_data.get('count', 0)} results")
                if sql_data.get("results"):
                    user_message_parts.append("Data:")
                    user_message_parts.append(json.dumps(sql_data["results"], indent=2))
                elif sql_data.get("value") is not None:
                    user_message_parts.append(f"Result: {sql_data['value']}")
            else:
                user_message_parts.append(f"SQL Error: {sql_data.get('message', 'Unknown error')}")
        
        if search_data and search_data.get("status") == "success":
            user_message_parts.append("\n--- Search Results ---")
            user_message_parts.append(f"Found {search_data.get('returned_count', 0)} relevant entries")
            if search_data.get("results"):
                # Summarize search results more concisely
                exercises = [r.get("exercise") for r in search_data["results"][:5] if r.get("exercise")]
                if exercises:
                    user_message_parts.append(f"Top exercises: {', '.join(set(exercises))}")
        
        user_message_parts.append("\nPlease provide an insightful analysis with:")
        user_message_parts.append("1. A clear answer to the user's question")
        user_message_parts.append("2. Key insights and patterns from the data")
        user_message_parts.append("3. Actionable recommendations for improvement")
        user_message_parts.append("4. Motivational observations about their progress")
        
        user_message = "\n".join(user_message_parts)
        
        # Generate enhanced response
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        enhanced_analysis = response.choices[0].message.content.strip()
        
        # Structure the final response
        final_response = {
            "status": "success",
            "question": question,
            "enhanced_analysis": enhanced_analysis,
            "data_sources": {
                "sql_available": sql_data is not None,
                "search_available": search_data is not None,
                "sql_results_count": sql_data.get("count") if sql_data else 0,
                "search_results_count": search_data.get("returned_count") if search_data else 0
            }
        }
        
        return json.dumps(final_response, indent=2)
        
    except Exception as e:
        error_message = f"Error in LLM enhancement: {str(e)}"
        print(error_message)
        
        return json.dumps({
            "status": "error",
            "message": error_message,
            "question": question,
            "fallback_analysis": "Unable to provide enhanced analysis due to technical issues. Please review the raw data results."
        }, indent=2)


# For local testing
if __name__ == "__main__":
    test_sql_result = json.dumps({
        "status": "success",
        "count": 1,
        "results": [25]
    })
    
    test_question = "How many bench press sets did I do?"
    
    result = llm_enhancer(test_question, test_sql_result)
    print(f"Enhanced Result: {result}")