with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

# Pattern 3
old_p3 = """## 3. Downstream Pattern: RCDP -> Auth Views
**Total Estimated Effort: ~7.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. IAM & Access Control** | Create specific Google Groups and IAM roles/Service Accounts for downstream consumers (e.g., Qlik, Appian). | 1.0 |
| **2. View Development** | Develop BigQuery Authorized Views joining DV Satellites/Links to meet specific consumer business logic. | 3.0 |
| **3. Connection Support** | Assist downstream teams in configuring their GCP/BigQuery ODBC drivers and testing connectivity. | 1.5 |
| **4. Testing & Go-Live** | UAT sign-off from downstream users, finalize production permissions. | 1.5 |"""

new_p3 = """## 3. Downstream Pattern: RCDP -> Auth Views
**Total Estimated Effort: ~12.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. IAM & Access Control** | Create specific Google Groups and IAM roles/Service Accounts for downstream consumers (e.g., Qlik, Appian). | 1.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. View Development** | Develop BigQuery Authorized Views joining DV Satellites/Links to meet specific consumer business logic. | 3.0 |
| **4. Connection Support** | Assist downstream teams in configuring their GCP/BigQuery ODBC drivers and testing connectivity. | 1.5 |
| **5. Testing & Go-Live** | UAT sign-off from downstream users, finalize production permissions. | 1.5 |"""

# Pattern 4
old_p4 = """## 4. Downstream Pattern: RCDP -> File Export (NAS/SFTP)
**Total Estimated Effort: ~11.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Outbound Network** | Secure connectivity from GCP to target external NAS/SFTP servers. | 2.0 |
| **2. Extract Pipeline (Dataflow)** | Develop Dataflow/Cloud Run job to query BigQuery, format data into required file format (CSV/TXT), and upload. | 4.0 |
| **3. Testing & Reconciliation** | Validate file structures and content parity with legacy CDR exports. | 3.0 |
| **4. CI/CD & Prod Cut-over** | Job scheduling, deployment, and establishing failure-alerting workflows. | 2.0 |"""

new_p4 = """## 4. Downstream Pattern: RCDP -> File Export (NAS/SFTP)
**Total Estimated Effort: ~16.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Outbound Network** | Secure connectivity from GCP to target external NAS/SFTP servers. | 2.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. Extract Pipeline (Dataflow)** | Develop Dataflow/Cloud Run job to query BigQuery, format data into required file format (CSV/TXT), and upload. | 4.0 |
| **4. Testing & Reconciliation** | Validate file structures and content parity with legacy CDR exports. | 3.0 |
| **5. CI/CD & Prod Cut-over** | Job scheduling, deployment, and establishing failure-alerting workflows. | 2.0 |"""

content = content.replace(old_p3, new_p3)
content = content.replace(old_p4, new_p4)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
