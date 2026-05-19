with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Support SIT/UAT Testing" in line:
        line = line.replace("| RCDP | 5.0 |", "| RCDP & CDR | 5.0 |")
    new_lines.append(line)

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.writelines(new_lines)
