import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# We need to add a new row to the Phase 2 table
old_table_end = "| **SFTP Server (VM) Provisioning** | RCDP Team | Provision a dedicated SFTP VM (Compute Engine) integrated with Cloud Storage (via GCSFuse). This provides a drop zone for PaaS upstreams unable to mount NAS or call APIs, landing files instantly in the data lake. |\n"

new_row = "| **Centralized Email / SMTP Dispatcher** | RCDP Team | Establish a centralized notification mechanism for downstream reporting. **Option 1:** RCDP builds a new, native common SendMail service (e.g., via Cloud Functions). **Option 2:** If CDR currently utilizes a standalone SendMail service, containerize and migrate that specific service to RCDP infrastructure. |\n"

new_table_end = old_table_end + new_row

content = content.replace(old_table_end, new_table_end)

with open(md_path, "w") as f:
    f.write(content)

