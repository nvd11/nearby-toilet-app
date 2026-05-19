import json

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Looking for lines with "&" indicating multiple connection types.
    # The only valid ones should be explicitly verified.
    if "| **Whistleblow** |" in line and "## ⬇️" not in "".join(lines[:i]):
        lines[i] = line.replace("SFTP & File Based (via Connect Direct)", "File Based (via Connect Direct)")

with open(md_path, "w") as f:
    f.writelines(lines)
