import re

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Modify Pattern 1
pattern1_old = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~18.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | 5.0 |
| **2. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **3. Ingestion Pipeline (Dataflow)** | Develop Dataflow job to read files from GCS, perform format validation, cleanse data, and load into BigQuery Raw Layer. | 3.0 |
| **4. Data Vault (DV) Modeling & Dev** | Core data engineering: Map raw data to the Data Vault model and develop ETL to populate Hubs, Links, and Satellites. | 4.0 |
| **5. Testing & Reconciliation** | SIT/UAT execution, write SQL reconciliation scripts to ensure data parity between RCDP and legacy CDR. | 3.0 |
| **6. CI/CD & Prod Cut-over** | Create Jenkins/GitLab CI/CD pipelines, configure Cloud Scheduler/Airflow, and set up alerting mechanisms. | 1.5 |"""

pattern1_new = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~20.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | 5.0 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **4. Ingestion Pipeline (Dataflow)** | Develop Dataflow job to read files from GCS, perform format validation, cleanse data, and load into BigQuery Raw Layer. | 3.0 |
| **5. Data Vault (DV) Modeling & Dev** | Core data engineering: Map raw data to the Data Vault model and develop ETL to populate Hubs, Links, and Satellites. | 4.0 |
| **6. Testing & Reconciliation** | SIT/UAT execution, write SQL reconciliation scripts to ensure data parity between RCDP and legacy CDR. | 3.0 |
| **7. CI/CD & Prod Cut-over** | Create Jenkins/GitLab CI/CD pipelines, configure Cloud Scheduler/Airflow, and set up alerting mechanisms. | 1.5 |"""

content = content.replace(pattern1_old, pattern1_new)

# Modify Pattern 2
pattern2_old = """## 2. Upstream Pattern: Database (JDBC/ODBC) -> RCDP
**Total Estimated Effort: ~17.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Connectivity** | Network peering, VPN/Interconnect setup for GCP to access on-prem databases, DB credential management (Secret Manager). | 2.5 |
| **2. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **3. Ingestion Pipeline (Dataflow)** | Develop Dataflow job with JDBC connector to extract data (full/incremental load) and write to BigQuery Raw Layer. | 4.0 |
| **4. Data Vault (DV) Modeling & Dev** | Transform raw DB tables into target Data Vault architecture. | 4.0 |
| **5. Testing & Reconciliation** | Data parity checks against source systems. | 3.0 |
| **6. CI/CD & Prod Cut-over** | Pipeline deployment, scheduling, and monitoring. | 1.5 |"""

pattern2_new = """## 2. Upstream Pattern: Database (JDBC/ODBC) -> RCDP
**Total Estimated Effort: ~19.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Network peering, VPN/Interconnect setup for GCP to access on-prem databases, DB credential management (Secret Manager). | 2.5 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **4. Ingestion Pipeline (Dataflow)** | Develop Dataflow job with JDBC connector to extract data (full/incremental load) and write to BigQuery Raw Layer. | 4.0 |
| **5. Data Vault (DV) Modeling & Dev** | Transform raw DB tables into target Data Vault architecture. | 4.0 |
| **6. Testing & Reconciliation** | Data parity checks against source systems. | 3.0 |
| **7. CI/CD & Prod Cut-over** | Pipeline deployment, scheduling, and monitoring. | 1.5 |"""

content = content.replace(pattern2_old, pattern2_new)

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'w', encoding='utf-8') as f:
    f.write(content)
