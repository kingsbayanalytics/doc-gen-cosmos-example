#!/usr/bin/env python3
"""Test script for deployed PromptFlow endpoint from AI Foundry."""

import requests
import json

# Replace with your actual AI Foundry endpoint details
ENDPOINT_URL = "https://<your-project>.<region>.inference.ai.azure.com/score"
API_KEY = "<your-api-key>"

def test_endpoint():
    """Test the deployed PromptFlow endpoint."""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        # AI Foundry might use different auth header
        "api-key": API_KEY
    }
    
    # Test data matching your PromptFlow input schema
    # This should match exactly what your flow.dag.yaml expects
    test_data = {
        "query": "How many total workout entries do I have?",
        "use_search": True,
        "search_type": "hybrid"
    }
    
    try:
        print(f"Testing endpoint: {ENDPOINT_URL}")
        print(f"Sending data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(ENDPOINT_URL, headers=headers, json=test_data)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Endpoint test successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            # Show the fields we need for document generation
            if "enhanced_result" in result:
                print("\n🎯 Enhanced result found - perfect for document generation!")
            if "sql_result" in result:
                print("📊 SQL result found - great for structured data!")
            if "search_result" in result:
                print("🔍 Search result found - excellent for context!")
            
            return True
        else:
            print(f"❌ Endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Endpoint test failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return False

if __name__ == "__main__":
    print("Testing deployed PromptFlow endpoint from AI Foundry...")
    print("\n⚠️  Make sure to update ENDPOINT_URL and API_KEY before running!")
    print("Find these in AI Foundry Studio → Your Project → Deployments → Your Endpoint → Consume tab\n")
    
    # Uncomment this when you have the real values
    # test_endpoint()