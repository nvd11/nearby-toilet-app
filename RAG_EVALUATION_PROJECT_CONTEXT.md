# RAG Evaluator and Diagnoser - Project Context
*Last Updated: 2026-03-21*

## 1. Background & Goal
- **User:** Jason (Candidate for Director, AI Software Engineering at Standard Chartered).
- **Goal:** Complete a 5-day take-home assignment (compressed to 3 days) to build an "Automated RAG Evaluator and Diagnoser".
- **Key Differentiator:** Instead of a local toy setup, demonstrating executive-level engineering by using real GCP infrastructure (Cloud SQL + pgvector + Envoy Proxy) and Infrastructure-as-Code (Terraform).

## 2. Infrastructure (GCP)
- **Database:** Private Cloud SQL (PostgreSQL 13 + `pgvector`) running internally at `10.195.208.3`.
- **Gateway:** Envoy Proxy VM with a dedicated Public IP (`34.153.134.240`).
- **DNS:** `db.jpgcp.cloud` -> `34.153.134.240:5432`.
- **Status:** Connection tested and verified successfully via `psql`.

## 3. Data Corpus
- **File:** `/home/gateman/.openclaw/workspace/HSBC_Annual_Report_2025.pdf` (9.7MB).
- **Purpose:** Replaces the dummy `reference_corpus.jsonl` to serve as the real-world unstructured document corpus for the RAG ingestion pipeline.

## 4. Assignment Requirements & Execution Plan
### Phase 1: Data Ingestion (Current Step)
- Parse the HSBC PDF (`PyPDFLoader`).
- Chunking (`RecursiveCharacterTextSplitter`).
- Embeddings via Google Vertex AI.
- Upsert vectors and metadata into Cloud SQL `pgvector` via `langchain-postgres` / `psycopg2`.

### Phase 2: Dynamic RAG & Evaluator
- Read `optimizer_config_template.json` to sweep different parameters (e.g., chunk sizes, indexing types).
- **Case 1 (With Ground Truth):** Direct evaluation (Recall@K, nDCG@K, Semantic Similarity).
- **Case 2 (Blind Test):** Proxy evaluation using LLM-as-a-Judge (RAG Triad: Context Relevance, Faithfulness, Answer Relevance).

### Phase 3: The Diagnoser (Core Value)
- Rule engine analyzing the metrics (e.g., `IF Recall is HIGH AND Faithfulness is LOW -> Hallucination -> Adjust Prompt`).
- Output strictly formatted to `diagnosis_report_template.json`.

### Phase 4: Delivery
- Python object-oriented codebase.
- Terraform scripts in `infra/` folder.
- Executive README detailing trade-offs, architecture, and production scalability.
