with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    content = f.read()

old_header = "## 3. Downstream Pattern: RCDP -> Auth Views (ODBC/JDBC)"
new_header = "## 3. Downstream Pattern: RCDP -> Auth Views"
content = content.replace(old_header, new_header)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.write(content)
