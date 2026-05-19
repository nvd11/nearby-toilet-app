import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out_lines = []
in_matrix = False

for line in lines:
    if line.startswith("### 3.1 Downstream Case-by-Case Execution Matrix"):
        in_matrix = True
        out_lines.append(line)
    elif line.startswith("## Phase 4:"):
        in_matrix = False
        out_lines.append(line)
    elif in_matrix and line.startswith("| # | Downstream Consumer"):
        out_lines.append("| # | Downstream Consumer (Target) | Downstream Provisioning Pattern (Action Required) | Upstream Dependencies (Ingestion Workload) | Upstream Data Visa (Prerequisite) |\n")
    elif in_matrix and line.startswith("| :---: | :--- | :--- | :--- |"):
        out_lines.append("| :---: | :--- | :--- | :--- | :--- |\n")
    elif in_matrix and line.startswith("| ") and line.split("|")[1].strip().isdigit():
        parts = line.split("|")
        # Add new column at the end
        parts.insert(-1, " *Pending review* ")
        out_lines.append("|".join(parts))
    else:
        out_lines.append(line)

with open(md_path, "w") as f:
    f.writelines(out_lines)

