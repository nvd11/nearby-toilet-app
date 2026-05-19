import re

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'r', encoding='utf-8') as f:
    content = f.read()

# For Upstream tables: insert a new row at the beginning (before Repository Setup)
# For Downstream tables: insert a new row at the beginning (before IAM & Access Control / Infra & Outbound Network / Infra & Connectivity)

# We will just write a simple replacement logic to add the new row to all 6 tables and update the totals.

new_content = ""
lines = content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    
    # Update Totals in headers
    if "**Total Estimated Effort: ~34.0 Man-Days (MD)**" in line:
        line = line.replace("34.0", "37.0")
    elif "**Total Estimated Effort: ~29.5 Man-Days (MD)**" in line:
        line = line.replace("29.5", "32.5")
    elif "**Total Estimated Effort: ~30.0 Man-Days (MD)**" in line:
        line = line.replace("30.0", "33.0")
    elif "**Total Estimated Effort: ~17.5 Man-Days (MD)**" in line:
        line = line.replace("17.5", "20.5")
    elif "**Total Estimated Effort: ~19.5 Man-Days (MD)**" in line:
        line = line.replace("19.5", "22.5")
    elif "**Total Estimated Effort: ~20.5 Man-Days (MD)**" in line:
        line = line.replace("20.5", "23.5")
        
    # Update totals in footers
    elif "| **Total** | | | ****34.0**** |" in line:
        line = line.replace("34.0", "37.0")
    elif "| **Total** | | | ****29.5**** |" in line:
        line = line.replace("29.5", "32.5")
    elif "| **Total** | | | ****30.0**** |" in line:
        line = line.replace("30.0", "33.0")
    elif "| **Total** | | | ****17.5**** |" in line:
        line = line.replace("17.5", "20.5")
    elif "| **Total** | | | ****19.5**** |" in line:
        line = line.replace("19.5", "22.5")
    elif "| **Total** | | | ****20.5**** |" in line:
        line = line.replace("20.5", "23.5")

    # Insert the new task right after the table separator line
    new_content += line + "\n"
    if line.strip() == "| :--- | :--- | :--- | :--- |":
        new_row = "| **0. RCDP & BA Communication** | Communicate with upstream/downstream teams and BAs to clarify data scope and requirements. | RCDP | 3.0 |"
        new_content += new_row + "\n"

    i += 1

with open('./cdr-demise-docs/plans/Estimation_Baselines.md', 'w', encoding='utf-8') as f:
    f.write(new_content)
