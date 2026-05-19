with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_cicd = "| **4. CI/CD for API/Deployment** | Set up CI/CD pipeline and deployment configurations for the API service. | 2.0 |"
new_cicd = "| **4. CI/CD for API & Dataflow/Deployment** | Set up CI/CD pipeline and deployment configurations for the API service and the Dataflow job. | 2.0 |"

content = content.replace(old_cicd, new_cicd)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
