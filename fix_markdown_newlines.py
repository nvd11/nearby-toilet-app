import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    # The header is broken: "| System Name | Full Name / Context | Integration Pattern Is Both Upstream & Downstream? | Remark |"
    # It misses a pipe between "Pattern" and "Is"
    if "| Integration Pattern Is Both Upstream & Downstream? |" in line:
        line = line.replace("| Integration Pattern Is Both Upstream & Downstream? |", "| Integration Pattern | Is Both Upstream & Downstream? |")
    
    # Also, there must be a blank line before the table for standard Markdown parsers to render it correctly
    if line.startswith("## ⬆️ Upstream Systems"):
        out.append(line)
        out.append("\n")
        continue
    
    if line.startswith("## ⬇️ Downstream Systems"):
        out.append("\n")
        out.append(line)
        out.append("\n")
        continue
        
    out.append(line)

with open(md_path, "w") as f:
    f.writelines(out)

