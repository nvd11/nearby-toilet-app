import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("| ") and "---" not in line and "System Name" not in line:
        parts = line.split("|")
        # Ensure it has exactly 7 segments after split: '', ' Sys ', ' Full ', ' Pat ', ' Bi ', ' Rem ', '\n'
        if len(parts) == 6:
            # Meaning the remark is missing completely or the last pipe is missing
            pass
            
        # The script before generated lines like this: 
        # |  **ABC Register**  |  Anti Bribery and Corruption Register  | File | ❌ No |
        # Wait, the previous replacement was:
        # lines[i] = re.sub(r'\|(.*?)\|(.*?)\|(.*?)\|', f"| \\1 | \\2 | {excel_upstream[sys_name]} |", line)
        # This regex replacement broke the table! 
        # It replaced the first 3 columns and discarded the rest or mismatched them!
        
        # Let's fix this properly.

# Let's do a complete regeneration from the lists to be absolutely safe and flawless.
# Read the current one to get the latest patterns which are mostly correct.
