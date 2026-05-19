# 🚀 渣打银行 AI Director 终极面试作业：3天作战计划 (The 3-Day Blitz)

## 📌 项目愿景与架构定位 (Executive Vision)
抛弃本地玩具数据库，交付一个基于真实云原生基建的**企业级自动化 RAG 评估与诊断框架**。
**核心基建 (已打通)**：GCP Cloud SQL (PostgreSQL 13 + `pgvector`)，通过带 SSL 域名的 Envoy Proxy (`db.jpgcp.cloud:5432`) 实现外网安全反向代理。
**真实语料 (已就绪)**：《2025年汇丰银行年度财报》完整 PDF (9.7MB, 300+页)。

---

## 🗓️ Day 1: 基建入库与数据合成 (Ingestion & Synthetic Data)
*目标：把生肉切碎放进冷库，并用大模型自动生成“黄金试卷”。*

### 1.1 Terraform 架构装裱 (Infrastructure-as-Code)
*   **动作**：在项目中建立 `infra/` 目录。
*   **产出**：放入 `.tf` 配置文件（展示 Cloud SQL, VPC, Cloud NAT, Envoy Proxy 的声明式部署）。
*   *战术意义*：不要求面试官运行，纯粹展示你作为 Director 级架构师的 IaC 与云原生掌控力。

### 1.2 真实语料解析与入库 (The Ingestion Pipeline)
*   **动作**：编写 `01_data_ingestion.py`。
*   **逻辑**：
    *   使用 `langchain-community` (PyPDFLoader) 读取汇丰财报 PDF。
    *   读取 `optimizer_config_template.json` 里的 Chunking 策略（如 `fixed_256`, `fixed_512` 等）。
    *   调用 GCP Vertex AI 生成 Embeddings。
    *   使用 `langchain-postgres` 将多套配置生成的 Vectors 和 Metadata 写入 Cloud SQL (`pgvector`) 的不同表中。

### 1.3 自动合成“黄金测试集” (Synthetic Data Bootstrapping)
*   **动作**：编写 `02_data_generation.py`。
*   **逻辑**：利用 Gemini API 扮演“刁钻财务分析师”，针对财报抽样数据反向提问。
    *   生成 `case1_eval_dataset.csv` (包含 Question, Document IDs, Golden Context, Golden Answer)。
    *   生成 `case2_query_doc_dataset.csv` (无答案盲测集，包含开放性、跨文档的宏观问题)。

---

## 🗓️ Day 2: 核心评估引擎与超参扫描 (The Evaluator Engine)
*目标：构建能自动换刀切肉、换锅炒菜，并为每一盘菜精准打分的自动化实验室。*

### 2.1 构建动态 RAG 执行器 (Dynamic RAG Runner)
*   **动作**：编写面向对象的 `RAGPipelineRunner` 类。
*   **逻辑**：遍历 `optimizer_config_template.json` 中定义的不同 Indexing (BM25, Dense), Reranking (MiniLM, LLM) 和 Generation (Temp, Prompts) 组合，分别对 Case 1 和 Case 2 现场生成 `ai_response`。

### 2.2 构建双轨打分器 (The Metric Evaluator)
*   **动作**：编写 `RAGEvaluator` 类（可基于 `ragas` 或手写 LLM Prompt）。
*   **Case 1 (Direct Eval)**：计算 `Recall@K`, `nDCG@K`（检索层），`Semantic Similarity` 和 `Answer Correctness`（生成层）。
*   **Case 2 (Proxy Eval)**：祭出杀手锏 **LLM-as-a-Judge / RAG Triad**，计算 `Context Relevance` (相关性), `Faithfulness` (防幻觉忠实度), `Answer Relevance` (回答有效性)。
*   **数据落盘**：将跑分结果用 `pandas` 整理并存入内存或 SQLite 供诊断。

---

## 🗓️ Day 3: 诊断大脑出炉与降维文档 (Diagnoser & Executive README)
*目标：通过规则引擎开出处方，撰写让面试官折服的架构总结。*

### 3.1 开发核心诊断引擎 (The Diagnoser)
*   **动作**：编写 `RAGDiagnoser` 类。
*   **逻辑**：实现“病理诊断树”。例如：
    *   `IF Recall is HIGH AND Faithfulness is LOW -> Root Cause: Hallucination -> Action: Lower Temperature, enforce strict citation.`
    *   `IF Context Relevance is LOW AND Answer Relevance is HIGH -> Root Cause: Data Leakage (LLM relied on internal memory) -> Action: Change Chunking size.`
*   **产出**：输出完美契合作业要求的 `diagnosis_report_template.json`。

### 3.2 终极包装与测试 (The Wrapper)
*   **动作**：编写入口文件 `main.py`。
*   **体验优化**：确保面试官只需 `pip install -r requirements.txt` 和 `python main.py` 就能跑通你的 Evaluator 和 Diagnoser（无痛连接你准备好的 Cloud SQL 外网节点）。

### 3.3 撰写总监级 README (The Executive Summary)
*   **动作**：编写高质量全英文 `README.md`。
*   **内容**：
    1.  附上一张高颜值的**全栈架构图** (GCP + Cloud SQL + GKE RAG + Terraform)。
    2.  解答作业中的所有 **Live interview prompts**（如何防止小数据过拟合、如何权衡重排器的延迟与准确度、如何评估成本 Token Cost 等）。
    3.  声明 Future Work（如引流至 BigQuery 构建监控看板等）。

---
**⚔️ 统帅，计划已定。只要您一声令下，Alice 即刻为您生成 Day 1 (数据切分与入库) 的 Python 代码骨架！**
