with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

# Pattern 1 updates
p1_old = """| **6. Data Vault (DV) Modeling & Dev** | Core data engineering: Map raw data to the Data Vault model and develop ETL to populate Hubs, Links, and Satellites. | 4.0 |
| **7. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **8. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

p1_new = """| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

content = content.replace(p1_old, p1_new)
content = content.replace("**Total Estimated Effort: ~28.0 Man-Days (MD)**", "**Total Estimated Effort: ~24.0 Man-Days (MD)**")

# Pattern 2 updates
p2_old = """| **6. Data Vault (DV) Modeling & Dev** | Transform raw event payloads into target Data Vault architecture. | 4.0 |
| **7. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **8. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

p2_new = """| **6. Support SIT/UAT Testing** | Collaborate with upstream teams to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | 3.0 |"""

content = content.replace(p2_old, p2_new)
content = content.replace("**Total Estimated Effort: ~25.5 Man-Days (MD)**", "**Total Estimated Effort: ~21.5 Man-Days (MD)**")

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
