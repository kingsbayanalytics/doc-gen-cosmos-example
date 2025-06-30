#!/usr/bin/env python3
"""Quick test of PromptFlow endpoint before starting the app."""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

def test_promptflow():
    endpoint = os.getenv('PROMPTFLOW_ENDPOINT')
    api_key = os.getenv('PROMPTFLOW_API_KEY')
    
    if not endpoint or not api_key:
        print("❌ Missing PROMPTFLOW_ENDPOINT or PROMPTFLOW_API_KEY in .env")
        return False
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key
    }
    
    test_data = {
        "query": "How many workouts did I do this week?",
        "use_search": True,
        "search_type": "hybrid"
    }
    
    print(f"Testing endpoint: {endpoint}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data)
        if response.status_code == 200:
            print("✅ PromptFlow endpoint is working!")
            print(f"Response preview: {json.dumps(response.json(), indent=2)[:200]}...")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_promptflow()