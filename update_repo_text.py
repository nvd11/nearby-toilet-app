with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

old_text = "| Provision new code repository | **2** | Set up and configure new code repository. |"
new_text = "| Provision new code repository for new upstream usecase | **2** | Set up and configure new code repository. |"
content = content.replace(old_text, new_text)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
