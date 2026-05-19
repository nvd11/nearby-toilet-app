import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# The specific clause to remove
clause_to_remove = r"3\.\s+\*\*Fast-Track InfoSec Approvals:\*\* Creation of the RCDP SFTP server, firewall rule changes, and Service Account provisioning must bypass standard queues via a VIP fast-track process\.\n"

content = re.sub(clause_to_remove, "", content)

# Re-number the remaining clause (4 becomes 3)
content = re.sub(r"4\.\s+\*\*Transformation Logic Portability:\*\*", r"3. **Transformation Logic Portability:**", content)

with open(md_path, "w") as f:
    f.write(content)

