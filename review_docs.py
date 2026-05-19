import re

files = [
    "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md",
    "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md",
    "/home/gateman/.openclaw/workspace/cdr-demise-docs/MEETING_MINUTES_AJIT.md",
    "/home/gateman/.openclaw/workspace/cdr-demise-docs/EMAIL_DRAFT_TO_AJIT.md"
]

missing_items = []

for file in files:
    with open(file, "r") as f:
        content = f.read()
        if "TBD" in content or "TBC" in content or "Pending" in content or "Unknown" in content or "Action for Ajit" in content:
            missing_items.append(f"Found unresolved tags in {file.split('/')[-1]}")

print("Review completed.")
for item in missing_items:
    print(item)

