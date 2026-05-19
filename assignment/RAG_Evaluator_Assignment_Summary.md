# Automated RAG Evaluator and Diagnoser - 核心需求拆解与战略分析

**🎯 面试官核心考点：** 
构建一个能跨多种参数配置（Chunking, Indexing, Reranking, Prompting, Generation）对 RAG 系统进行全自动“超参扫描 (Hyperparameter Sweep)”并能输出“归因诊断 (Root Cause Analysis)”的实验框架。

## 📂 第一部分：作业需求与打分标准（文档类）

### 1. `candidate_assignment_rag_evaluator.docx` (核心任务书)
*   **必须交付物 (Deliverables)**：
    *   **架构设计说明** (Evaluator & Diagnoser Architecture)。
    *   **评估指标目录** (Metric catalog)，需定义不同阶段的计算方式。
    *   **可运行的原型代码** (Runnable Python skeleton)。
    *   **实验配置格式** (支持读取/遍历多个对比设置)。
    *   **诊断报告示例** (输出包含根本原因分析与优化建议的 JSON)。
*   **灵魂拷问 / 现场答辩准备 (Live interview prompts)**：
    *   当检索 Recall 很好但生成答案很差时，怎么归因？
    *   Case 2（盲测无标准答案）你怎么比较不同配置？
    *   你怎么区分是“重排器(Reranker)”拉胯，还是“分块(Chunking)”拉胯？
    *   如何防止在小验证集上过拟合？

### 2. `grading_rubric_rag_evaluator.docx` (打分红线/机密)
*   **得分要点**：必须区分“检索”和“生成”阶段进行独立打分；必须实现“诊断逻辑（Diagnosis logic）”将分数映射到根本原因。
*   **扣分雷区 (Red Flags)**：只用 BLEU/ROUGE 等低级指标评估；Case 2 只让 LLM 盲目输出而不做 RAG Triad 评估；代码不可运行或高度硬编码。

### 3. `README.md` (说明文件)
*   强调了**不要用假数据交差**，必须自己去下载真实的上市公司财报（我们下载的 9.7MB 汇丰年报 PDF 完美契合）。

---

## ⚙️ 第二部分：系统输入与输出协议（JSON 模板）

### 4. `optimizer_config_template.json` (优化器输入配置)
*   规定了代码必须能读取并扫描的配置空间：
    *   `chunking`: fixed_256_overlap_32, fixed_512, recursive_section_aware...
    *   `indexing`: bm25, dense_bge, hybrid_bm25_dense...
    *   `reranking`: none, cross_encoder_miniLM, llm_rerank...
    *   `query_prompting`: raw_query, query_rewrite...
    *   `generation`: strict_citation_low_temp, balanced_temp...

### 5. `diagnosis_report_template.json` (诊断报告输出模板)
*   **作业最终产出物**。必须输出包含 `quality_score`, `latency_seconds`, `cost_estimate` 以及分段指标的 JSON。
*   最核心的是 `diagnosis` 数组：需包含 `issue`, `evidence`, `likely_root_causes`, `recommended_actions`。

---

## 📊 第三部分：模拟数据集结构（CSV/JSONL）

### 6. `reference_corpus.jsonl` (原始语料格式)
*   展示了被建库的文档结构（`doc_id`, `title`, `text`）。实操中，该部分将被我们从 PDF 提取的 Chunk 列表替代并写入 Cloud SQL (pgvector)。

### 7. `case1_eval_dataset.csv` (有标准答案的测试集 / Direct Eval)
*   包含 `query` 和 `reference_answer`。
*   **评估指标**：可计算 Recall@K, nDCG@K（检索层）以及 Semantic Similarity / Answer Correctness（生成层）。

### 8. `case2_query_doc_dataset.csv` (盲测集 / Proxy Eval)
*   只有 `query`，无标准答案。
*   **评估指标**：必须使用 LLM-as-a-Judge 计算 RAG Triad（Context Relevance, Faithfulness, Answer Relevance）。

---

## 🚀 Alice 的战略部署 (The 3-Day Blitz)
我们的核心技术栈（降维打击方案）：**GCP Cloud SQL (pgvector) + Python/LangChain 面向对象架构 + Terraform 基础设施声明**。

*   **Step 1. Data Ingestion (数据入库)**：解析汇丰 PDF，按照不同 Chunking 策略写入 `db.jpgcp.cloud` 的 pgvector 实例。
*   **Step 2. The Evaluator (评估引擎)**：读取 JSON 配置，循环查询 Cloud SQL，调用 Vertex AI/Gemini 打分。
*   **Step 3. The Diagnoser (诊断大脑)**：设计一套 `if-else` 规则树，分析得分并生成最终的 `diagnosis_report.json`。
