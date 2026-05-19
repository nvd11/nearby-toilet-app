# 潘文林 (Jason Pan)
**目标职位:** 模型验证总监 (Model Validation Director) / AI 安全与治理负责人 / AI 首席架构师
**工作地点:** 广州 | **工作经验:** 17年 (10+年金融风控与合规经验，深耕 AI 治理与 MLOps)
**学历:** 本科 (广东外语外贸大学 - 计算机科学与技术)

---

## 职业总结 (Executive Summary)
资深金融科技与 AI 架构专家，拥有超过 17 年的软件研发与架构经验，其中 10+ 年专注于**金融风险与合规 (Risk & Compliance)** 领域。
* **企业级 AI 架构与治理:** 专注于 GenAI 与大模型在金融领域的高安全性落地。主导企业级 RAG Agent (ADA) 与合规风控 AI 系统 (Rapid2) 的全生命周期治理，精通非侵入式 AI 架构设计，**成功将合规工单响应时间从天级别压缩至 1 小时内**。
* **模型风险管理 (MRM) 与验证:** 深度理解全球金融监管合规要求 (SR 11-7, Basel, GDPR)。独立设计并落地自动化模型评估流水线与监控闭环，利用 LLM-as-a-Judge 构建涵盖完整度、忠实度、毒性及越狱拦截的多维 AI 安全指标体系。
* **MLOps 与云原生工程:** 极客级别的云原生实战能力，精通 GCP 生态 (BigQuery, Dataflow, Kubeflow, GKE)。从零构建面向数据科学家与业务系统的模型执行环境 (Model Execution Env)，实现从数据清洗、特征工程到模型一键部署与监控的端到端自动化。
* **前沿 AI 技术开拓者:** 具备罕见的“懂战略更懂底层代码”的复合优势。熟练运用 LangChain、ReAct 模式，并在开源社区持续贡献基于 MCP 协议的智能代理。期待与您进一步交流 AI 业务方向，探讨我的技能矩阵与团队目标的契合点。

---

## 核心能力 (Core Competencies)
* **AI 战略与治理:** 模型风险管理 (MRM), GenAI/LLM 评估指标构建, 负责任的 AI (Responsible AI), 越狱拦截与敏感度审查, 数据偏见清洗。
* **企业级 AI 架构:** 非侵入式 AI 编排 (Orchestration Service), RAG 架构, 向量数据库 (AlloyDB), MCP Server 开发与集成, LangChain。
* **MLOps 与云原生:** GCP (Dataflow, BigQuery, Pub/Sub, Cloud Run), Kubernetes (GKE), Kubeflow 机器学习平台, Jenkins/Terraform CI/CD。
* **软件工程与数据架构:** Python (异步高性能开发), Java (Spring Cloud 微服务), 流批一体数据处理 (Streaming/Batch ETL), 高并发架构设计。

---

## 工作经历 (Professional Experience)

### **汇丰软件开发 (广东) 有限公司 (HSBC)**
**职位:** 技术研发经理 / ITSO - 监管合规数据平台 (RCDP) | **时间:** 2018.06 - 至今
**核心职责：**全面负责 RCDP 平台的技术战略选型与架构演进，主导跨部门 (数据科学、风控合规、工程架构) 的企业级 AI 项目落地与合规数据体系建设。

#### **核心项目 1: 监管合规数据平台 (RCDP) 与 Ask Compliance AI 助手 (ADA)**
**项目背景：** 引入 GenAI 赋能传统合规咨询系统，减轻合规专家查阅海量跨国政策文档的成本。
* **企业级 AI 架构设计与合规拦截：** 设计并落地了核心的 **Orchestration Service (AI 编排层)**。在将用户提问路由至大模型前，基于 NLP 与 BM25 算法进行意图相关性分析与数据敏感度拦截，确保符合金融信息安全标准；实现对传统系统的**非侵入式 AI 赋能**。
* **卓越的业务价值：** 知识库融合了全球政策数据 (GPPS)，AI 助手上线后，**将合规查询工单的平均响应时间从“天级别”断崖式降至“1小时以内”**，极大释放了合规专家的生产力。
* **模型评估与 MRM 治理体系：** 开发 Model Evaluation API，收集“用户提问-AI回答-用户反馈”全链路数据。构建了基于 LLM-as-a-Judge 的多维监控仪表盘，实时追踪：
    * **核心质量指标:** 完整性 (Completeness), 忠实度 (Faithfulness), 准确率 (Accuracy), 语义相似度 (Cosine Similarity)。
    * **安全与合规防御:** 毒性检测 (Toxicity), PII 敏感数据拦截, 越狱攻击防御 (Jailbreaking Flag)，成功筑起 AI 输出的第二道防线。

#### **核心项目 2: Rapid2 智能合规警报分流系统 (Model1 Project)**
**项目背景：** 将机器学习能力无缝集成至传统 RC 警报系统，实现海量警报的自动化初步分类与处理。
* **构建端到端 MLOps 闭环：** 针对数据科学家“懂算法、弱工程”的痛点，主导开发了 **Model Execution Environment (模型执行环境)**。建立 CI/CD 流水线，实现从 Kubeflow 到生产环境的模型自动化部署与端到端测试。
* **实时数据流与反向验证：** 基于 Dataflow 与 Pub/Sub 构建 Streaming ETL，实时消费并处理上游警报数据；同时建立 Recommendation Reverse Flow 将模型决策实时写回业务系统。
* **模型决策自反馈机制：** 每日批量对比“模型推荐结论”与“合规人员最终决策”，通过 Evaluation Model 生成偏差与准确度报告，为模型的持续迭代提供量化依据。

#### **历史核心管理成就：全球冲突管理系统 (GCMS) 敏捷转型**
**角色:** 中国区团队经理 (Team Manager) | **时间:** 2021.08 - 2023.04
* 带领 9 人敏捷团队，推动研发模式从传统瀑布向 2-Week Sprint 敏捷交付转型。
* 实施深度 DevOps 改造（蓝绿部署、Feature Toggles），将自动化测试覆盖率从 0 提升至 70%，测试成本降低 50%。
* 领导微服务架构迁移，并在 1.5 个月内无生产事故地完成了 20+ 个组件的 Log4j 高危漏洞修复。

---

### **过往履历简述 (Previous Experience)**
在加入汇丰正式编制前，长达 7 年以核心外派专家身份为友邦保险 (AIA) 与汇丰银行提供底层系统架构支持。
* **友邦资讯科技 (2017.11 - 2018.06) / 上海微创 (2016.12 - 2017.11):** 担任高级系统工程师，主导核心团险系统 (Group Insurance) 的架构升级、代码审查与高并发性能调优。
* **塔塔信息技术 TCS - 汇丰项目 (2011.03 - 2016.12):** 担任高级软件工程师，深度参与汇丰全球核心交易系统开发，积累了深厚的底层金融业务逻辑、交易幂等性及高可用系统设计经验。

---

## 前沿 AI Agent 架构作品 (Open Source & Personal Projects)
* **Agentic Web Chat-App (全栈 AI 聊天应用):**
    * **架构:** 基于 GKE 与 Cloud Run 部署的云原生应用，集成 **MCP Server (Model Context Protocol)** 与多层 Agent Routing 技术，实现智能工具路由。
    * **亮点:** 利用 Cloud SQL 实现 AI Memory 增强，采用 Auth0 进行安全鉴权，前端支持 LLM 流式输出与 Markdown 实时渲染。*(Repo: github.com/nvd11/askc-backend)*
* **Automated AI Code Reviewer (基于 GitOps 的 AI 审查工具):**
    * **机制:** 开发 GitHub Webhook 服务，在 PR 创建时自动唤醒 Gemini LLM 及 WebAgent 进行深度代码走查，并将改进建议直接打入 PR Comment。
    * **企业级扩展:** 深度集成 Jira 和 Confluence 的 MCP 工具链，确保 AI 审查不仅关注代码规范，更对齐企业内部的业务上下文。该工具已成功推广至跨部门团队。

---

## 教育背景 (Education)
* **广东外语外贸大学** - 计算机科学与技术 (本科) | 2003.09 - 2007.07