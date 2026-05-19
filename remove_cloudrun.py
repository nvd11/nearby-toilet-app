import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Replace the specific GKE/Cloud Run mention
old_text = "Deploy backend microservices (Cloud Run/GKE) that mimic legacy API contracts"
new_text = "Deploy backend API microservices that mimic legacy API contracts"
content = content.replace(old_text, new_text)

with open(md_path, "w") as f:
    f.write(content)

