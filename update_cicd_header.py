with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

old_header = "### CI/CD Setup"
new_header = "### CI/CD Pipeline Setup & Testing Env Deployment"
content = content.replace(old_header, new_header)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
