#!/usr/bin/env python3
"""Test the dual-LLM approach for template generation."""

import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv('src/.env')

def test_dual_llm_template_generation():
    """Test using PromptFlow output + Azure OpenAI template generation."""
    
    print("🧪 Testing Dual-LLM Template Generation Approach")
    print("=" * 60)
    
    # Step 1: Simulate PromptFlow output (from your actual working system)
    sample_promptflow_output = {
        "status": "success",
        "question": "Create a monthly pushup report template for me",
        "enhanced_analysis": """### Analysis of Your Pushup Data

#### Total Pushups Completed:
You've performed 3,226 pushups! That's an incredible milestone that shows dedication and consistency in your upper body training.

#### Key Insights and Patterns:
- **Consistency**: Reaching over 3,000 pushups suggests strong commitment to integrating this exercise into your routine
- **Upper Body Strength**: Pushups engage chest, shoulders, triceps, and core - you're building comprehensive strength
- **Progressive Volume**: This total indicates you've been scaling up your volume consistently

#### Actionable Recommendations:
- **Introduce Variations**: Try diamond pushups, decline pushups, or explosive clap pushups for increased difficulty
- **Balance Training**: Complement pushups with pulling exercises like pull-ups or rows for muscle balance
- **Track Progress**: Set weekly or monthly goals to continue building on this foundation

#### Motivational Observations:
Every pushup contributes to your overall fitness and strength. This 3,226 total represents hours of dedication and hard work!""",
        "data_sources": {
            "sql_available": True,
            "search_available": True,
            "sql_results_count": 1,
            "search_results_count": 20
        }
    }
    
    print("📊 Step 1: PromptFlow Analysis (Current Working System)")
    print("User Request:", sample_promptflow_output["question"])
    print("Analysis Length:", len(sample_promptflow_output["enhanced_analysis"]), "characters")
    print("✅ PromptFlow provides rich workout data insights")
    print()
    
    # Step 2: Use Azure OpenAI with AZURE_OPENAI_TEMPLATE_SYSTEM_MESSAGE
    print("📝 Step 2: Template Structure Generation with Azure OpenAI")
    
    try:
        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        # Get template system message
        template_system_message = os.getenv("AZURE_OPENAI_TEMPLATE_SYSTEM_MESSAGE")
        print(f"Template System Message: {template_system_message[:100]}...")
        
        # Construct the template generation request
        template_request = f"""
User Request: {sample_promptflow_output["question"]}

Based on this workout data analysis:
{sample_promptflow_output["enhanced_analysis"]}

Create a structured document template that incorporates the specific data insights (like the 3,226 pushups total) into the section descriptions.
"""
        
        print("Sending template generation request...")
        
        # Call Azure OpenAI for template structure
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL"),
            messages=[
                {"role": "system", "content": template_system_message},
                {"role": "user", "content": template_request}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        template_response = response.choices[0].message.content
        print("✅ Template structure generated!")
        print()
        
        # Step 3: Show the results
        print("🎯 Step 3: Dual-LLM Results")
        print("=" * 40)
        print("TEMPLATE STRUCTURE:")
        print(template_response)
        print()
        
        # Try to parse as JSON (handle markdown code blocks)
        try:
            # Remove markdown code block markers if present
            json_content = template_response
            if "```json" in json_content:
                json_content = json_content.split("```json")[1].split("```")[0].strip()
            elif "```" in json_content:
                json_content = json_content.split("```")[1].split("```")[0].strip()
            
            template_json = json.loads(json_content)
            print("✅ SUCCESS: Valid JSON template structure!")
            print()
            print("📋 Template Sections:")
            if "template" in template_json:
                for i, section in enumerate(template_json["template"], 1):
                    print(f"{i}. {section.get('section_title', 'Untitled')}")
                    print(f"   Description: {section.get('section_description', 'No description')[:100]}...")
                    print()
            
            return True, template_json
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print("Raw response:", template_response[:200], "...")
            return False, template_response
            
    except Exception as e:
        print(f"❌ Azure OpenAI error: {e}")
        return False, str(e)

def test_integration_approach():
    """Show how this would integrate into the document generation backend."""
    
    print("\n" + "=" * 60)
    print("🔧 Integration Approach for Backend")
    print("=" * 60)
    
    integration_steps = [
        "1. Detect ChatType.TEMPLATE in conversation_internal()",
        "2. Call PromptFlow for workout data analysis (existing code)",
        "3. Extract PromptFlow insights from response",
        "4. Call Azure OpenAI with template system message + insights",
        "5. Parse template JSON and return to frontend",
        "6. Frontend renders template sections with data-driven content"
    ]
    
    for step in integration_steps:
        print(f"   {step}")
    
    print()
    print("🎯 Benefits of Dual-LLM Approach:")
    print("   ✅ PromptFlow unchanged (no deployment needed)")
    print("   ✅ Templates include real workout data")
    print("   ✅ Structured format for document generation")
    print("   ✅ Follows original Microsoft architecture")
    print("   ✅ Each step independently testable")

if __name__ == "__main__":
    # Test the dual-LLM approach
    success, result = test_dual_llm_template_generation()
    
    # Show integration plan
    test_integration_approach()
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    if success:
        print("✅ DUAL-LLM APPROACH WORKS!")
        print("✅ Ready to integrate into document generation backend")
        print("✅ Next step: Implement in conversation_internal() function")
    else:
        print("❌ Issues found - need to debug template generation")
        print("🔧 Check Azure OpenAI configuration and system message format")
    
    print("\n🚀 Ready to proceed with Option A implementation!")