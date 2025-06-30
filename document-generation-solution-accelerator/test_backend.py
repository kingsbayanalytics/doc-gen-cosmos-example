#!/usr/bin/env python3
"""Test the document generation backend with PromptFlow integration."""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

def test_conversation_endpoint():
    """Test the /conversation endpoint with workout data query."""
    
    backend_url = "http://localhost:50505"
    endpoint = f"{backend_url}/conversation"
    
    # Test data - asking about workout information
    test_data = {
        "messages": [
            {
                "role": "user", 
                "content": "How many workouts did I do this week? Can you generate a weekly workout summary?"
            }
        ],
        "chat_type": "browse",  # Required: either "browse" or "template"
        "promptflow_request": {
            "query": "How many workouts did I do this week?",
            "use_search": True,
            "search_type": "hybrid"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing backend endpoint: {endpoint}")
    print(f"Request data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=test_data)
        print(f"\nResponse Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend endpoint is working!")
            try:
                response_data = response.json()
                print(f"Response preview: {json.dumps(response_data, indent=2)[:500]}...")
            except:
                print(f"Response text: {response.text[:500]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_frontend_settings():
    """Test the /frontend_settings endpoint."""
    
    backend_url = "http://localhost:50505"
    endpoint = f"{backend_url}/frontend_settings"
    
    print(f"\nTesting frontend settings: {endpoint}")
    
    try:
        response = requests.get(endpoint)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Frontend settings endpoint working!")
            settings = response.json()
            print(f"UI Title: {settings.get('ui', {}).get('title')}")
            print(f"Auth Enabled: {settings.get('auth_enabled')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🏋️ Testing Document Generation Backend Integration\n")
    
    # Test basic connectivity
    test_frontend_settings()
    
    # Test conversation endpoint with workout data
    test_conversation_endpoint()