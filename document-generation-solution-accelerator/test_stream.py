#!/usr/bin/env python3
"""Test streaming response to debug frontend issues."""

import requests
import json

def test_streaming_response():
    """Test streaming response format."""
    
    backend_url = "http://localhost:50505"
    endpoint = f"{backend_url}/conversation"
    
    test_data = {
        "messages": [
            {
                "role": "user", 
                "content": "When was the last time I worked out?"
            }
        ],
        "chat_type": "browse"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing streaming response: {endpoint}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data, stream=True, timeout=30)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("\nStreaming response chunks:")
            chunk_count = 0
            for chunk in response.iter_lines():
                if chunk:
                    chunk_count += 1
                    try:
                        chunk_data = json.loads(chunk.decode('utf-8'))
                        print(f"Chunk {chunk_count}: {json.dumps(chunk_data, indent=2)}")
                    except json.JSONDecodeError:
                        print(f"Chunk {chunk_count} (raw): {chunk.decode('utf-8')}")
            
            print(f"\nTotal chunks received: {chunk_count}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_streaming_response()