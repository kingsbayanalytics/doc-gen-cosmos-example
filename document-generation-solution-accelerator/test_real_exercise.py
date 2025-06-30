#!/usr/bin/env python3
"""Test with exercises that actually exist in the data."""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')

def test_real_exercise():
    endpoint = os.getenv('PROMPTFLOW_ENDPOINT')
    api_key = os.getenv('PROMPTFLOW_API_KEY')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key
    }
    
    # Test with an exercise that exists in the data
    test_data = {
        "query": "When was the last time I did jumping jacks?",
        "use_search": True,
        "search_type": "hybrid"
    }
    
    print(f"Testing with real exercise: {test_data['query']}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ PromptFlow response received!")
            
            if 'answesr' in result:
                import json as json_lib
                try:
                    parsed = json_lib.loads(result['answesr'])
                    print(f"\nSQL Results Count: {parsed.get('data_sources', {}).get('sql_results_count', 'N/A')}")
                    print(f"Search Results Count: {parsed.get('data_sources', {}).get('search_results_count', 'N/A')}")
                    print(f"\nAnalysis: {parsed.get('enhanced_analysis', 'N/A')[:400]}...")
                except:
                    print(f"Raw response: {result['answesr'][:300]}...")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_real_exercise()