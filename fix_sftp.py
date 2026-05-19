import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    content = f.read()

# Update known SFTP systems based on the diagram extraction
sftp_systems = ["RegMap", "IRIS", "Engage2", "Whistleblow", "HashiCorp Vault", "Manual Feed Reference Data"]
nas_systems = ["NAS"]

# Update the markdown content
lines = content.split('\n')
for i, line in enumerate(lines):
    if "| **" in line and "## ⬇️ Downstream" not in "\n".join(lines[:i]):
        # We are in the Upstream table
        sys_name = line.split("|")[1].strip().strip("*")
        
        # We need to change the integration pattern column (index 3)
        parts = line.split("|")
        pattern = parts[3].strip()
        
        if sys_name in sftp_systems:
            if "DB Connection" in pattern:
                pattern = pattern.replace("DB Connection", "SFTP")
            elif "Batch (TBC)" in pattern:
                pattern = "SFTP"
            elif "Rest API" in pattern:
                pattern = pattern + " & SFTP"
            else:
                pattern = "SFTP"
        elif sys_name in nas_systems:
            pattern = "NAS"
            
        parts[3] = f" {pattern} "
        lines[i] = "|".join(parts)

with open(md_path, "w") as f:
    f.write("\n".join(lines))

