md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
        out.append(line)
    elif line.startswith("## ⬇️"):
        mode = "down"
        out.append(line)
    elif line.startswith("| **"):
        # We need to replace "Excel" with "Excel ('Upstream' sheet)" or "Excel ('Downstream' sheet)"
        sheet = "Upstream" if mode == "up" else "Downstream"
        
        if "Diagram & Excel" in line:
            new_line = line.replace("Diagram & Excel", f"Diagram & Excel ('{sheet}' sheet)")
        elif "Source: Excel" in line:
            new_line = line.replace("Source: Excel", f"Source: Excel ('{sheet}' sheet)")
        else:
            new_line = line
        out.append(new_line)
    else:
        out.append(line)

with open(md_path, "w") as f:
    f.writelines(out)

