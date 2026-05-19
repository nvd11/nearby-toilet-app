import re

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Modify Pattern 1
pattern1_old = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~26.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | 5.0 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **4. Landing Pipeline** | Build ingestion pipeline from NAS/SFTP landing path to RCDP landing bucket. | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Build Beam Pipeline (Dataflow) from landing bucket to BQ staging data layer. | 5.0 |
| **6. Data Vault (DV) Modeling & Dev** | Core data engineering: Map raw data to the Data Vault model and develop ETL to populate Hubs, Links, and Satellites. | 4.0 |
| **7. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **8. CI/CD & Prod Cut-over** | Create Jenkins/GitLab CI/CD pipelines, configure Cloud Scheduler/Airflow, and set up alerting mechanisms. | 1.5 |"""

pattern1_new = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~28.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | 5.0 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **4. Landing Pipeline** | Build ingestion pipeline from NAS/SFTP landing path to RCDP landing bucket. | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Build Beam Pipeline (Dataflow) from landing bucket to BQ staging data layer. | 5.0 |
| **6. Data Vault (DV) Modeling & Dev** | Core data engineering: Map raw data to the Data Vault model and develop ETL to populate Hubs, Links, and Satellites. | 4.0 |
| **7. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **8. CI/CD Pipeline Setup** | CI/CD pipeline setup for new terraform and dataflow pipelines, including deployment configuration. | 3.0 |"""

content = content.replace(pattern1_old, pattern1_new)

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'w', encoding='utf-8') as f:
    f.write(content)
