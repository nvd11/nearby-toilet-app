with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

content = content.replace("| Data batch infrastructure | **TBD** | Provision data batch infrastructure. |", "| Data batch infrastructure | **2** | Provision data batch infrastructure. |")
content = content.replace("| Provision new code repository | **TBD** | Set up and configure new code repository. |", "| Provision new code repository | **2** | Set up and configure new code repository. |")

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
