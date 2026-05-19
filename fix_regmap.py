import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **RegMap** |" in line:
        if "## ⬇️ Downstream Systems" not in "".join(lines[:i]):
            # This is the Upstream one. Change "DB Connection & SFTP" to just "SFTP"
            lines[i] = line.replace("DB Connection & SFTP", "SFTP")

with open(md_path, "w") as f:
    f.writelines(lines)
