with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

new_p3 = """## 3. Upstream Pattern: API Pull (REST/SOAP) -> RCDP
**Total Estimated Effort: ~21.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Repository Setup** | Provision new terraform code repository for new upstream usecase. | 2.0 |
| **2. Infra & Connectivity** | Provision infrastructure (e.g., Cloud Scheduler, Cloud NAT) for API polling, configure Secret Manager for API credentials, and set up IAM. | 2.5 |
| **3. Connectivity Testing** | Perform end-to-end connectivity and authentication testing with upstream API endpoints. | 2.0 |
| **4. BQ dataset & table creation** | Design and execute BigQuery DDL scripts by Terraform for both Raw Layer and target Data Vault tables. | 2.0 |
| **5. Beam Pipeline (Dataflow)** | Develop Beam Pipeline to fetch data from API (handling pagination/rate limits) and write to BigQuery staging layer. | 5.0 |
| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |

---

"""

# Renumber downstream pattern 4 -> 5 first
content = content.replace("## 4. Downstream Pattern", "## 5. Downstream Pattern")
# Insert new upstream pattern 3 and renumber existing downstream pattern 3 -> 4
content = content.replace("## 3. Downstream Pattern", new_p3 + "## 4. Downstream Pattern")

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
