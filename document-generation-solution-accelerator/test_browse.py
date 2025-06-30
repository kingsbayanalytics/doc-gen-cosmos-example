#!/usr/bin/env python3
"""Test the browse interface to debug the error."""

import requests
import json

def test_browse_query():
    """Test a browse query to see what error occurs."""
    
    backend_url = "http://localhost:50505"
    endpoint = f"{backend_url}/conversation"
    
    # Simulate what the frontend sends
    test_data = {
        "messages": [
            {
                "role": "user", 
                "content": "When was the last time I did a pushup"
            }
        ],
        "chat_type": "browse"  # Browse mode for regular chat
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing browse query: {endpoint}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data, timeout=30)
        print(f"\nResponse Status: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_browse_query()