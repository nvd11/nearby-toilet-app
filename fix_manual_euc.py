import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/MEETING_MINUTES_AJIT.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **f. Manual EUC (Rekey / Upload)** |" in line:
        new_desc = "**Business Process Change.** Excel shows manual processes (e.g., M2799, PQM). RCDP is a backend data platform and does not provide UI/SFTP for end-users, nor can human users access Prod GCS buckets directly due to InfoSec controls. These business users must transition to connecting Excel/BI tools directly to BQ Auth Views, or a new intermediary frontend/SharePoint dropzone must be built by the business."
        lines[i] = f"| **f. Manual EUC (Rekey / Upload)** | {new_desc} | 🔴 High (Process) |\n"

with open(md_path, "w") as f:
    f.writelines(lines)
