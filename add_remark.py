import sys

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out_lines = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
        out_lines.append(line)
    elif line.startswith("## ⬇️"):
        mode = "down"
        out_lines.append(line)
    elif line.startswith("| System Name |"):
        out_lines.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? | Remark |\n")
    elif line.startswith("| :--- |"):
        out_lines.append("| :--- | :--- | :--- | :---: | :--- |\n")
    elif line.startswith("| **"):
        parts = [p.strip() for p in line.split("|")]
        sys_name = parts[1].strip("* ")
        remark = "-"
        
        if sys_name == "NAS" and mode == "down":
            remark = "Shared Drive accessed manually by Users / Auditors"
        elif sys_name == "NAS" and mode == "up":
            remark = "Manual file drops via NAS Path"
        
        new_row = f"| {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]} | {remark} |\n"
        out_lines.append(new_row)
    else:
        out_lines.append(line)

with open(md_path, "w") as f:
    f.writelines(out_lines)

