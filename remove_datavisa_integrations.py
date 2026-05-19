import re

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
    elif mode == "up" and line.startswith("| System Name |"):
        out_lines.append(line.replace("| Data Visa | ", ""))
    elif mode == "up" and line.startswith("| :--- | :--- | :--- | :--- | :---: |"):
        out_lines.append(line.replace("| :--- | :--- | :--- | :--- | :---: |", "| :--- | :--- | :--- | :---: |"))
    elif mode == "up" and line.startswith("| **"):
        parts = line.split("|")
        # Remove the element at index 4 (" TBD ")
        del parts[4]
        out_lines.append("|".join(parts))
    else:
        out_lines.append(line)

with open(md_path, "w") as f:
    f.writelines(out_lines)

