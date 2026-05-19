with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_p1 = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~24.0 Man-Days (MD)**

| Task Breakdown | Description | Owner | Est. (MD) |
| :--- | :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | RCDP | 2.0 |
| **2. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | RCDP | 5.0 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | RCDP | 2.0 |
| **4. Landing Pipeline** | Build ingestion pipeline from NAS/SFTP landing path to RCDP landing bucket. | RCDP | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Build Beam Pipeline (Dataflow) from landing bucket to BQ staging data layer. | RCDP | 5.0 |
| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | RCDP | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **Total** | | | ****24.0**** |"""

new_p1 = """## 1. Upstream Pattern: File (NAS/SFTP) -> RCDP
**Total Estimated Effort: ~26.0 Man-Days (MD)**

| Task Breakdown | Description | Owner | Est. (MD) |
| :--- | :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | RCDP | 2.0 |
| **2. Infra & Connectivity** | Set up GCS bucket, Storage Transfer Service, service account, IAM configuration, etc. | RCDP | 5.0 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | RCDP | 2.0 |
| **4. Landing Pipeline** | Build ingestion pipeline from NAS/SFTP landing path to RCDP landing bucket. | RCDP | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Build Beam Pipeline (Dataflow) from landing bucket to BQ staging data layer. | RCDP | 5.0 |
| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | RCDP | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **8. Shutdown Legacy Jobs** | Shutdown legacy CDR file loading jobs to prevent conflicts. | CDR | 2.0 |
| **Total** | | | ****26.0**** |"""

content = content.replace(old_p1, new_p1)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
