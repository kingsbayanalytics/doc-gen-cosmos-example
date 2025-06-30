# CSV Prompt Flow Test

This directory contains the implementation for natural language querying of workout data using Azure Prompt Flow and Cosmos DB.

## Quick Start

1. Copy `.env.template` to `.env` and fill in your Azure credentials
2. Convert your CSV data: `python csv_to_jsonl.py "Workout Entries SP.csv" workout_entries_cosmos.jsonl`
3. Upload to Cosmos DB: `python load_csv_to_cosmos.py`
4. Run a query: `pf run --flow . --inputs query="How many sets did I do last week?"`

## Files

- `csv_to_jsonl.py` - Converts CSV workout data to JSONL format
- `load_csv_to_cosmos.py` - Uploads JSONL data to Azure Cosmos DB
- `flow.dag.yaml` - Prompt Flow DAG definition
- `query_interpreter.py` - Converts natural language to SQL using GPT-4o
- `cosmos_query_runner.py` - Executes SQL queries against Cosmos DB

## Example Queries

- "How many strength exercises did I do last week?"
- "What's my average weight for bench press?"
- "Show me all cardio exercises from January"
- "How many total sets did I complete this month?"