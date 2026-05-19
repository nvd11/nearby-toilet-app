# ADA Project (Ask Compliance Digital Assistant) - True Architecture

**Context:** ADA is an AI assistant built to reduce the manual workload of human compliance experts who answer global policy questions from front-line HSBC staff.

## 4 Core Systems
1. **AskC (Ask Compliance):** The front-end user Q&A system.
2. **RCDP (RC Data Platform):** Boss Jason's team. Acts as the data hub and orchestrator.
3. **GenAI (Gen AI System):** The system hosting the LLM, RAG Agent, and VectorDB.
4. **GPPS (Global Policy & Procedures System):** The source of truth for compliance documents.

## 3 Main Workflows

### 1. Document Embedding Workflow
- **Flow:** GPPS -> RCDP -> GenAI
- GPPS pushes updated policy/procedure docs to RCDP.
- RCDP filters and detects documents relevant to ADA.
- RCDP pushes relevant doc data to the GenAI system's Embedding API.
- GenAI system builds and maintains the VectorDB (Knowledge Base).

### 2. Core Q&A Workflow (RAG via Orchestration)
- **Flow:** AskC -> Pub/Sub -> RCDP Orchestration -> GenAI -> RCDP Orchestration -> Pub/Sub -> AskC
- User submits a form in AskC.
- If AskC determines it's in scope, it drops the query data into an RCDP Pub/Sub queue.
- **RCDP Orchestration Service** pulls the query.
- *Pre-filtering:* RCDP uses Python libraries and **BM25 algorithm** to evaluate relevance, data sensitivity, and complexity.
- If suitable, RCDP calls the GenAI system's RAG Agent query interface.
- GenAI queries its VectorDB and returns the AI response + metrics (e.g., policy chunk match score) back to Orchestration Service.
- Orchestration Service sends the result back to AskC via a second Pub/Sub queue.
- *Result:* Compliance experts see the AI's reference answer. Non-intrusive AI empowerment for AskC.

### 3. Model Evaluation & Monitoring Workflow
- **Flow:** AskC -> RCDP -> MI System / Data Analysts
- AskC sends the processed query, AI response, and **User Feedback** back to RCDP.
- RCDP persists this data.
- RCDP collaborates with Data Analysts to build an Evaluation API.
- The API processes the data and generates model evaluation metrics for each AI response.
- MI (Management Information) systems generate reports.
- Data Analysts and GenAI tech teams use these reports to continuously improve the RAG agent.