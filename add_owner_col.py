with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    if line.startswith("| Task Breakdown |"):
        new_lines.append("| Task Breakdown | Description | Owner | Est. (MD) |\n")
    elif line.startswith("| :--- | :--- | :--- |"):
        new_lines.append("| :--- | :--- | :--- | :--- |\n")
    elif line.startswith("| **Total**"):
        # Total row needs to pad an extra column
        parts = line.strip().split('|')
        if len(parts) >= 4:
            new_lines.append(f"| **Total** | | | **{parts[3].strip()}** |\n")
        else:
            new_lines.append(line)
    elif line.startswith("| **"):
        # Data rows
        parts = line.strip().split('|')
        if len(parts) >= 4:
            new_lines.append(f"| {parts[1].strip()} | {parts[2].strip()} | RCDP | {parts[3].strip()} |\n")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.writelines(new_lines)
