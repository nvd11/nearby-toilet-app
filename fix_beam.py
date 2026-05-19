with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

old_text = "| Develop Beam custom provider | **TBD** | Write custom provider for Beam YAML data ingestion. |"
new_text = "| Develop Beam custom provider | **5** | Write custom provider for Beam YAML data ingestion. |"
content = content.replace(old_text, new_text)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
