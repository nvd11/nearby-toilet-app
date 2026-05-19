with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_p2 = """## 2. Upstream Pattern: Event Driven (Pub/Sub) -> RCDP
**Total Estimated Effort: ~23.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Provision GCP Pub/Sub topics, subscriptions, Publisher service accounts, and configure IAM permissions. | 2.5 |
| **3. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **4. Beam Pipeline (Dataflow)** | Develop Beam Pipeline with Pub/Sub IO connector to stream events and write to BigQuery staging data layer. | 5.0 |
| **5. Data Vault (DV) Modeling & Dev** | Transform raw event payloads into target Data Vault architecture. | 4.0 |
| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

new_p2 = """## 2. Upstream Pattern: Event Driven (Pub/Sub) -> RCDP
**Total Estimated Effort: ~25.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Provision GCP Pub/Sub topics, subscriptions, Publisher service accounts, and configure IAM permissions. | 2.5 |
| **3. Connectivity Testing** | Perform end-to-end connectivity testing with upstream systems to ensure event publishing works correctly. | 2.0 |
| **4. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Develop Beam Pipeline with Pub/Sub IO connector to stream events and write to BigQuery staging data layer. | 5.0 |
| **6. Data Vault (DV) Modeling & Dev** | Transform raw event payloads into target Data Vault architecture. | 4.0 |
| **7. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **8. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

content = content.replace(old_p2, new_p2)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
