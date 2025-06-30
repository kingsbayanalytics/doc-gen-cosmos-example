# Enhanced PromptFlow SQL - Intelligent Workout Data Analysis System

A comprehensive Microsoft Prompt Flow application that combines natural language processing, structured SQL queries, semantic search, and AI-powered analysis to provide intelligent insights from your workout data. Ask questions in plain English and receive personalized, actionable fitness guidance.

## 🎯 Overview

This enhanced system demonstrates how to:
- Convert CSV workout data to Azure Cosmos DB and Azure AI Search
- Build a multi-modal Prompt Flow pipeline combining SQL precision with semantic search
- Generate vector embeddings for semantic workout data discovery
- Provide AI-powered analysis, insights, and personalized recommendations
- Create a flexible query system that adapts to different types of fitness questions

## 🏗️ Enhanced Architecture

```
User Question 
    ↓
┌─────────────────────────────────────────────────────────┐
│                 Prompt Flow Pipeline                    │
├─────────────────────────────────────────────────────────┤
│ 1. Query Interpreter (GPT-4o)                          │
│    ├─ Natural Language → SQL Query                     │
│    └─ Schema-aware query generation                    │
│                                                         │
│ 2. Dual Data Retrieval (Parallel)                      │
│    ├─ Cosmos DB SQL Query ── Structured Data           │
│    └─ AI Search Vector/Semantic ── Related Content     │
│                                                         │
│ 3. LLM Enhancer (GPT-4o)                              │
│    ├─ Intelligent Analysis & Insights                  │
│    ├─ Personalized Recommendations                     │
│    ├─ Progress Tracking & Motivation                   │
│    └─ Actionable Fitness Guidance                      │
└─────────────────────────────────────────────────────────┘
    ↓
Enhanced Response with Insights & Recommendations
```

The system uses a four-node Prompt Flow:
1. **Query Interpreter**: Converts natural language to Cosmos DB SQL using GPT-4o
2. **Cosmos Query Runner**: Executes SQL queries for precise structured data
3. **Search Query Runner**: Performs semantic/vector search for contextual discovery
4. **LLM Enhancer**: Analyzes results and provides intelligent insights and recommendations

## 📋 Prerequisites

- Python 3.10+
- Azure Cosmos DB account
- Azure AI Search service
- Azure OpenAI resource with:
  - GPT-4o deployment for chat/analysis
  - text-embedding-3-large deployment for vector embeddings
- Conda (recommended) or virtual environment

## 🚀 Quick Start

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd promptflow-sql

# Create conda environment
conda create -n promptflow-sql python=3.10 -y
conda activate promptflow-sql

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Azure Credentials

Copy `.env.template` to `csv-promptflow-test/.env` and fill in your Azure credentials:

```bash
cp .env.template csv-promptflow-test/.env
cd csv-promptflow-test
# Edit .env with your credentials
```

Required environment variables:
```bash
# Azure Cosmos DB
COSMOS_URI=https://your-cosmos.documents.azure.com:443/
COSMOS_KEY=your-primary-key
COSMOS_DB=sql-test
COSMOS_CONTAINER=sql-test

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-openai-key
AZURE_OPENAI_ENDPOINT=https://your-openai.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o-deployment-name
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_ADMIN_KEY=your-search-key
AZURE_SEARCH_INDEX_NAME=workout-entries-index
```

### 3. Load Data to Cosmos DB

```bash
# Convert CSV to JSONL format
python csv_to_jsonl.py "Workout Entries SP.csv" workout_entries_cosmos.jsonl

# Upload to Cosmos DB
python load_csv_to_cosmos.py
```

### 4. Set Up Azure AI Search Index

```bash
# Create the search index with vector capabilities
python create_search_index.py

# Populate with embeddings and data (takes ~10-15 minutes for large datasets)
python populate_search_index.py
```

### 5. Run Enhanced Natural Language Queries

```bash
# Enhanced analysis with both SQL and search
pf flow test --flow . --inputs query="How am I progressing with my bench press?" use_search=true

# SQL-only analysis (faster)
pf flow test --flow . --inputs query="How many workout entries do I have?" use_search=false

# Semantic search focused
pf flow test --flow . --inputs query="Find my most challenging cardio workouts" use_search=true search_type="semantic"
```

## 📊 Data Schema

The workout data includes these fields:
- `id`: Unique identifier
- `ExDate`: Exercise date
- `Exercise`: Exercise name
- `Set`: Set number
- `Reps`: Number of repetitions
- `Weight`: Weight used
- `ExType`: Exercise type (Strength, Cardio, etc.)

## 🛠️ Enhanced Project Structure

```
promptflow-sql/
├── README.md                       # This file
├── CLAUDE.md                      # Development guidance
├── requirements.txt               # Python dependencies
├── .env.template                  # Environment variable template
└── csv-promptflow-test/          # Main application
    ├── flow.dag.yaml             # Enhanced 4-node Prompt Flow definition
    ├── csv_to_jsonl.py           # CSV to JSONL converter
    ├── load_csv_to_cosmos.py     # Cosmos DB uploader
    ├── create_search_index.py    # Azure AI Search index creator
    ├── populate_search_index.py  # Embedding generator and index populator
    ├── delete_search_index.py    # Index management utility
    ├── query_interpreter.py      # Natural language to SQL converter
    ├── cosmos_query_runner.py    # SQL execution engine
    ├── search_query_runner.py    # Semantic/vector search engine
    └── llm_enhancer.py           # AI-powered analysis and insights generator
```

## 💡 Enhanced Query Examples

### 📊 Analytical Queries (SQL-focused)
- **Counting**: "How many sets of bench press did I do?"
- **Aggregation**: "What's my total volume for deadlifts?"
- **Progress**: "How has my squat weight progressed over time?"
- **Frequency**: "What are my 5 most frequent exercises?"

### 🔍 Discovery Queries (Search-focused)
- **Semantic**: "Find my most challenging upper body workouts"
- **Similar**: "Show me workouts similar to heavy lifting sessions"
- **Contextual**: "What exercises did I do when focusing on core strength?"

### 🤖 Enhanced Analysis (Full System)
- **Insights**: "How am I progressing with my bench press?" 
- **Recommendations**: "What should I focus on to improve my fitness?"
- **Patterns**: "What trends do you see in my workout consistency?"
- **Motivation**: "Celebrate my biggest fitness achievements!"

### ⚙️ Query Configuration Examples
```bash
# Pure SQL analysis (fastest)
pf flow test --flow . --inputs query="Count my deadlift sets" use_search=false

# Hybrid approach (SQL + semantic search)
pf flow test --flow . --inputs query="Analyze my leg day performance" use_search=true search_type="hybrid"

# Vector similarity search
pf flow test --flow . --inputs query="Find workouts like my best sessions" use_search=true search_type="vector"

# Semantic understanding focus
pf flow test --flow . --inputs query="When did I feel strongest?" use_search=true search_type="semantic"
```

## 🔧 Advanced Usage

### Running as a Service

```bash
# Start Prompt Flow service
pf service start

# Run queries via API with full configuration
pf run --flow . --inputs query="Analyze my fitness progress" use_search=true search_type="hybrid"

# Stop service
pf service stop
```

### Query Modes & Performance

| Mode | Speed | Capabilities | Best For |
|------|-------|-------------|----------|
| **SQL Only** | ⚡ Fastest | Precise structured queries | Counting, aggregation, filtering |
| **Search Only** | 🔍 Fast | Semantic discovery, similarity | Finding patterns, related content |
| **Hybrid** | 🤖 Comprehensive | Combined precision + discovery | Complex analysis, recommendations |

### Search Types Explained

- **`semantic`**: Uses Azure AI Search's semantic ranking for natural language understanding
- **`vector`**: Pure vector similarity search using embeddings
- **`hybrid`**: Combines keyword, semantic, and vector search for best results
- **`keyword`**: Traditional text-based search

### Customizing for Different Data Types

To adapt this system for other domains:

1. **Update Data Schema** (`csv_to_jsonl.py`):
   ```python
   # Modify field mappings for your data structure
   # Example: sales data, medical records, etc.
   ```

2. **Adjust Query Interpreter** (`query_interpreter.py`):
   ```python
   # Update the system prompt with your domain's schema
   # Include field descriptions and query patterns
   ```

3. **Customize Search Index** (`create_search_index.py`):
   ```python
   # Modify fields and search configurations
   # Adjust semantic configurations for your domain
   ```

4. **Enhance LLM Analysis** (`llm_enhancer.py`):
   ```python
   # Update the system prompt for domain-specific insights
   # Add relevant analysis patterns and recommendations
   ```

## 🎯 How the LLM Enhancement Works

The LLM Enhancer transforms raw data into actionable insights:

### Input Processing
- Receives SQL query results (structured data)
- Receives search results (semantic context)
- Analyzes user's original question for intent

### Intelligence Layer
- **Pattern Recognition**: Identifies trends and correlations
- **Contextual Analysis**: Understands fitness domain specifics
- **Personalization**: Tailors advice to user's data patterns
- **Motivation**: Provides encouraging and supportive feedback

### Enhanced Output Examples

**Raw SQL**: `2109`

**Enhanced Analysis**:
> You have an impressive **2,109 total workout entries**! This shows incredible dedication to your fitness journey.
>
> **Key Insights**: Your consistency is remarkable - logging over 2,000 workouts indicates long-term commitment...
>
> **Recommendations**: Consider setting new challenges like increasing intensity or adding exercise variety...
>
> **Motivation**: Every workout logged contributes to your transformation. Keep pushing forward! 💪

## 🐛 Troubleshooting

**Issue: "Query contains features client doesn't support"**
- Solution: Ensure all aggregate queries use the VALUE keyword (e.g., `SELECT VALUE COUNT(1) FROM c`)

**Issue: "Vector dimensions mismatch"**
- Solution: Recreate the search index with correct dimensions (3072 for text-embedding-3-large)
```bash
python delete_search_index.py
python create_search_index.py
```

**Issue: OpenAI connection errors**
- Solution: Verify your Azure OpenAI endpoint and API key in `.env`

**Issue: Search index population fails**
- Solution: Check rate limits on embedding API; the script includes delays to handle this

**Issue: No search results returned**
- Solution: Ensure the search index is fully populated and your search service has sufficient capacity

**Issue: LLM enhancer provides generic responses**
- Solution: Verify both SQL and search data are being passed correctly to the enhancer node

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Resources

- [Azure Prompt Flow Documentation](https://microsoft.github.io/promptflow/)
- [Azure Cosmos DB SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/)
- [Azure AI Search Documentation](https://docs.microsoft.com/en-us/azure/search/)
- [Vector Search in Azure AI Search](https://docs.microsoft.com/en-us/azure/search/vector-search-overview)

## 🏆 Key Benefits

### For Fitness Enthusiasts
- **Intelligent Analysis**: Get personalized insights from your workout data
- **Natural Language**: Ask questions in plain English, no SQL knowledge required
- **Motivational Feedback**: Receive encouraging analysis of your progress
- **Pattern Discovery**: Uncover trends and patterns you might miss

### For Developers
- **Multi-Modal Architecture**: Combines SQL precision with semantic search flexibility
- **Extensible Design**: Easy to adapt for other data domains beyond fitness
- **Modern AI Stack**: Demonstrates integration of Cosmos DB, AI Search, and OpenAI
- **Production Ready**: Includes error handling, rate limiting, and proper configuration

### For Data Scientists
- **Hybrid Query Approach**: SQL for precision, vector search for discovery
- **Embedding Integration**: Shows practical use of text-embedding-3-large
- **LLM Enhancement**: Demonstrates how to add intelligence layers to raw data
- **Semantic Search**: Enables natural language understanding of domain-specific content

---

*Built with ❤️ using Azure AI services and Microsoft Prompt Flow*