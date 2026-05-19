import re

upstream_excel = [
    ("CIMT", "CONSOLIDATED-ISSUES-MONITORING-TOOL"),
    ("ENGLOBE", "ENGLOBE"), # PGT - Englobe
    ("My trades", "ET-COMPLIANCE-MY-TRADES-APPIAN"),
    ("Rapid2", "REGULATORY-COMPLIANCE-RAPID2"),
    ("Hotline", "HSBC-CONFIDENTIAL-HOTLINE (Navex)"),
    ("UCM", "UNIFIED-CASE-MANAGEMENT"),
    ("GCMS", "GLOBAL-CONFLICT-MANAGEMENT-SYSTEM"),
    ("Ask", "ASK for Risk and Compliance"),
    ("Breach", "EMPLOYEE-COMPLIANCE-BREACH-MANAGEMENT"),
    ("ECA", "EMPLOYEE-COMPLIANCE-CONDUCT-ACTIVITIES"),
    ("ABC Register", "Anti Bribery and Corruption Register"),
    ("Attestation", "EMP-COMP"),
    ("RegMap", "POLICY-ADVISORY-COMPLIANCE-REG-MAPPING"),
    ("ECM (Population Management)", "EMPLOYEE-COMPLIANCE-POPULATION-MANAGEMENT"), # ECM?
    ("PGT - HR?", "HR-SUCCESSFACTORS-CS-EC"),
    ("RRIS", "MAGNUS-REG-REPORTING-OBLIGATIONS"),
    ("Engage2", "REGULATORY-ENGAGEMENT-GLOBAL"),
    ("PHANTOM", "PHANTOM"),
    ("GBM-THOR-US", "GBM-THOR-US"),
    ("ITBM-DISCOVER", "ITBM-DISCOVER (Clarity)"),
    ("RDH", "REFERENCE-DATA-HUB-GCP"),
    ("GFHR-INTEG", "GFHR-INTEGRATION-TECHNOLOGY"),
    ("HELIOS", "HSBC-HELIOS")
]

downstream_excel = [
    ("Rapid2", "REGULATORY-COMPLIANCE-RAPID2"),
    ("Ask", "ASK for Risk and Compliance"),
    ("CIMT", "CONSOLIDATED-ISSUES-MONITORING-TOOL"),
    ("ECM (Population Management)", "EMPLOYEE-COMPLIANCE-POPULATION-MANAGEMENT"), # ECM?
    ("RegMap", "POLICY-ADVISORY-COMPLIANCE-REG-MAPPING"),
    ("UCM", "UNIFIED-CASE-MANAGEMENT"),
    ("Breach", "EMPLOYEE-COMPLIANCE-BREACH-MANAGEMENT"),
    ("Vetting", "IR-EMPLOYEE-VETTING-APPIAN"),
    ("GPPS", "GROUP-POLICY-PROCEDURE-MANAGEMENT"),
    ("KYE-US-INTERFACE", "KYE-US-INTERFACE"),
    ("Hotline", "HSBC-CONFIDENTIAL-HOTLINE (Navex)"),
    ("RRIS", "MAGNUS-REG-REPORTING-OBLIGATIONS"),
    ("SDF", "SURVEILLANCE-DATA-FACTORY-GBM-UK"),
    ("Engage2", "REGULATORY-ENGAGEMENT-GLOBAL"),
    ("Risk Culture", "Risk Culture Dashboard"),
    ("ECA", "EMPLOYEE-COMPLIANCE-CONDUCT-ACTIVITIES"),
    ("GFHR-INTEG", "GFHR-INTEGRATION-TECHNOLOGY"),
    ("My trades", "ET-COMPLIANCE-MY-TRADES-APPIAN"),
    ("PQM - CE RC", "PQM - CE RC"),
    ("PQM - I&M", "PQM - I&M"),
    ("EUC M3302", "EUC for M3302..."),
    ("SUPERVISION", "SUPERVISION-PLATFORM"),
    ("M2799", "M2799 Financial Crime Consolidated Performance")
]

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

upstream_dict = {}
downstream_dict = {}

mode = None
for line in lines:
    if line.startswith("## ⬆️"): mode = "up"
    elif line.startswith("## ⬇️"): mode = "down"
    elif line.startswith("| **"):
        parts = [p.strip() for p in line.split("|")]
        name = parts[1].strip("*")
        full = parts[2]
        pattern = parts[3]
        if mode == "up":
            upstream_dict[name] = {"full": full, "pattern": pattern}
        elif mode == "down":
            downstream_dict[name] = {"full": full, "pattern": pattern}

# Ensure Excel items exist
for n, f in upstream_excel:
    if n not in upstream_dict:
        upstream_dict[n] = {"full": f, "pattern": "Batch (TBC)"}
for n, f in downstream_excel:
    if n not in downstream_dict:
        downstream_dict[n] = {"full": f, "pattern": "Database View / Extract (TBC)"}

# Update bi-directionality
def write_md():
    out = ["# CDR Integrations Inventory (Full List)\n",
           "This document tracks ALL known upstream and downstream systems interacting with the legacy Compliance Data Repository (CDR), aggregated from all 3 architectural diagrams.\n",
           "Systems marked with `✅ Yes` under **Bi-directional** act as both publishers (Upstream) and consumers (Downstream) of CDR data.\n\n"]
    
    out.append("## ⬆️ Upstream Systems (Data Sources)\n")
    out.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
    out.append("| :--- | :--- | :--- | :---: |\n")
    for k in sorted(upstream_dict.keys()):
        bi = "✅ Yes" if k in downstream_dict else "❌ No"
        v = upstream_dict[k]
        out.append(f"| **{k}** | {v['full']} | {v['pattern']} | {bi} |\n")

    out.append("\n## ⬇️ Downstream Systems (Data Consumers)\n")
    out.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
    out.append("| :--- | :--- | :--- | :---: |\n")
    for k in sorted(downstream_dict.keys()):
        bi = "✅ Yes" if k in upstream_dict else "❌ No"
        v = downstream_dict[k]
        out.append(f"| **{k}** | {v['full']} | {v['pattern']} | {bi} |\n")
        
    with open(md_path, "w") as f:
        f.writelines(out)

write_md()

