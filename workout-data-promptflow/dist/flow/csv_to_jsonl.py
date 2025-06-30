#!/usr/bin/env python3
"""Convert CSV workout data to JSONL format for Cosmos DB ingestion."""

import csv
import json
import sys
from pathlib import Path


def csv_to_jsonl(csv_file_path, jsonl_file_path):
    """
    Convert CSV file to JSONL format with unique IDs.
    
    Args:
        csv_file_path: Path to input CSV file
        jsonl_file_path: Path to output JSONL file
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
                for idx, row in enumerate(csv_reader, 1):
                    # Add unique ID field
                    row['id'] = f"entry_{idx}"
                    
                    # Clean up field names (remove any extra spaces)
                    cleaned_row = {key.strip(): value.strip() if value else value 
                                   for key, value in row.items()}
                    
                    # Write as JSON line
                    jsonl_file.write(json.dumps(cleaned_row) + '\n')
        
        print(f"Successfully converted {csv_file_path} to {jsonl_file_path}")
        print(f"Total records: {idx}")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_jsonl.py <input.csv> <output.jsonl>")
        print("Example: python csv_to_jsonl.py 'Workout Entries SP.csv' workout_entries_cosmos.jsonl")
        sys.exit(1)
    
    csv_to_jsonl(sys.argv[1], sys.argv[2])