import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("| **"):
        parts = line.split("|")
        pattern = parts[3].strip()
        
        # Standardize "File & API" and "API & File" to just "API & File"
        if pattern == "File & API":
            parts[3] = " API & File "
            lines[i] = "|".join(parts)
            
        # Also let's check for any "Database Connection & File" vs "File & Database Connection"
        if pattern == "Database Connection & File" or pattern == "File & Database Connection":
            parts[3] = " Database Connection & File "
            lines[i] = "|".join(parts)

with open(md_path, "w") as f:
    f.writelines(lines)

