with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_p4 = """## 4. Downstream Pattern: RCDP -> File Export (NAS/SFTP)
**Total Estimated Effort: ~16.0 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Outbound Network** | Secure connectivity from GCP to target external NAS/SFTP servers. | 2.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. Extract Pipeline (Dataflow)** | Develop Dataflow/Cloud Run job to query BigQuery, format data into required file format (CSV/TXT), and upload. | 4.0 |
| **4. Testing & Reconciliation** | Validate file structures and content parity with legacy CDR exports. | 3.0 |
| **5. CI/CD & Prod Cut-over** | Job scheduling, deployment, and establishing failure-alerting workflows. | 2.0 |"""

new_p4 = """## 4. Downstream Pattern: RCDP -> File Export (NAS/SFTP)
**Total Estimated Effort: ~19.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Outbound Network** | Secure connectivity from GCP to target external NAS/SFTP servers. | 2.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. Extract Pipeline (Dataflow)** | Develop Dataflow/Cloud Run job to query BigQuery, format data into required file format (CSV/TXT), and upload. | 4.0 |
| **4. CI/CD for Dataflow/Deployment** | Set up CI/CD pipeline and deployment configurations for the Dataflow job. | 2.0 |
| **5. Connection Support** | Assist downstream teams in testing and verifying target NAS/SFTP connectivity. | 1.5 |
| **6. Support SIT/UAT Testing** | Collaborate with downstream consumers to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |"""

content = content.replace(old_p4, new_p4)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
