# 潘文林 (Jason)
**目标职位:** 模型验证总监 (Model Validation Director) / AI 安全与治理负责人
**工作地点:** 广州
**工作经验:** 17年 (10+年金融科技与合规风控经验)
**学历:** 本科 (广东外语外贸大学 - 计算机科学与技术)

---

## 职业总结 (Professional Summary)
资深金融科技与 AI 工程专家，拥有超过 17 年软件研发与架构经验，深耕 **金融风险与合规 (Risk & Compliance)** 领域逾 10 年。
*   **AI 安全与模型治理:** 专注于 **GenAI (生成式 AI)** 与 **LLM (大语言模型)** 的落地与治理，主导设计了企业级 **RAG Agent (ADA项目)** 的全生命周期管理，包括模型评估 (Model Evaluation)、监控 (Monitoring) 及合规性审查 (Compliance Check)。
*   **模型验证架构体系:** 具备构建自动化模型验证流水线的实战经验，利用 **GCP (Dataflow, BigQuery)** 和 **Kubeflow** 搭建了端到端的 MLOps 平台，确保模型在生产环境的准确性、稳定性与可解释性。
*   **监管合规与 MRM:** 深刻理解全球金融监管要求 (如 SR 11-7, Basel, GDPR)，在汇丰银行 (HSBC) 负责监管合规数据平台 (RCDP) 的建设，确保数据处理与模型应用符合严格的银行审计与风控标准。
*   **技术领导力:** 具备跨国团队管理经验，擅长连接数据科学、风险管理与工程团队，推动复杂 AI 项目的合规落地与价值交付。

---

## 核心技能 (Core Skills)
*   **AI & Model Validation:** GenAI/LLM Evaluation, RAG Architecture, AI Safety, Model Monitoring, Explainable AI (XAI), Prompt Engineering Governance.
*   **Cloud & MLOps:** Google Cloud Platform (GCP), Kubernetes (GKE), Kubeflow, Dataflow (Apache Beam), BigQuery, Terraform (IaC).
*   **Programming:** Python (Expert), Java (Expert), SQL, Shell Scripting.
*   **Frameworks:** LangChain, TensorFlow/PyTorch (Deployment & Validation), Spring Boot, FastAPI.
*   **Evaluation Tools:** LangSmith, MLflow, Prometheus/Grafana (Monitoring), BERTScore, LLM-as-a-Judge (Custom Implementation).
*   **Domain:** Financial Risk Management, Regulatory Compliance (AML/KYC/Sanctions), Data Governance, GDPR.

---

## 工作经历 (Work Experience)

### **汇丰软件开发 (广东) 有限公司 (HSBC Software Development)**
**职位:** 技术负责人 & 研发经理 - 监管合规数据平台 (RCDP) | **时间:** 2018.06 - 至今

**核心职责：领导监管合规数据平台与 AI 模型治理体系建设**

*   **GenAI 模型验证与治理体系 (Model Validation for GenAI):**
    *   主导 **"ADA" (Ask Compliance Digital Assistance)** 项目的 **模型验证与评估框架** 设计。该项目利用 **RAG (检索增强生成)** 技术自动化处理合规咨询，直接服务于银行前线业务。
    *   建立 **自动化模型评估流水线 (Automated Evaluation Pipeline)**，引入 **LLM-as-a-Judge** 机制，结合 **NLP 模型** 对输入查询进行敏感度分析 (Sensitivity Analysis) 和意图识别，并对 LLM 输出进行准确性与合规性校验，确保符合 **Responsible AI** 原则。
        *   **数据闭环 (Data Loop):** 构建全链路数据采集机制，实时收集 **User Query (用户提问)**、**AI Response (模型回答)** 及 **User Feedback (用户反馈)** 三大核心数据，为持续优化模型性能提供高价值样本。
    *   开发 **模型监控仪表盘 (Model Monitoring Dashboard)**，实时追踪全维度的模型评估指标，并生成合规审计报告，满足内部 MRM (Model Risk Management) 要求。
        *   **核心评估指标 (Core Metrics):** 监控 **Completeness (完整性)**, **Faithfulness (忠实度)**, **Accuracy (准确率)**, **Cosine Similarity (语义相似度)** 及 **Toxicity (毒性)**，确保模型输出的高质量与安全性。
        *   **安全与合规 (Security & Compliance):** 实施 **PII Flag (敏感信息检测)** 与 **Jailbreaking Flag (越狱攻击检测)** 机制，防止数据泄露与恶意诱导。
        *   **性能与成本 (Performance & Cost):** 追踪 **Latency (延迟)** 与 **Cost per Response (单次响应成本)**，优化资源利用率。
    *   实施 **数据质量与偏见管理 (Data Quality & Bias Mitigation)**，利用 **Dataflow** 清洗与标准化政策文档 (GPPS)，构建高质量向量数据库 (AlloyDB)，从源头降低模型幻觉 (Hallucination) 风险。

*   **MLOps 与模型全生命周期管理:**
    *   基于 **GCP Kubeflow** 构建标准化的 MLOps 平台，统一管理从模型训练、验证到部署的完整流程，实现了模型版本控制与可追溯性 (Traceability)，符合金融监管审计要求。
    *   设计并实施 **非侵入式验证架构**，通过流式 API (Streaming API) 将 AI 能力集成至上游系统，在不破坏原有系统稳定性的前提下引入先进的 AI 验证机制。

*   **团队管理与跨部门协作:**
    *   带领全球工程团队，与数据科学家、风险合规专家 (Risk Stewards) 及产品负责人紧密协作，将复杂的 MRM 规范转化为可执行的技术标准与代码规范。
    *   推动 DevSecOps 文化，在 CI/CD 流水线中集成自动化测试与安全扫描，确保模型发布的合规性与安全性。

### **友邦资讯科技 (AIA Information Technology)**
**职位:** 高级软件工程师 | **时间:** 2017.11 - 2018.06
*   负责核心团险系统 (Group Insurance) 的迁移与验证工作，确保新旧系统数据一致性与业务逻辑准确性。
*   参与系统稳定性评估与性能调优，建立关键业务指标监控体系。

### **上海微创软件 (Client: AIA)**
**职位:** 系统工程师 | **时间:** 2016.12 - 2017.11
*   主导团险业务模块的技术设计与代码审查，确保交付质量符合保险行业标准。
*   负责 UAT 测试支持与生产环境问题排查，保障系统高可用性。

### **塔塔信息技术 (Client: HSBC)**
**职位:** 高级软件工程师 | **时间:** 2011.03 - 2016.12
*   参与汇丰银行全球核心交易系统的开发与维护，深入理解银行业务流程与风控逻辑。
*   设计高并发交易处理模块，并实施严格的单元测试与集成测试，确保金融交易数据的准确性。

---

## 项目经验 (Selected AI & Validation Projects)

*   **企业级合规助手 (Project ADA - RAG Agent):**
    *   **描述:** 基于 LangChain 和 GCP 构建的企业级 RAG 应用，辅助合规人员快速查询全球政策。
    *   **验证贡献:** 设计了基于 "Golden Dataset" 的自动化评估机制，通过计算语义相似度 (Semantic Similarity) 和事实一致性 (Factuality) 指标，量化评估 RAG 系统的回答质量。

*   **自动化 AI 代码审查工具 (Automated AI Code Reviewer):**
    *   **描述:** 集成 GitHub Webhook 与 Gemini LLM 的智能代码审查 Agent。
    *   **验证贡献:** 引入 "Human-in-the-loop" 机制，收集开发者反馈以微调 Prompt 策略，持续提升代码建议的准确率与采纳率。

---

## 教育背景 (Education)
*   **广东外语外贸大学** - 计算机科学与技术 (本科) | 2003.09 - 2007.07
