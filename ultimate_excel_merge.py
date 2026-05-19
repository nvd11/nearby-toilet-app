import json
import re

# True ground truth from EXCEL text extraction

excel_upstream = {
    "CIMT": "File",
    "ENGLOBE": "File",
    "My trades": "API & File",  # Extracted both API and File from excel
    "Rapid2": "File",
    "Hotline": "File",
    "UCM": "File",
    "GCMS": "Database Connection",
    "Ask": "File",
    "Breach": "File",
    "ECA": "File",
    "ABC Register": "File",
    "Attestation": "File",
    "RegMap": "Database Connection & File",
    "ECM (Population Management)": "File",
    "PGT - HR?": "File",
    "RRIS": "Change Data Capture",
    "Engage2": "Database Connection",
    "PHANTOM": "File",
    "GBM-THOR-US": "File",
    "ITBM-DISCOVER": "File",
    "RDH": "API",
    "GFHR-INTEG": "File",
    "HELIOS": "File",
    "RegAP": "File"
}

excel_downstream = {
    "Rapid2": "API & File",
    "Ask": "File",
    "CIMT": "File & API",
    "ECM (Population Management)": "API",
    "RegMap": "API",
    "UCM": "File",
    "Breach": "API",
    "Vetting": "API",
    "GPPS": "API",
    "KYE-US-INTERFACE": "Database Conn",
    "Hotline": "File",
    "RRIS": "API",
    "SDF": "File",
    "Engage2": "Database Conn",
    "Risk Culture": "API",
    "ECA": "File",
    "GFHR-INTEG": "Web Services",
    "My trades": "File",
    "PQM - CE RC": "Manual - Upload",
    "PQM - I&M": "Manual - Upload",
    "EUC M3302": "Manual - Rekey",
    "SUPERVISION": "File",
    "M2799": "Manual - Rekey"
}

# The diagram gives us SOME extra ones not in excel (like ARCHER, QlikSense, NAS, WORM).
# We MUST merge Excel + Diagram. If Excel says something, Excel is the explicit contract for those apps.

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "| **" in line and "## ⬇️" not in "".join(lines[:i]):
        # Upstream
        sys_name = line.split("|")[1].strip().strip("*")
        if sys_name in excel_upstream:
            lines[i] = re.sub(r'\|(.*?)\|(.*?)\|(.*?)\|', f"| \\1 | \\2 | {excel_upstream[sys_name]} |", line)
    
    elif "| **" in line and "## ⬇️" in "".join(lines[:i]):
        # Downstream
        sys_name = line.split("|")[1].strip().strip("*")
        if sys_name in excel_downstream:
            lines[i] = re.sub(r'\|(.*?)\|(.*?)\|(.*?)\|', f"| \\1 | \\2 | {excel_downstream[sys_name]} |", line)

with open(md_path, "w") as f:
    f.writelines(lines)

