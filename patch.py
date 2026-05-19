import re

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

# BQ changes
content = content.replace("| Create auth view for CA user | **3** |", "| Create auth view for CA user | **2** |")
content = content.replace("| Build data dictionary and entitlement metrics | **2** |", "| Build data dictionary and entitlement metrics | **3** |")

# MLOps changes
mlops_addition = """| Standard Deploy for new model | **8** | Deploy ML model into CMLP execution env. |
| Prod deployment for model | **3** | Prod deployment tasks and verification. |
| Data migration for business release | **5** | Data migration effort required for business release. |"""
content = content.replace("| Standard Deploy for new model | **8** | Deploy ML model into CMLP execution env. |", mlops_addition)

# ETL changes
etl_addition = """| Medium ETL | **5** | Ingest data from staging dataset to a conformed dataset for a specific downstream system. May involve some view creation and SQL joins. May cover multiple tables. Incorporates logic for customer provider. |"""
content = re.sub(r'\| Medium ETL \| \*\*5\*\* \| Ingest data from staging dataset to a conformed dataset for a specific downstream system\. May involve some view creation and SQL joins\. May cover multiple tables\. \|', etl_addition, content)

# CI/CD changes
cicd_repl1 = """| CloudBuild configuration for Dataflow | **2** | Creating or modifying CloudBuild configurations for Dataflow pipeline deployments. Must cover Xmatter integration. (Specify if new lib or new pattern). |"""
content = content.replace("| CloudBuild configuration for Dataflow | **2** | Creating or modifying CloudBuild configurations for Dataflow pipeline deployments. |", cicd_repl1)

cicd_repl2 = """| CloudBuild configuration for Cloud Run API svc | **2** | Creating or modifying CloudBuild configurations for Cloud Run API service deployments. Must cover Xmatter integration. |"""
content = content.replace("| CloudBuild configuration for Cloud Run API svc | **2** | Creating or modifying CloudBuild configurations for Cloud Run API service deployments. |", cicd_repl2)

cicd_addition = """| CloudBuild configuration for Cloud Run API svc | **2** | Creating or modifying CloudBuild configurations for Cloud Run API service deployments. Must cover Xmatter integration. |
| CloudBuild configuration for Dataflow (new lib / new pattern) | **4** | Add a new test case for CloudBuild incorporating the new lib. Must cover Xmatter integration. |"""
content = content.replace(cicd_repl2, cicd_addition)

# GCP Infra
infra_addition1 = "| Modify BigQuery table schema | **2** | Update or modify existing BigQuery table schemas using Terraform. |"
content = content.replace("| Modify BigQuery table schema | **1** | Update or modify existing BigQuery table schemas using Terraform. |", infra_addition1)

infra_addition2 = """| Modify BigQuery table schema | **2** | Update or modify existing BigQuery table schemas using Terraform. |
| Data batch infrastructure | **TBD** | Provision data batch infrastructure. |
| Provision new code repository | **TBD** | Set up and configure new code repository. |"""
content = content.replace(infra_addition1, infra_addition2)

# E2E Auto testing
e2e_repl = "| Auto E2E PyBDD testing case for a use case | **8** | Develop automated end-to-end testing scenarios using PyBDD for a specific business use case. Includes effort for Prod violation fixes. |"
content = content.replace("| Auto E2E PyBDD testing case for a use case | **5** | Develop automated end-to-end testing scenarios using PyBDD for a specific business use case. |", e2e_repl)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
