with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

# Pattern 3
old_p3 = """## 3. Downstream Pattern: RCDP -> Auth Views
**Total Estimated Effort: ~12.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. IAM & Access Control** | Create specific Google Groups and IAM roles/Service Accounts for downstream consumers (e.g., Qlik, Appian). | 1.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. View Development** | Develop BigQuery Authorized Views joining DV Satellites/Links to meet specific consumer business logic. | 3.0 |
| **4. Connection Support** | Assist downstream teams in configuring their GCP/BigQuery ODBC drivers and testing connectivity. | 1.5 |
| **5. Testing & Go-Live** | UAT sign-off from downstream users, finalize production permissions. | 1.5 |"""

new_p3 = """## 3. Downstream Pattern: RCDP -> Auth Views
**Total Estimated Effort: ~14.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. IAM & Access Control** | Create specific Google Groups and IAM roles/Service Accounts for downstream consumers (e.g., Qlik, Appian). | 1.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. View Development** | Develop BigQuery Authorized Views joining DV Satellites/Links to meet specific consumer business logic. | 3.0 |
| **4. CI/CD for Dataflow/Deployment** | Set up CI/CD pipeline and deployment configurations for the Dataflow job. | 2.0 |
| **5. Connection Support** | Assist downstream teams in configuring their GCP/BigQuery ODBC drivers and testing connectivity. | 1.5 |
| **6. Testing & Go-Live** | UAT sign-off from downstream users, finalize production permissions. | 1.5 |"""

content = content.replace(old_p3, new_p3)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
