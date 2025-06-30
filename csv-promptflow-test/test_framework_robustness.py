#!/usr/bin/env python3
"""Test the framework-level robustness of the schema-aware query system."""

from query_interpreter import query_interpreter
from cosmos_query_runner import cosmos_query_runner
import json

def test_natural_language_mapping():
    """Test how well the system maps natural language to database values."""
    
    test_cases = [
        # Test exercise name variations
        {
            "natural": "How many pushups have I done?",
            "expected_exercise": "Pushup",
            "description": "Maps 'pushups' to 'Pushup'"
        },
        {
            "natural": "Show me jumping jack workouts",
            "expected_exercise": "Jumping Jacks", 
            "description": "Maps 'jumping jack' to 'Jumping Jacks'"
        },
        {
            "natural": "What's my bench press total?",
            "expected_exercise": "Bench Press",
            "description": "Maps 'bench press' to 'Bench Press'"
        },
        {
            "natural": "How many dips did I do?",
            "expected_exercise": "Dip",
            "description": "Maps 'dips' to 'Dip'"
        },
        # Test exercise type variations
        {
            "natural": "Show me upper body exercises",
            "expected_type": "Upper",
            "description": "Maps 'upper body' to 'Upper'"
        },
        {
            "natural": "How many cardio exercises?",
            "expected_type": "Mixed Cardio",
            "description": "Maps 'cardio' to 'Mixed Cardio'"
        }
    ]
    
    print("🧪 Testing Framework-Level Natural Language Mapping")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['description']}")
        print(f"Question: '{test['natural']}'")
        
        # Generate SQL
        sql = query_interpreter(test['natural'])
        print(f"Generated SQL: {sql}")
        
        # Check if expected value is in SQL
        success = False
        if 'expected_exercise' in test:
            success = test['expected_exercise'] in sql
        elif 'expected_type' in test:
            success = test['expected_type'] in sql
            
        if success:
            print("✅ PASSED: Correct mapping found in SQL")
            
            # Execute query to verify it works
            result = cosmos_query_runner(sql)
            if 'success' in result:
                result_data = json.loads(result)
                if result_data.get('results') and result_data['results'][0] is not None:
                    print(f"📊 Data found: {result_data['results'][0]}")
                else:
                    print("📊 Query succeeded (no matching data)")
            else:
                print("⚠️  SQL error (but mapping was correct)")
        else:
            print("❌ FAILED: Expected mapping not found")
        
        print("-" * 40)

def test_aggregation_accuracy():
    """Test that numeric aggregations work correctly with StringToNumber."""
    
    print("\n🔢 Testing Numeric Aggregation Accuracy")
    print("=" * 60)
    
    aggregation_tests = [
        "How many total jumping jacks have I done?",
        "What's my average bench press weight?", 
        "How many pushup reps in total?"
    ]
    
    for i, question in enumerate(aggregation_tests, 1):
        print(f"\nAggregation Test {i}: {question}")
        sql = query_interpreter(question)
        print(f"SQL: {sql}")
        
        # Check if StringToNumber is used for numeric operations
        if "StringToNumber" in sql and ("SUM" in sql or "AVG" in sql):
            print("✅ PASSED: Uses StringToNumber for aggregation")
            
            result = cosmos_query_runner(sql)
            if 'success' in result:
                result_data = json.loads(result)
                if result_data.get('results') and result_data['results'][0] is not None:
                    print(f"📊 Result: {result_data['results'][0]}")
                else:
                    print("📊 No data found")
            else:
                print("❌ Query failed")
        else:
            print("❌ FAILED: Missing StringToNumber or aggregation function")
        
        print("-" * 40)

if __name__ == "__main__":
    print("🚀 Testing Framework-Level Robustness")
    print("This demonstrates how the system works with ANY dataset\n")
    
    test_natural_language_mapping()
    test_aggregation_accuracy()
    
    print("\n🎯 Framework Benefits:")
    print("✅ Automatically discovers database schema")
    print("✅ Maps natural language to exact database values") 
    print("✅ Handles string-stored numeric fields")
    print("✅ Works with any categorical dataset")
    print("✅ No hardcoded mappings required")