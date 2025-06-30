# Document Generation Integration Plan

## 🎯 Project Overview
Integrate Microsoft's Document Generation Solution Accelerator with your existing PromptFlow workout analysis system to enable:
- RAG chat with your fitness data via PromptFlow endpoint
- Auto-populated document templates with LLM-generated fitness insights
- Local deployment without Azure auto-provisioning

## 📋 Your Requirements (Confirmed)
1. **Clone and integrate** the document generation repo into existing environment
2. **Manual Azure deployment** - no auto-provisioning
3. **Connect to existing PromptFlow** endpoint for workout data queries
4. **Document template generation** based on fitness insights
5. **Educational documentation** for intern learning

## 🏗️ Architecture Integration

```
Your Existing System                 Document Generation Frontend
┌─────────────────────┐             ┌────────────────────────┐
│ Enhanced PromptFlow │             │   React UI             │
│ - Query Interpreter │ <---------> │   - Chat Interface     │
│ - Cosmos DB Query   │             │   - Template Builder   │
│ - AI Search Query   │             │   - Document Export    │
│ - LLM Enhancer      │             └────────────────────────┘
└─────────────────────┘                          |
         ^                                       v
         |                              Flask/Quart Backend
         |                              ┌─────────────────┐
         └----------------------------- │ PromptFlow API  │
                                       │ Integration     │
                                       └─────────────────┘
```

## 📂 Implementation Steps

### Phase 1: Environment Setup

1. **Clone the repository** (keeping it separate from your PromptFlow project):
   ```bash
   cd /Users/mikewarren
   git clone https://github.com/microsoft/document-generation-solution-accelerator.git
   cd document-generation-solution-accelerator
   ```

2. **Create a Python virtual environment**:
   ```bash
   conda create -n docgen python=3.11 -y
   conda activate docgen
   ```

3. **Install dependencies**:
   ```bash
   cd src/backend
   pip install -r requirements.txt
   
   cd ../frontend
   npm install
   ```

### Phase 2: Deploy PromptFlow as Endpoint

**Manual Azure Steps Required:**

1. **Create PromptFlow Endpoint in Azure ML Studio**:
   - Navigate to Azure Machine Learning workspace
   - Go to "Endpoints" > "Real-time endpoints"
   - Click "Deploy" > "Deploy a model"
   - Select "PromptFlow" deployment type
   - Upload your `flow.dag.yaml` and associated files
   - Configure compute instance (recommend Standard_DS3_v2)
   - Enable authentication (key-based for simplicity)

2. **Get Endpoint Details**:
   - Endpoint URL: `https://<your-endpoint>.inference.ml.azure.com/score`
   - API Key: From "Consume" tab in endpoint details

### Phase 3: Configure Document Generation

1. **Create `.env` file in `/src/backend/`**:
   ```bash
   # PromptFlow Integration
   USE_PROMPTFLOW=True
   PROMPTFLOW_ENDPOINT=https://<your-endpoint>.inference.ml.azure.com/score
   PROMPTFLOW_API_KEY=<your-endpoint-key>
   PROMPTFLOW_RESPONSE_TIMEOUT=120
   PROMPTFLOW_REQUEST_FIELD_NAME=inputs
   PROMPTFLOW_RESPONSE_FIELD_NAME=outputs
   PROMPTFLOW_CITATIONS_FIELD_NAME=search_result
   
   # Map to your PromptFlow inputs/outputs
   PROMPTFLOW_QUERY_FIELD=query
   PROMPTFLOW_USE_SEARCH_FIELD=use_search
   PROMPTFLOW_SEARCH_TYPE_FIELD=search_type
   
   # Document Generation Settings
   AZURE_OPENAI_ENDPOINT=<same-as-your-promptflow>
   AZURE_OPENAI_API_KEY=<same-as-your-promptflow>
   AZURE_OPENAI_MODEL=gpt-4o-smashGPT
   AZURE_OPENAI_TEMPLATE_SYSTEM_MESSAGE="You are a fitness document assistant. Generate structured templates for fitness reports, workout plans, and progress summaries."
   
   # Optional: Direct AI Search (if you want hybrid approach)
   AZURE_SEARCH_SERVICE=<your-search-service>
   AZURE_SEARCH_INDEX=workout-entries-index
   AZURE_SEARCH_KEY=<your-search-key>
   
   # App Configuration
   BACKEND_URL=http://localhost:5000
   AUTH_ENABLED=false
   ```

### Phase 4: Modify Integration Points

1. **Update `backend/settings.py`** to handle your PromptFlow schema:
   ```python
   # Add custom field mappings for your enhanced PromptFlow
   PROMPTFLOW_ENHANCED_RESULT_FIELD = "enhanced_result"
   PROMPTFLOW_SQL_RESULT_FIELD = "sql_result"
   ```

2. **Create adapter in `backend/promptflow_adapter.py`**:
   ```python
   def format_promptflow_request(user_query, use_search=True, search_type="hybrid"):
       """Format request for your enhanced PromptFlow."""
       return {
           "inputs": {
               "query": user_query,
               "use_search": use_search,
               "search_type": search_type
           }
       }
   
   def parse_promptflow_response(response):
       """Parse enhanced PromptFlow response."""
       outputs = response.get("outputs", {})
       return {
           "reply": outputs.get("enhanced_result", {}).get("enhanced_analysis", ""),
           "documents": outputs.get("search_result", {}).get("results", []),
           "sql_data": outputs.get("sql_result", {})
       }
   ```

### Phase 5: Create Fitness Document Templates

1. **Define template types in `backend/templates/fitness_templates.py`**:
   ```python
   WORKOUT_SUMMARY_TEMPLATE = {
       "name": "Weekly Workout Summary",
       "sections": [
           {"title": "Overview", "prompt": "Summarize total workouts, exercises, and volume"},
           {"title": "Strength Progress", "prompt": "Analyze strength gains and PRs"},
           {"title": "Consistency Analysis", "prompt": "Evaluate workout frequency and patterns"},
           {"title": "Recommendations", "prompt": "Provide personalized fitness recommendations"}
       ]
   }
   
   PROGRESS_REPORT_TEMPLATE = {
       "name": "Monthly Progress Report",
       "sections": [
           {"title": "Executive Summary", "prompt": "High-level fitness progress overview"},
           {"title": "Performance Metrics", "prompt": "Detailed analysis of key exercises"},
           {"title": "Goal Achievement", "prompt": "Progress toward fitness goals"},
           {"title": "Next Month Plan", "prompt": "Suggested workout plan for next month"}
       ]
   }
   ```

### Phase 6: Frontend Configuration

1. **Update `frontend/.env`**:
   ```bash
   VITE_BACKEND_URL=http://localhost:5000
   ```

2. **Add fitness-specific UI elements** in `frontend/src/pages/chat/Chat.tsx`:
   - Quick template buttons for common fitness documents
   - Exercise-specific filters
   - Date range selectors

### Phase 7: Local Testing

1. **Start backend**:
   ```bash
   cd src/backend
   python app.py
   ```

2. **Start frontend**:
   ```bash
   cd src/frontend
   npm run dev
   ```

3. **Test workflow**:
   - Chat: "Show me my workout progress this month"
   - Generate template: "Create a monthly progress report"
   - Populate sections with PromptFlow data
   - Export as DOCX

## 🔌 Integration Architecture

### Request Flow:
1. User asks question in chat → 
2. Backend routes to PromptFlow endpoint →
3. Your enhanced PromptFlow processes (SQL + Search + LLM) →
4. Response formatted for document generation →
5. User can create templates and export documents

### Key Integration Files:
- `app.py`: Main routing logic
- `settings.py`: Configuration management
- `promptflow_adapter.py`: Custom adapter for your schema
- `fitness_templates.py`: Domain-specific templates

## 📚 Educational Documentation Structure

Create these documents for your intern:

1. **ARCHITECTURE.md**: System design and data flow
2. **PROMPTFLOW_INTEGRATION.md**: How PromptFlow endpoints work
3. **DOCUMENT_TEMPLATES.md**: Template system explanation
4. **API_REFERENCE.md**: All endpoints and their purposes
5. **DEPLOYMENT_GUIDE.md**: Step-by-step Azure deployment
6. **TROUBLESHOOTING.md**: Common issues and solutions

## 🚀 Next Steps

1. **Deploy your PromptFlow** to Azure ML endpoint
2. **Clone and configure** document generation repo
3. **Test integration** with sample queries
4. **Customize templates** for fitness domain
5. **Document the process** for educational purposes

## 🎯 Expected Outcomes

- **Fitness Chat**: Natural language queries about workout data
- **Auto-Generated Documents**:
  - Weekly/Monthly workout summaries
  - Progress reports with charts
  - Personalized training plans
  - Goal tracking documents
- **Educational Value**: Complete system for intern to study modern AI architecture

This plan provides a clear path to integrate the document generation capabilities with your existing PromptFlow system without auto-deploying to Azure, while maintaining full control over the deployment process.