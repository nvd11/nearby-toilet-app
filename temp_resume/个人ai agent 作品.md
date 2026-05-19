# 个人简介 (Profile Summary)

- 资深全栈与AI开发专家 - 拥有10年以上Java开发及架构经验，4年以上Python开发经验。精通Python异步高性能编程，专注于构建高并发、低延迟的云原生应用。
- AI Agent与大模型应用 -熟悉 AI Agent 开发，熟练使用 LangChain 框架构建基于 ReAct 模式 or 原生 function call的智能代理。具备开发及部署 MCP Server (Model Context Protocol) 的实战经验，致力于将LLM能力与企业业务流程深度集成。
- Public Cloud (GCP) 专家 - 深度掌握 Google cloud 公有云生态，熟练运用 GKE, Cloud Run, Dataflow, Pub/Sub, MIG, GCS 等核心组件。具备复杂的 VPC 网络规划及 IAM 安全配置能力，能充分利用云原生优势优化系统架构。
- 微服务与架构设计- 深谙微服务架构设计，精通 Spring Cloud/Spring Boot 生态及 JPA/Mockito 等框架。具有将传统银行单体应用迁移至微服务架构的丰富经验，擅长编写高质量的技术方案与文档。
- DevOps与云原生工程 - 具备深厚的 DevOps 实践经验，熟练掌握 K8s/GKE 资源编排。能主导设计并实施基于 Terraform, GitHub Webhook, Jenkins Libs/CloudBuild 的自动化 CI/CD 流水线，显著提升交付效率。
- 数据工程与MLOps - 熟悉大数据与 MLOps 流程，拥有从零构建基于 BigQuery 的市场风险数据仓库（ETL/数据分层）经验，以及搭建 Kubeflow 平台进行机器学习模型部署的能力。
- 全球化团队领导力 - 具备优秀的双语（中/英）沟通能力，日常主导全球团队的英文会议。能够带领团队按时高质量交付任务，并与终端用户保持卓越的合作关系。
- 数据处理技术 - 精通基于 Google Cloud (Dataflow, Pub/Sub, BigQuery) 的云原生海量数据处理架构，熟练构建 Streaming/Batch ETL 流程。同时精通 Oracle, PostgreSQL 等主流数据库及 SQL 性能调优。

# 开源项目 (Open Source Projects)

- Agentic Web Chat-App (Full Stack AI Chat Application)
  - 项目演示: https://gateway.jpgcp.cloud/askc-ui (支持 GitHub OAuth2 登录)
  - 后端架构: 集成 MCP Server (GitHub MCP) 与多层 Agent Routing 技术，实现基于语境的智能路由。利用 Cloud SQL 数据库集成 AI 记忆增强 (Memory Enhancement) 能力，提供持久化的上下文支持。并采用 Auth0 实现 OAuth2 安全鉴权。(Backend Repo: https://github.com/nvd11/askc-backend)
  - 前端交互: 构建现代化的响应式布局界面，支持 LLM 流式输出 (Streaming) 及 Markdown 实时渲染，提供极致的对话体验。(Frontend Repo: https://github.com/nvd11/askc-ui)
  - 云原生部署: 基于 Google GKE 容器化部署，利用 Cloud Build 实现全自动化的 CI/CD 持续交付。

- Automated AI Code Reviewer (GitHub App)
  - 项目地址: https://github.com/nvd11/py-webhook-svc
  - 核心功能: 开发了一款基于 GitOps 模式的自动化 Code Review 工具。当 PR 创建时，自动触发 Webhook 调用 Gemini LLM 及 WebAgent 对代码变更进行深度审查，并将 Review 结果与建议自动反馈至 PR Comment。
  - 企业级扩展: 集成 Jira 和 Confluence 的 MCP Tools，构建定制化的 AI Agent，能基于内部规范与业务需求进行高精度 Code Review。该企业版已成功推广至公司内部多个其他部门团队使用，显著提升了代码审核效率。
