import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/MEETING_MINUTES_AJIT.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **f. MFT / Connect:Direct** |" in line:
        lines[i] = line.replace("| **f. MFT / Connect:Direct** |", "| **f. Connect:Direct** |")

with open(md_path, "w") as f:
    f.writelines(lines)
