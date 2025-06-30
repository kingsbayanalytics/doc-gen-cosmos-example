# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Prompt Flow project that enables natural language querying of workout data stored in Azure Cosmos DB. Users can ask questions in plain English, which are converted to SQL queries and executed against their fitness tracking data.

## Architecture

The system follows this flow:
1. User asks a natural language question (e.g., "How many strength exercises did I do last week?")
2. Azure OpenAI GPT-4o converts the question to a Cosmos DB SQL query
3. The SQL query is executed against Cosmos DB
4. Results are returned to the user in JSON format

## Key Components

- **csv_to_jsonl.py**: Converts CSV workout data to JSONL format for Cosmos DB ingestion
- **load_csv_to_cosmos.py**: Uploads JSONL data to Azure Cosmos DB with proper error handling
- **query_interpreter.py**: Uses Azure OpenAI to convert natural language to SQL
- **cosmos_query_runner.py**: Executes SQL queries against Cosmos DB and formats results
- **flow.dag.yaml**: Prompt Flow DAG that orchestrates the query pipeline

## Development Commands

```bash
# Convert CSV to JSONL
python csv-promptflow-test/csv_to_jsonl.py "Workout Entries SP.csv" workout_entries_cosmos.jsonl

# Upload data to Cosmos DB
cd csv-promptflow-test
python load_csv_to_cosmos.py

# Run Prompt Flow locally
pf run --flow . --inputs query="How many sets did I do last week?"

# Test individual components
python query_interpreter.py
python cosmos_query_runner.py
```

## Data Schema

Workout data contains these fields:
- `id`: Unique identifier (e.g., "entry_1")
- `ExDate`: Exercise date
- `Exercise`: Exercise name
- `Set`: Set number
- `Reps`: Number of repetitions
- `Weight`: Weight used
- `ExType`: Exercise type (e.g., "Strength", "Cardio")

## Environment Variables

Required in `.env` file:
- `COSMOS_URI`: Azure Cosmos DB endpoint
- `COSMOS_KEY`: Primary key for authentication
- `COSMOS_DB`: Database name (sql-test)
- `COSMOS_CONTAINER`: Container name (sql-test)
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint
- `AZURE_OPENAI_CHAT_DEPLOYMENT`: GPT-4o deployment name
- `AZURE_OPENAI_API_VERSION`: API version (2025-01-01-preview)

## Testing

When testing queries, ensure:
1. Environment variables are properly set
2. Cosmos DB container has data loaded
3. Azure OpenAI connection is active
4. Test with various natural language queries to verify SQL generation

## Future Enhancements

- Integration with Azure AI Search for vector-based semantic search
- Support for more complex workout analytics
- Caching layer for frequently asked questions
- Export functionality for query results

## Document Generation Integration

This project integrates with Microsoft's Document Generation Solution Accelerator to enable:
- RAG chat with fitness data via PromptFlow endpoint
- Auto-populated document templates with LLM-generated fitness insights
- Export capabilities for workout summaries, progress reports, and training plans

### Integration Architecture
The enhanced PromptFlow system serves as the backend data engine for document generation:
- PromptFlow endpoint provides intelligent workout analysis
- Document generation frontend consumes PromptFlow responses
- Templates auto-populate with personalized fitness insights
- Users can export as Word documents

### Key Files for Document Generation
- `DOCUMENT_GENERATION_PLAN.md` - Complete integration plan
- `DOCGEN_ENV_TEMPLATE.env` - Environment variables template
- PromptFlow must be deployed as Azure ML endpoint for integration

### Document Generation Workflow
1. User queries workout data through document generation UI
2. System routes to deployed PromptFlow endpoint
3. Enhanced analysis (SQL + Search + LLM) returns structured insights
4. User creates document templates populated with insights
5. Export as formatted Word documents

When working on document generation integration:
- Follow the detailed plan in `DOCUMENT_GENERATION_PLAN.md`
- Use manual Azure deployments only (no auto-provisioning)
- Maintain separate codebases connected via API
- Focus on educational documentation for intern learning

## Document Generation Integration - Design Decisions & Status

### ✅ Completed Integration Steps

#### 1. **PromptFlow Backend Integration**
- **Status**: ✅ WORKING
- **Decision**: Use existing PromptFlow as data source for document generation
- **Implementation**: Document generation app consumes PromptFlow endpoint via REST API
- **Key Files**: `src/backend/promptflow_handler.py`, `src/app.py`

#### 2. **Browse/Chat Functionality** 
- **Status**: ✅ WORKING
- **Decision**: Maintain original chat interface with PromptFlow integration
- **Implementation**: Chat page successfully queries workout data and displays insights
- **Example**: "How many pushups have I done?" → "You've performed 3,226 pushups!"

#### 3. **Data Quality Fixes**
- **Status**: ✅ WORKING
- **Decision**: Implement schema-aware SQL generation for robust data access
- **Implementation**: 
  - `schema_discovery.py`: Auto-discovers database field names and categorical values
  - `query_interpreter.py`: Maps natural language to exact database values ("pushups" → "Pushup")
  - `StringToNumber()` conversion for string-stored numeric fields
- **Impact**: Eliminated "no data found" errors, now returns real workout statistics

#### 4. **Chat History Infrastructure**
- **Status**: ✅ WORKING
- **Decision**: Use separate CosmosDB container for conversation history
- **Implementation**: 
  - CosmosDB setup: `sql-test` database, `conversations` container
  - Environment configuration: `AZURE_COSMOSDB_*` variables in `src/.env`
  - Backend gracefully handles disabled chat history for PromptFlow-only mode

### 🔧 Current Issue: Template Generation

#### **Problem**: "No content in messages object" error when generating templates

#### **Root Cause Analysis**:
1. **Original Design**: Template generation expects structured JSON response with document sections
2. **Current Behavior**: PromptFlow returns workout data analysis (not template structure)
3. **Format Mismatch**: Frontend expects `{"template": [{"section_title": "...", "section_description": "..."}]}`
4. **Current Output**: Enhanced fitness analysis text

### 📋 Recommended Solution Path (Staying True to Original Design)

#### **Option A: Minimal Backend Modification (RECOMMENDED)**
- **Principle**: Keep PromptFlow unchanged, add template formatting logic in document generation backend
- **Implementation**: 
  1. Detect template requests via `ChatType.TEMPLATE` 
  2. Call PromptFlow for workout data analysis
  3. Transform PromptFlow response into template JSON structure
  4. Use workout insights to populate section descriptions
- **Pros**: No PromptFlow changes, follows original architecture
- **Cons**: Requires backend logic to convert analysis to template format

#### **Option B: Dual System Message Approach**
- **Principle**: Use different system messages for template vs. browse requests
- **Implementation**: Modify template requests to use `AZURE_OPENAI_TEMPLATE_SYSTEM_MESSAGE` instead of PromptFlow
- **Pros**: Leverages original template generation design
- **Cons**: Templates wouldn't include actual workout data insights

#### **Option C: PromptFlow Extension** 
- **Principle**: Add template generation capability to PromptFlow
- **Implementation**: Add conditional logic to return template JSON when template keywords detected
- **Pros**: Single source of truth, data-driven templates
- **Cons**: Modifies PromptFlow significantly, deviates from original design

### 🎯 Next Steps (Incremental Testing)

#### **Step 1: Understand Current Template Flow**
- [ ] Test original template generation with Azure AI Search disabled
- [ ] Verify `AZURE_OPENAI_TEMPLATE_SYSTEM_MESSAGE` behavior in isolation
- [ ] Document exact request/response format expected by frontend

#### **Step 2: Implement Option A (Backend Transform)**
- [ ] Add template detection logic in `conversation_internal()`
- [ ] Create function to transform PromptFlow analysis into template JSON
- [ ] Test with simple template request: "Create a monthly pushup report template"

#### **Step 3: Validate Template Structure**
- [ ] Ensure JSON format matches `DraftedDocument` model
- [ ] Test frontend parsing of generated template
- [ ] Verify template history saves correctly

#### **Step 4: Content Generation Integration**
- [ ] Test section content generation using PromptFlow data
- [ ] Ensure individual sections can be populated with workout insights
- [ ] Verify Word document export functionality

### 🔄 Design Principles Maintained
1. **Minimal Code Changes**: Reuse existing PromptFlow for data access
2. **Original Architecture**: Keep template/browse separation intact  
3. **Data-Driven**: Templates populated with real workout analytics
4. **Incremental Progress**: Each step independently testable
5. **Fallback Capability**: Template generation can fall back to Azure OpenAI if needed

## 📋 Critical Development Rule: PromptFlow Integration Documentation

**MANDATORY**: When working on PromptFlow Document Generation integration, ALWAYS:

1. **Reference**: Check `PROMPTFLOW_DOCUMENT_GENERATION_INTEGRATION.md` for current status
2. **Update**: Modify the integration document after any changes to:
   - Backend integration code (`src/app.py`)
   - PromptFlow configuration 
   - Frontend parsing fixes
   - Environment setup
   - Testing protocols
3. **Track Progress**: Update status sections (✅ WORKING, 🔧 IN PROGRESS, ❌ BROKEN)
4. **Document Issues**: Add any new problems to the troubleshooting section
5. **Preserve Knowledge**: Ensure future developers can understand the integration without context

**Key Files to Maintain**:
- `PROMPTFLOW_DOCUMENT_GENERATION_INTEGRATION.md` - Primary integration documentation
- `CLAUDE.md` - This file (high-level project guidance)
- `DOCUMENT_GENERATION_PLAN.md` - Original planning document

**Before Making Changes**: Read the integration document to understand current state
**After Making Changes**: Update the integration document with new status and learnings

This rule prevents regression and ensures the complex PromptFlow + Document Generation integration remains maintainable for future developers modifying the Microsoft Document Generation Solution Accelerator.