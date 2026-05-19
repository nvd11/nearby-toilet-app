import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **My trades** |" in line:
        if "## ⬇️ Downstream Systems" not in "".join(lines[:i]):
            # This is the Upstream one. Change "DB Connection & Rest API" to just "DB Connection"
            lines[i] = line.replace("DB Connection & Rest API", "DB Connection")

with open(md_path, "w") as f:
    f.writelines(lines)
