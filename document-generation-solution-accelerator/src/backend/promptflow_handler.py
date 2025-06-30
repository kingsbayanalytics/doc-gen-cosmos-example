"""PromptFlow integration handler for workout data analysis."""

import json
import logging
import os
import requests
from typing import Dict, Any, Optional


class PromptFlowHandler:
    """Handles integration with PromptFlow for workout data analysis."""
    
    def __init__(self):
        self.endpoint = os.getenv('PROMPTFLOW_ENDPOINT')
        self.api_key = os.getenv('PROMPTFLOW_API_KEY')
        self.timeout = float(os.getenv('PROMPTFLOW_RESPONSE_TIMEOUT', '120'))
        
        # Field mappings
        self.query_field = os.getenv('PROMPTFLOW_QUERY_FIELD', 'query')
        self.use_search_field = os.getenv('PROMPTFLOW_USE_SEARCH_FIELD', 'use_search')
        self.search_type_field = os.getenv('PROMPTFLOW_SEARCH_TYPE_FIELD', 'search_type')
        
        # Response field mappings
        self.enhanced_result_field = os.getenv('PROMPTFLOW_ENHANCED_RESULT_FIELD', 'enhanced_result')
        self.sql_result_field = os.getenv('PROMPTFLOW_SQL_RESULT_FIELD', 'sql_result')
        self.search_result_field = os.getenv('PROMPTFLOW_SEARCH_RESULT_FIELD', 'search_result')
    
    def is_available(self) -> bool:
        """Check if PromptFlow is configured and available."""
        print(f"[DEBUG] PromptFlow availability check - endpoint: {self.endpoint}, api_key: {self.api_key[:10] if self.api_key else None}...")
        # For local development, just check if endpoint is set
        if self.endpoint and '127.0.0.1' in self.endpoint:
            print(f"[DEBUG] Local PromptFlow detected, available: {bool(self.endpoint)}")
            return bool(self.endpoint)
        # For Azure deployment, need both endpoint and API key
        result = bool(self.endpoint and self.api_key)
        print(f"[DEBUG] Azure PromptFlow check, available: {result}")
        return result
    
    def call_promptflow(self, query: str, use_search: bool = True, search_type: str = "hybrid") -> Dict[str, Any]:
        """Call the PromptFlow endpoint with workout data query."""
        
        if not self.is_available():
            raise Exception("PromptFlow is not configured. Missing PROMPTFLOW_ENDPOINT or PROMPTFLOW_API_KEY")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add authentication headers only for Azure deployment
        if self.api_key and self.api_key != 'dummy_local_key':
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["api-key"] = self.api_key
        
        # Prepare request data for AI Foundry PromptFlow endpoint
        request_data = {
            self.query_field: query,
            self.use_search_field: use_search,
            self.search_type_field: search_type
        }
        
        logging.info(f"Calling PromptFlow endpoint: {self.endpoint}")
        logging.debug(f"Request data: {json.dumps(request_data, indent=2)}")
        
        try:
            response = requests.post(
                self.endpoint, 
                headers=headers, 
                json=request_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logging.info("PromptFlow call successful")
                logging.debug(f"Response: {json.dumps(result, indent=2)}")
                return result
            else:
                error_msg = f"PromptFlow endpoint error: {response.status_code} - {response.text}"
                logging.error(error_msg)
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"PromptFlow connection error: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)
    
    def format_response_for_chat(self, promptflow_result: Dict[str, Any], user_message: str) -> Dict[str, Any]:
        """Format PromptFlow response for the chat interface."""
        
        # Try to extract the main result - the response format may vary
        content = ""
        
        # Check for different possible response field names
        raw_content = ""
        if 'answesr' in promptflow_result:  # Note: there's a typo in the actual response
            raw_content = promptflow_result['answesr']
        elif self.enhanced_result_field in promptflow_result:
            raw_content = promptflow_result[self.enhanced_result_field]
        elif 'answer' in promptflow_result:
            raw_content = promptflow_result['answer']
        elif 'result' in promptflow_result:
            raw_content = promptflow_result['result']
        else:
            # If no specific field found, use the whole response as string
            raw_content = json.dumps(promptflow_result, indent=2)
        
        # Try to parse the JSON content and extract the enhanced_analysis
        try:
            if isinstance(raw_content, str):
                parsed_content = json.loads(raw_content)
                if 'enhanced_analysis' in parsed_content:
                    content = parsed_content['enhanced_analysis']
                else:
                    content = raw_content
            else:
                content = str(raw_content)
        except json.JSONDecodeError:
            # If it's not JSON, use the raw content
            content = str(raw_content)
        
        # Format as a chat completion response
        formatted_response = {
            "id": "promptflow-response",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": content
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(str(content).split()),
                "total_tokens": len(user_message.split()) + len(str(content).split())
            },
            "promptflow_data": promptflow_result  # Include original data for debugging
        }
        
        return formatted_response


# Global instance
promptflow_handler = PromptFlowHandler()