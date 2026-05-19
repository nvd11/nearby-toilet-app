import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **CIMT** |" in line and "## ⬇️ Downstream Systems" in "".join(lines[:i]):
        lines[i] = line.replace("Database View / Extract (TBC)", "Rest API")

with open(md_path, "w") as f:
    f.writelines(lines)
