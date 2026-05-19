import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

tbc_items = []
for line in lines:
    if "TBC" in line:
        parts = line.split("|")
        if len(parts) >= 4:
            sys_name = parts[1].replace("**", "").strip()
            pattern = parts[3].strip()
            tbc_items.append((sys_name, pattern))

print("TBC Items:")
for sys, pat in tbc_items:
    print(f"- {sys}: {pat}")

