with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "r") as f:
    content = f.read()

# Revert the wrong addition
wrong_line = "| Medium ETL | **5** | Ingest data from staging dataset to a conformed dataset for a specific downstream system. May involve some view creation and SQL joins. May cover multiple tables. Incorporates logic for customer provider. |"
correct_line = "| Medium ETL | **5** | Ingest data from staging dataset to a conformed dataset for a specific downstream system. May involve some view creation and SQL joins. May cover multiple tables. |"
content = content.replace(wrong_line, correct_line)

# Add the new row at the end of the ETL table
target = "| Support upstream/downstream E2E testing | **5** | Collaborate with upstream data providers and downstream consumers for end-to-end integration testing. |"
new_row = "| Develop Beam custom provider | **TBD** | Write custom provider for Beam YAML data ingestion. |"
content = content.replace(target, target + "\n" + new_row)

with open("rcdp-agile-metrics/RCDP_Story_Points_Matrix.md", "w") as f:
    f.write(content)
