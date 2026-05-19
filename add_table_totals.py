import re

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "r") as f:
    lines = f.readlines()

new_lines = []
in_table = False
current_total = "0.0"

for line in lines:
    match = re.search(r'\*\*Total Estimated Effort: ~([\d\.]+)\s*Man-Days', line)
    if match:
        current_total = match.group(1)
        
    is_table_line = line.strip().startswith('|')
    
    if in_table and not is_table_line:
        # Reached the end of the table
        new_lines.append(f"| **Total** | | **{current_total}** |\n")
        in_table = False
        
    if is_table_line:
        in_table = True
        
    new_lines.append(line)

# If file ends with a table
if in_table:
    new_lines.append(f"| **Total** | | **{current_total}** |\n")

with open("cdr-demise-docs/plans/Estimation_Baselines.md", "w") as f:
    f.writelines(new_lines)
