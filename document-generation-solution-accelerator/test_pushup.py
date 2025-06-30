#!/usr/bin/env python3
"""Test specific pushup query to see if we get actual data."""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

def test_pushup_query():
    endpoint = os.getenv('PROMPTFLOW_ENDPOINT')
    api_key = os.getenv('PROMPTFLOW_API_KEY')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key
    }
    
    # Test with specific pushup query
    test_data = {
        "query": "Show me all pushup exercises from my workout data",
        "use_search": True,
        "search_type": "hybrid"
    }
    
    print(f"Testing pushup-specific query...")
    print(f"Query: {test_data['query']}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ PromptFlow response received!")
            
            # Parse the response to see what data we got
            if 'answesr' in result:
                import json as json_lib
                try:
                    parsed = json_lib.loads(result['answesr'])
                    print(f"\nSQL Results Count: {parsed.get('data_sources', {}).get('sql_results_count', 'N/A')}")
                    print(f"Search Results Count: {parsed.get('data_sources', {}).get('search_results_count', 'N/A')}")
                    print(f"\nAnalysis Preview: {parsed.get('enhanced_analysis', 'N/A')[:200]}...")
                except:
                    print(f"Response: {result['answesr'][:300]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pushup_query()