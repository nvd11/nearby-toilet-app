import json

# Absolute ground truth combining Excel and diagram safely
upstreams = {
    "ABC Register": {"full": "Anti Bribery and Corruption Register", "pattern": "Batch (TBC)"},
    "ARAMIS (Audit)": {"full": "-", "pattern": "DB Connection"},
    "Ask": {"full": "ASK for Risk and Compliance", "pattern": "Batch (TBC)"},
    "Attestation": {"full": "EMP-COMP", "pattern": "Batch (TBC)"},
    "Breach": {"full": "EMPLOYEE-COMPLIANCE-BREACH-MANAGEMENT", "pattern": "Batch (TBC)"},
    "CAP160": {"full": "-", "pattern": "DB Connection"},
    "CIMT": {"full": "CONSOLIDATED-ISSUES-MONITORING-TOOL", "pattern": "Batch (TBC)"},
    "ECA": {"full": "EMPLOYEE-COMPLIANCE-CONDUCT-ACTIVITIES", "pattern": "Batch (TBC)"},
    "ECM (Population Management)": {"full": "EMPLOYEE-COMPLIANCE-POPULATION-MANAGEMENT", "pattern": "Batch (TBC)"},
    "EIM": {"full": "-", "pattern": "DB Connection"},
    "ENGLOBE": {"full": "ENGLOBE", "pattern": "DB Connection"},
    "Engage2": {"full": "REGULATORY-ENGAGEMENT-GLOBAL", "pattern": "SFTP"},
    "G&E (Iqueue)": {"full": "-", "pattern": "DB Connection"},
    "GBM-THOR-US": {"full": "GBM-THOR-US", "pattern": "Batch (TBC)"},
    "GCMS": {"full": "GLOBAL-CONFLICT-MANAGEMENT-SYSTEM", "pattern": "Batch (TBC)"},
    "GFHR-INTEG": {"full": "GFHR-INTEGRATION-TECHNOLOGY", "pattern": "Batch (TBC)"},
    "GMT": {"full": "-", "pattern": "DB Connection"},
    "HELIOS": {"full": "HSBC-HELIOS", "pattern": "DB Connection"},
    "HMS": {"full": "-", "pattern": "DB Connection"},
    "HR Employee": {"full": "-", "pattern": "DB Connection"},
    "HashiCorp Vault": {"full": "-", "pattern": "SFTP"},
    "Hotline": {"full": "HSBC-CONFIDENTIAL-HOTLINE (Navex)", "pattern": "Batch (TBC)"},
    "IRIS": {"full": "-", "pattern": "SFTP"},
    "ITBM-DISCOVER": {"full": "ITBM-DISCOVER (Clarity)", "pattern": "DB Connection"},
    "Manual Feed Reference Data": {"full": "-", "pattern": "SFTP"},
    "My trades": {"full": "ET-COMPLIANCE-MY-TRADES-APPIAN", "pattern": "DB Connection"},
    "NAS": {"full": "-", "pattern": "NAS"},
    "PGT - HR?": {"full": "HR-SUCCESSFACTORS-CS-EC", "pattern": "Batch (TBC)"},
    "PHANTOM": {"full": "PHANTOM", "pattern": "DB Connection"},
    "RDH": {"full": "REFERENCE-DATA-HUB-GCP", "pattern": "Real-Time (API)"},
    "RRIS": {"full": "MAGNUS-REG-REPORTING-OBLIGATIONS", "pattern": "Real-Time (GoldenGate CDC)"},
    "Rapid2": {"full": "REGULATORY-COMPLIANCE-RAPID2", "pattern": "DB Connection"},
    "RegAP": {"full": "-", "pattern": "DB Connection"},
    "RegMap": {"full": "POLICY-ADVISORY-COMPLIANCE-REG-MAPPING", "pattern": "DB Connection & SFTP"},
    "SDF": {"full": "SURVEILLANCE-DATA-FACTORY-GBM-UK", "pattern": "DB Connection"},
    "UCM": {"full": "UNIFIED-CASE-MANAGEMENT", "pattern": "Batch (TBC)"},
    "WORM Device": {"full": "-", "pattern": "Write/Retrieve (File Based via Connect Direct)"},
    "Whistleblow": {"full": "Whistleblow", "pattern": "SFTP & File Based (via Connect Direct)"}
}

downstreams = {
    "ARCHER": {"full": "-", "pattern": "ODBC"},
    "Ask": {"full": "ASK for Risk and Compliance", "pattern": "Rest API"},
    "Attestation": {"full": "EMP-COMP", "pattern": "Rest API"},
    "Breach": {"full": "EMPLOYEE-COMPLIANCE-BREACH-MANAGEMENT", "pattern": "Rest API"},
    "CIMT": {"full": "CONSOLIDATED-ISSUES-MONITORING-TOOL", "pattern": "Database View / Extract (TBC)"},
    "EC - ECBA": {"full": "-", "pattern": "Rest API"},
    "EC - ECTA": {"full": "-", "pattern": "Rest API"},
    "ECA": {"full": "EMPLOYEE-COMPLIANCE-CONDUCT-ACTIVITIES", "pattern": "Rest API"},
    "ECM (Population Management)": {"full": "EMPLOYEE-COMPLIANCE-POPULATION-MANAGEMENT", "pattern": "Rest API"},
    "EDQ (External Data Quality Screening)": {"full": "-", "pattern": "Rest API"},
    "EUC M3302": {"full": "EUC for M3302...", "pattern": "Database View / Extract (TBC)"},
    "Engage2": {"full": "REGULATORY-ENGAGEMENT-GLOBAL", "pattern": "Database View / Extract (TBC)"},
    "External Recipients": {"full": "-", "pattern": "Mail"},
    "GCMS": {"full": "GLOBAL-CONFLICT-MANAGEMENT-SYSTEM", "pattern": "ODBC"},
    "GFHR-INTEG": {"full": "GFHR-INTEGRATION-TECHNOLOGY", "pattern": "Database View / Extract (TBC)"},
    "GHRS": {"full": "-", "pattern": "ODBC"},
    "GIAM (Employee)": {"full": "-", "pattern": "ODBC"},
    "GPAD": {"full": "-", "pattern": "ODBC"},
    "GPPS": {"full": "GROUP-POLICY-PROCEDURE-MANAGEMENT", "pattern": "Rest API"},
    "HSBC SMTP Exchange Services": {"full": "-", "pattern": "Mail"},
    "Hotline": {"full": "HSBC-CONFIDENTIAL-HOTLINE (Navex)", "pattern": "Rest API"},
    "Internal Recipients": {"full": "-", "pattern": "Mail"},
    "KYE-US-INTERFACE": {"full": "KYE-US-INTERFACE", "pattern": "Rest API"},
    "M2799": {"full": "M2799 Financial Crime Consolidated Performance", "pattern": "Database View / Extract (TBC)"},
    "My trades": {"full": "ET-COMPLIANCE-MY-TRADES-APPIAN", "pattern": "Rest API"},
    "NAS": {"full": "-", "pattern": "File Based"},
    "NPrinting": {"full": "-", "pattern": "ODBC"},
    "OSPD": {"full": "-", "pattern": "ODBC"},
    "PCRT": {"full": "-", "pattern": "Rest API"},
    "PQM - CE RC": {"full": "PQM - CE RC", "pattern": "Database View / Extract (TBC)"},
    "PQM - I&M": {"full": "PQM - I&M", "pattern": "Database View / Extract (TBC)"},
    "QlikSense": {"full": "-", "pattern": "ODBC"},
    "QlikView": {"full": "-", "pattern": "ODBC"},
    "RRIS": {"full": "MAGNUS-REG-REPORTING-OBLIGATIONS", "pattern": "Rest API"},
    "RTS (Real Time Screening)": {"full": "-", "pattern": "Rest API"},
    "Rapid2": {"full": "REGULATORY-COMPLIANCE-RAPID2", "pattern": "Rest API"},
    "RegMap": {"full": "POLICY-ADVISORY-COMPLIANCE-REG-MAPPING", "pattern": "Rest API"},
    "Risk Culture": {"full": "Risk Culture Dashboard", "pattern": "Database View / Extract (TBC)"},
    "SDF": {"full": "SURVEILLANCE-DATA-FACTORY-GBM-UK", "pattern": "Database View / Extract (TBC)"},
    "SUPERVISION": {"full": "SUPERVISION-PLATFORM", "pattern": "Database View / Extract (TBC)"},
    "UCM": {"full": "UNIFIED-CASE-MANAGEMENT", "pattern": "Database View / Extract (TBC)"},
    "Vetting": {"full": "IR-EMPLOYEE-VETTING-APPIAN", "pattern": "Rest API"}
}

md = ["# CDR Integrations Inventory (Full List)\n",
      "This document tracks ALL known upstream and downstream systems interacting with the legacy Compliance Data Repository (CDR), aggregated from all 3 architectural diagrams.\n",
      "Systems marked with `✅ Yes` under **Bi-directional** act as both publishers (Upstream) and consumers (Downstream) of CDR data.\n\n"]

md.append("## ⬆️ Upstream Systems (Data Sources)\n")
md.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
md.append("| :--- | :--- | :--- | :---: |\n")

for k in sorted(upstreams.keys()):
    bi = "✅ Yes" if k in downstreams else "❌ No"
    v = upstreams[k]
    md.append(f"| **{k}** | {v['full']} | {v['pattern']} | {bi} |\n")

md.append("\n## ⬇️ Downstream Systems (Data Consumers)\n")
md.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
md.append("| :--- | :--- | :--- | :---: |\n")

for k in sorted(downstreams.keys()):
    bi = "✅ Yes" if k in upstreams else "❌ No"
    v = downstreams[k]
    md.append(f"| **{k}** | {v['full']} | {v['pattern']} | {bi} |\n")

with open("/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md", "w") as f:
    f.writelines(md)

