with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

# Update Infra from 2.5 to 3.0
old_infra = "| **2. Infra & Connectivity** | Provision infrastructure (e.g., Cloud Scheduler, Cloud NAT) for API polling, configure Secret Manager for API credentials, and set up IAM. | 2.5 |"
new_infra = "| **2. Infra & Connectivity** | Provision infrastructure (e.g., Cloud Scheduler, Cloud NAT) for API polling, configure Secret Manager for API credentials, and set up IAM. | 3.0 |"
content = content.replace(old_infra, new_infra)

# Update Total from 21.5 to 22.0
old_total = """## 3. Upstream Pattern: API Pull (REST/SOAP) -> RCDP
**Total Estimated Effort: ~21.5 Man-Days (MD)**"""
new_total = """## 3. Upstream Pattern: API Pull (REST/SOAP) -> RCDP
**Total Estimated Effort: ~22.0 Man-Days (MD)**"""
content = content.replace(old_total, new_total)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
