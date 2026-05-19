import json

# Let's cleanly construct the table from dictionaries
md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
        out.append(line)
    elif line.startswith("## ⬇️"):
        mode = "down"
        out.append(line)
    elif line.startswith("| **") or line.startswith("|  **"):
        parts = [p.strip() for p in line.split("|")[1:-1]] # Remove empty first and last
        sys_name = parts[0].replace("**", "").strip()
        full_name = parts[1]
        pattern = parts[2]
        
        # Determine bi-directional from the current table
        bi = "❌ No" if "❌ No" in parts[3] else "✅ Yes"
        
        # Determine remark
        # Some rows lost their remark because of my bad regex previously.
        # Let's rebuild the source logic.
        
        excel_only_up = ["CIMT", "UCM", "GCMS", "ABC Register", "PGT - HR?", "GBM-THOR-US", "GFHR-INTEG"]
        excel_both_up = ["ENGLOBE", "My trades", "Rapid2", "Hotline", "Ask", "Breach", "ECA", "Attestation", "RegMap", "ECM (Population Management)", "RRIS", "Engage2", "PHANTOM", "ITBM-DISCOVER", "RDH", "HELIOS", "RegAP"]

        excel_only_down = ["CIMT", "UCM", "Engage2", "Risk Culture", "GFHR-INTEG", "PQM - CE RC", "PQM - I&M", "EUC M3302", "SUPERVISION", "M2799"]
        excel_both_down = ["Rapid2", "Ask", "ECM (Population Management)", "RegMap", "Breach", "Vetting", "GPPS", "KYE-US-INTERFACE", "Hotline", "RRIS", "SDF", "ECA", "My trades"]

        source = "Architecture Diagram"
        if mode == "up":
            if sys_name in excel_only_up: source = "Excel"
            elif sys_name in excel_both_up: source = "Diagram & Excel"
        elif mode == "down":
            if sys_name in excel_only_down: source = "Excel"
            elif sys_name in excel_both_down: source = "Diagram & Excel"
        
        remark = f"Source: {source}"
        if sys_name == "NAS" and mode == "down":
            remark += ". Shared Drive accessed manually by Users / Auditors"
        elif sys_name == "NAS" and mode == "up":
            remark += ". Manual file drops via NAS Path"
            
        # Reconstruct the line perfectly
        new_row = f"| **{sys_name}** | {full_name} | {pattern} | {bi} | {remark} |\n"
        out.append(new_row)
    else:
        out.append(line)

with open(md_path, "w") as f:
    f.writelines(out)

