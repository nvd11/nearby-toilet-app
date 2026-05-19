import re

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

# Pattern 1
old_p1 = """| **8. Shutdown Legacy Jobs** | Shutdown legacy CDR file loading jobs to prevent conflicts. | CDR | 2.0 |
| **Total** | | | ****26.0**** |"""
new_p1 = """| **8. Shutdown Legacy Jobs** | Shutdown legacy CDR file loading jobs to prevent conflicts. | CDR | 2.0 |
| **9. Historical Data Migration** | Migrate corresponding upstream historical data from CDR to RCDP. | CDR | 8.0 |
| **Total** | | | ****34.0**** |"""
content = content.replace(old_p1, new_p1)
content = content.replace("Total Estimated Effort: ~26.0 Man-Days (MD)", "Total Estimated Effort: ~34.0 Man-Days (MD)")

# Pattern 2
old_p2 = """| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **Total** | | | ****21.5**** |"""
new_p2 = """| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **8. Historical Data Migration** | Migrate corresponding upstream historical data from CDR to RCDP. | CDR | 8.0 |
| **Total** | | | ****29.5**** |"""
content = content.replace(old_p2, new_p2)
content = content.replace("Total Estimated Effort: ~21.5 Man-Days (MD)", "Total Estimated Effort: ~29.5 Man-Days (MD)")

# Pattern 3
old_p3 = """| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **Total** | | | ****22.0**** |"""
new_p3 = """| **7. CI/CD Pipeline Setup & Testing Env Deployment** | CI/CD pipeline setup for new terraform and dataflow pipelines, including testing env deployment. | RCDP | 3.0 |
| **8. Historical Data Migration** | Migrate corresponding upstream historical data from CDR to RCDP. | CDR | 8.0 |
| **Total** | | | ****30.0**** |"""
content = content.replace(old_p3, new_p3)
content = content.replace("Total Estimated Effort: ~22.0 Man-Days (MD)", "Total Estimated Effort: ~30.0 Man-Days (MD)")

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
