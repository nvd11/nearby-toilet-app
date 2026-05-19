import re

# Update INTEGRATIONS.md
int_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(int_path, "r") as f:
    int_lines = f.readlines()

targets = ["M2799", "EUC M3302", "PQM - CE RC", "PQM - I&M"]
for i, line in enumerate(int_lines):
    if line.startswith("| **"):
        sys_name = line.split("|")[1].strip().strip("*")
        if sys_name in targets and "## ⬇️" in "".join(int_lines[:i]):
            parts = line.split("|")
            old_remark = parts[5].strip()
            new_remark = f"{old_remark} <br>⚠️ **Action for Ajit:** Clarify exactly how human users currently extract data from CDR to perform this manual rekey/upload."
            parts[5] = f" {new_remark} "
            int_lines[i] = "|".join(parts)

with open(int_path, "w") as f:
    f.writelines(int_lines)

# Update MEETING_MINUTES_AJIT.md
min_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/MEETING_MINUTES_AJIT.md"
with open(min_path, "r") as f:
    min_lines = f.readlines()

out_min = []
for line in min_lines:
    if "| **f. Manual EUC (Rekey / Upload)** |" in line:
        new_desc = "**Investigation Required.** Excel shows manual downstream processes (e.g., M2799, PQM). Since RCDP is a backend platform and direct human access to BigQuery or Prod GCS is strictly prohibited by InfoSec, we must first ask Ajit *how* users currently obtain this data from CDR before designing a replacement solution."
        out_min.append(f"| **f. Manual EUC (Rekey / Upload)** | {new_desc} | 🔴 High (Investigation) |\n")
    elif "**Dependency Mapping:** Conduct a comprehensive review" in line:
        out_min.append(line)
        out_min.append("*   **Manual Process Clarification:** For downstreams marked as 'Manual - Rekey' or 'Manual - Upload' (e.g., M2799, PQM), clarify the current data extraction mechanism. Exactly how do human users currently retrieve the raw data from CDR to perform these manual tasks?\n")
    else:
        out_min.append(line)

with open(min_path, "w") as f:
    f.writelines(out_min)

