# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** Jason (中文名：潘文林)
- **What to call them:** Boss
- **Pronouns:** He/Him
- **Timezone:** Beijing Time (UTC+8) - Confirmed on 2026-05-18 CST.
- **Education:** 广东外语外贸大学 - 计算机科学与技术 (2003-2007)
- **Experience:** 17 years (10+ in Finance Tech & Risk Compliance)
- **Line Manager:** Mona (Strict female boss)
- **Notes:** Likes a playful, sexy secretary vibe.

## Professional Background
- **Industry:** Finance IT (entire career post-graduation).
- **Core Tech Stack:** Java (early career), deeply specialized in GCP (BigQuery, Cloud Storage, Dataflow/Apache Beam, Cloud Scheduler, Pub/Sub, Cloud Run, SpringBoot, Python FastAPI).

### Career History
- **2018/06 - Present: HSBC Software Development (Guangdong) Co., Ltd**
  - **Role:** Technical/R&D Manager (ITSO for RC Data Platform).
  - *Context:* Finally joined HSBC as a full-time employee. Built and maintained a stable, high-efficiency dev team. Negotiated priorities with POs, led technical design, managed DevSecOps automation, supported production batches, and collaborated with bank audit teams.
  - *Team Metrics:* Developers average ~8 Jira story points per sprint consistently (sustained for over a year).
- **2017/11 - 2018/06: AIA IT Guangzhou Branch**
  - **Role:** Senior Software Engineer.
  - *Context:* Converted from vendor to in-house (AIA). Maintained legacy Compass system and developed new Coast system.
- **2016/12 - 2017/11: Shanghai Wicresoft Co., Ltd (Outsourced to AIA)**
  - **Role:** System Engineer.
  - *Context:* Handled Compass system maintenance and Coast system transition/support. Wrote Technical Design documents, performed code reviews, and managed UAT/production support.
- **2011/03 - 2016/12: Tata Consultancy Services (TCS) Shenzhen Branch (Outsourced to HSBC)**
  - **Role:** Senior Software Engineer.
  - *Context:* Started out as an outsourced vendor for HSBC. Designed business classes/DB schemas, mentored junior devs, improved dev processes (auto-testing, one-click deployments). Jumped to AIA in 2016 due to lack of conversion opportunities at the time.

## Key Projects & Responsibilities
### Current: RCDP & MLOps (HSBC)
- Leads architecture, tech selection, and code reviews.
- Strategic Goal: RCDP is built to replace the department's legacy data warehouse, Compliance Data Repository (CDR), which is an on-premise framework based on Oracle.
- **Current Major Initiative (CDR Demise):** Tasked by management to collaborate with CDR Tech Lead (Ajit) to formulate a comprehensive "demise plan" migrating all upstream/downstream integrations from CDR (on-prem Oracle + Informatica) to RCDP (GCP).
  - *Key Architectural Decisions:* 
    1. **ETL:** Rewrite legacy Informatica mappings into Dataflow to follow RCDP's standard pattern.
    2. **Ingestion:** CDC (GoldenGate) replication is currently difficult to implement directly in BigQuery; will need a workaround or pattern shift for real-time upstream feeds.
    3. **Downstream:** Downstream BI tools (Qlik) will not be rebuilt. Downstream teams will be responsible for repointing their Qlik connections to RCDP's BigQuery Auth Views.
- Manages data ingestion (streaming & batch) and downstream data provisioning (BigQuery Auth Views, REST APIs).
- **MLOps:** Operationalizes ML models (PyTorch) trained by Data Scientists on CMLP. Handles deployment, testing, and production monitoring.

### Selected AI & Validation Projects (Open Source & GKE Apps)
- **Enterprise Compliance Assistant (Project ADA - RAG Agent):**
  - *Description:* Enterprise-level RAG application built with LangChain and GCP to assist compliance officers in querying global policies.
  - *Validation Contribution:* Designed an automated evaluation mechanism based on a "Golden Dataset". Quantitatively evaluates RAG response quality by calculating Semantic Similarity and Factuality metrics. *(Note: This replaces the previous fabricated Model Evaluation API details, capturing the real RAG/GKE scope).*
- **Automated AI Code Reviewer:**
  - *Description:* Intelligent code review Agent integrating GitHub Webhook with Gemini LLM.
  - *Validation Contribution:* Introduced a "Human-in-the-loop" mechanism, collecting developer feedback to fine-tune prompt strategies, continuously improving the accuracy and adoption rate of code suggestions.

### Previous: GCMS (2021/08 - 2023/04)
- **Role:** China Team Manager (POD of 9).
- Driven major Agile transformations, reducing delivery cycles to 2 weeks.
- Implemented CI/CD pipelines (Jenkins/Ansible), feature toggles, blue-green deployments, and migrated to Spring Cloud microservices. Boosted automated testing to 70%.

### Previous: QuickApp (2021/02 - 2021/08)
- **Role:** Pod Lead.
- Built a Python Django web platform to replace traditional Excel Macro EUCs for APAC risk reporting users.

## Personal Interests & Career Goals
- Passionate about **AI Agent development** (using Langchain).
- Built internal SDLC tools: PR auto-reviewer, Jira/Confluence agent web chat apps.
- **Next Career Goal:** Wants his next job to be heavily focused on AI Agent technology.
- **HSBC Email:** jason1.pan@hsbc.com.hk
