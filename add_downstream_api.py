with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

new_p6 = """
---

## 6. Downstream Pattern: RCDP -> API Provision (REST)
**Total Estimated Effort: ~20.5 Man-Days (MD)**

| Task Breakdown | Description | Est. (MD) |
| :--- | :--- | :--- |
| **1. Infra & Connectivity** | Provision infrastructure (e.g., Cloud Run, API Gateway) and configure IAM/Security for API endpoints. | 2.0 |
| **2. Beam ETL Pipeline (Dataflow)** | Develop Beam ETL Dataflow job to transform data from staging layer to conformed layer. | 5.0 |
| **3. API Service Development** | Develop API service (FastAPI / SpringBoot) to serve data from BigQuery to downstream consumers. | 5.0 |
| **4. CI/CD for API/Deployment** | Set up CI/CD pipeline and deployment configurations for the API service. | 2.0 |
| **5. Connection Support** | Assist downstream teams in testing and verifying API connectivity and authentication. | 1.5 |
| **6. Support SIT/UAT Testing** | Collaborate with downstream consumers to support SIT/UAT testing, including data parity checks and reconciliation. | 5.0 |
"""

content += new_p6

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
