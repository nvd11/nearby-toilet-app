import json

full_data_str = """
{"upstream": [
    {"name": "My Trades", "method": "DB Connection"},
    {"name": "RegMap/SRM (Source Systems)", "method": "DB Connection"},
    {"name": "RDHM", "method": "DB Connection"},
    {"name": "HashiCorp Vault", "method": "Approle auth"},
    {"name": "IRIS", "method": "DB Connection"},
    {"name": "Reg Engage2", "method": "DB Connection"},
    {"name": "HELIOS", "method": "DB Connection"},
    {"name": "Horizon Scanning (RAPID2)", "method": "DB Connection"},
    {"name": "ARAMIS (Audit)", "method": "DB Connection"},
    {"name": "SCM / SDF", "method": "DB Connection"},
    {"name": "ITBM Discover (Clarity)", "method": "DB Connection"},
    {"name": "ENGLOBE", "method": "DB Connection"},
    {"name": "CAP160", "method": "DB Connection"},
    {"name": "Whistleblow (Source Systems)", "method": "DB Connection"},
    {"name": "EIM", "method": "DB Connection"},
    {"name": "HR Employee", "method": "DB Connection"},
    {"name": "G&E (Iqueue)", "method": "DB Connection"},
    {"name": "GMT", "method": "DB Connection"},
    {"name": "Phantom (ISR)", "method": "DB Connection"},
    {"name": "RegAP", "method": "DB Connection"},
    {"name": "HMS", "method": "DB Connection"},
    {"name": "Manual Feed Reference Data", "method": "File Based (via Connect Direct)"},
    {"name": "Whistleblow (Manual Feed)", "method": "File Based (via Connect Direct)"},
    {"name": "NAS", "method": "NAS Path (File Based)"},
    {"name": "WORM Device", "method": "Write/Retrieve (File Based via Connect Direct)"},
    {"name": "RAPID2 Appian Common Service", "method": "Rest API"},
    {"name": "EC - PM", "method": "Rest API"},
    {"name": "EC - ECBM", "method": "Rest API"},
    {"name": "EC - ECA", "method": "Rest API"},
    {"name": "EC - ECTA", "method": "Rest API"},
    {"name": "Ask C", "method": "Rest API"},
    {"name": "EC - Attestations", "method": "Rest API"},
    {"name": "Vetting (External Third Party)", "method": "Rest API"},
    {"name": "EC - MyTrades", "method": "Rest API"},
    {"name": "GPPS", "method": "Rest API"},
    {"name": "EC - ECBA", "method": "Rest API"},
    {"name": "US KYE", "method": "Rest API"},
    {"name": "NAVEX (HSBC Confidential Hotline)", "method": "Rest API"},
    {"name": "PCRT", "method": "Rest API"},
    {"name": "RegMap/SRM (Appian)", "method": "Rest API"},
    {"name": "Vetting (Hybrid)", "method": "Rest API"},
    {"name": "RRIS (Magnus)", "method": "Rest API"},
    {"name": "RegMap/SRM (Hybrid)", "method": "Rest API"},
    {"name": "EDQ (External Data Quality Screening)", "method": "Rest API"},
    {"name": "RTS (Real Time Screening)", "method": "Rest API"}
  ],
  "downstream": [
    {"name": "QlikSense", "method": "ODBC"},
    {"name": "NPrinting", "method": "ODBC"},
    {"name": "QlikView", "method": "ODBC"},
    {"name": "GIAM (Employee)", "method": "ODBC"},
    {"name": "ARCHER", "method": "ODBC"},
    {"name": "GPAD", "method": "ODBC"},
    {"name": "GCMS", "method": "ODBC"},
    {"name": "OSPD", "method": "ODBC"},
    {"name": "GHRS", "method": "ODBC"},
    {"name": "NAS", "method": "File Based"},
    {"name": "HSBC SMTP Exchange Services", "method": "Mail"},
    {"name": "Internal Recipients", "method": "Mail"},
    {"name": "External Recipients", "method": "Mail"},
    {"name": "RAPID2 Appian Common Service", "method": "Rest API"},
    {"name": "EC - PM", "method": "Rest API"},
    {"name": "EC - ECBM", "method": "Rest API"},
    {"name": "EC - ECA", "method": "Rest API"},
    {"name": "EC - ECTA", "method": "Rest API"},
    {"name": "Ask C", "method": "Rest API"},
    {"name": "EC - Attestations", "method": "Rest API"},
    {"name": "Vetting (External Third Party)", "method": "Rest API"},
    {"name": "EC - MyTrades", "method": "Rest API"},
    {"name": "GPPS", "method": "Rest API"},
    {"name": "EC - ECBA", "method": "Rest API"},
    {"name": "US KYE", "method": "Rest API"},
    {"name": "NAVEX (HSBC Confidential Hotline)", "method": "Rest API"},
    {"name": "PCRT", "method": "Rest API"},
    {"name": "RegMap/SRM (Appian)", "method": "Rest API"},
    {"name": "Vetting (Hybrid)", "method": "Rest API"},
    {"name": "RRIS (Magnus)", "method": "Rest API"},
    {"name": "RegMap/SRM (Hybrid)", "method": "Rest API"},
    {"name": "EDQ (External Data Quality Screening)", "method": "Rest API"},
    {"name": "RTS (Real Time Screening)", "method": "Rest API"}
  ]}
"""
full_data = json.loads(full_data_str)

name_map = {
    "RAPID2 Appian Common Service": "Rapid2",
    "EC - PM": "ECM (Population Management)",
    "EC - ECBM": "Breach",
    "EC - ECA": "ECA",
    "EC - Attestations": "Attestation",
    "Ask C": "Ask",
    "EC - MyTrades": "My trades",
    "My Trades": "My trades",
    "US KYE": "KYE-US-INTERFACE",
    "NAVEX (HSBC Confidential Hotline)": "Hotline",
    "RegMap/SRM (Appian)": "RegMap",
    "RegMap/SRM (Hybrid)": "RegMap",
    "RegMap/SRM (Source Systems)": "RegMap",
    "RRIS (Magnus)": "RRIS",
    "Vetting (External Third Party)": "Vetting",
    "Vetting (Hybrid)": "Vetting",
    "Horizon Scanning (RAPID2)": "Rapid2",
    "SCM / SDF": "SDF",
    "Whistleblow (Source Systems)": "Whistleblow",
    "Whistleblow (Manual Feed)": "Whistleblow",
    "Reg Engage2": "Engage2",
    "RDHM": "RDH",
    "ITBM Discover (Clarity)": "ITBM-DISCOVER"
}

full_name_map = {
    "Rapid2": "REGULATORY-COMPLIANCE-RAPID2",
    "ECM (Population Management)": "EMPLOYEE-COMPLIANCE-POPULATION-MANAGEMENT",
    "Breach": "EMPLOYEE-COMPLIANCE-BREACH-MANAGEMENT",
    "ECA": "EMPLOYEE-COMPLIANCE-CONDUCT-ACTIVITIES",
    "Attestation": "EMP-COMP",
    "Ask": "ASK for Risk and Compliance",
    "My trades": "ET-COMPLIANCE-MY-TRADES-APPIAN",
    "KYE-US-INTERFACE": "KYE-US-INTERFACE",
    "Hotline": "HSBC-CONFIDENTIAL-HOTLINE (Navex)",
    "RegMap": "POLICY-ADVISORY-COMPLIANCE-REG-MAPPING",
    "RRIS": "MAGNUS-REG-REPORTING-OBLIGATIONS",
    "Vetting": "IR-EMPLOYEE-VETTING-APPIAN",
    "SDF": "SURVEILLANCE-DATA-FACTORY-GBM-UK",
    "Whistleblow": "Whistleblow",
    "Engage2": "REGULATORY-ENGAGEMENT-GLOBAL",
    "CIMT": "CONSOLIDATED-ISSUES-MONITORING-TOOL",
    "GCMS": "GLOBAL-CONFLICT-MANAGEMENT-SYSTEM",
    "ABC Register": "Anti Bribery and Corruption Register",
    "PGT - HR?": "HR-SUCCESSFACTORS-CS-EC",
    "PHANTOM": "PHANTOM",
    "GBM-THOR-US": "GBM-THOR-US",
    "ITBM-DISCOVER": "ITBM-DISCOVER (Clarity)",
    "RDH": "REFERENCE-DATA-HUB-GCP",
    "GFHR-INTEG": "GFHR-INTEGRATION-TECHNOLOGY",
    "Helios": "HSBC-HELIOS",
    "GPPS": "GROUP-POLICY-PROCEDURE-MANAGEMENT",
    "Risk Culture": "Risk Culture Dashboard",
    "EUC M3302": "EUC for M3302...",
    "SUPERVISION": "SUPERVISION-PLATFORM",
    "M2799": "M2799 Financial Crime Consolidated Performance",
    "ENGLOBE": "ENGLOBE",
    "Phantom (ISR)": "PHANTOM"
}

upstream_map = {}
downstream_map = {}

def normalize_name(n):
    return name_map.get(n, n)

for item in full_data['upstream']:
    norm = normalize_name(item['name'])
    if norm in upstream_map and upstream_map[norm] != item['method']:
        upstream_map[norm] += " & " + item['method']
    else:
        upstream_map[norm] = item['method']

for item in full_data['downstream']:
    norm = normalize_name(item['name'])
    if norm in downstream_map and downstream_map[norm] != item['method']:
        downstream_map[norm] += " & " + item['method']
    else:
        downstream_map[norm] = item['method']

old_upstreams = ["CIMT", "ABC Register", "PGT - HR?", "GFHR-INTEG", "GBM-THOR-US", "PHANTOM"]
old_downstreams = ["CIMT", "Risk Culture", "GFHR-INTEG", "PQM - CE RC", "PQM - I&M", "EUC M3302", "SUPERVISION", "M2799"]

for o in old_upstreams:
    if o not in upstream_map: upstream_map[o] = "Batch / MFT (TBC)"
for o in old_downstreams:
    if o not in downstream_map: downstream_map[o] = "Database View / Extract (TBC)"

md = ["# CDR Integrations Inventory (Full List)\n",
      "This document tracks ALL known upstream and downstream systems interacting with the legacy Compliance Data Repository (CDR), aggregated from all 3 architectural diagrams.\n",
      "Systems marked with `✅ Yes` under **Bi-directional** act as both publishers (Upstream) and consumers (Downstream) of CDR data.\n\n"]

md.append("## ⬆️ Upstream Systems (Data Sources)\n")
md.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
md.append("| :--- | :--- | :--- | :---: |\n")

for k, v in sorted(upstream_map.items()):
    bi = "✅ Yes" if k in downstream_map else "❌ No"
    full = full_name_map.get(k, "-")
    md.append(f"| **{k}** | {full} | {v} | {bi} |\n")

md.append("\n## ⬇️ Downstream Systems (Data Consumers)\n")
md.append("| System Name | Full Name / Context | Integration Pattern | Bi-directional? |\n")
md.append("| :--- | :--- | :--- | :---: |\n")

for k, v in sorted(downstream_map.items()):
    bi = "✅ Yes" if k in upstream_map else "❌ No"
    full = full_name_map.get(k, "-")
    md.append(f"| **{k}** | {full} | {v} | {bi} |\n")

with open("/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md", "w") as f:
    f.writelines(md)

