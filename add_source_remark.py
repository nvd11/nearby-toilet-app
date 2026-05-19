import sys

excel_only_up = ["CIMT", "UCM", "GCMS", "ABC Register", "PGT - HR?", "GBM-THOR-US", "GFHR-INTEG"]
excel_both_up = ["ENGLOBE", "My trades", "Rapid2", "Hotline", "Ask", "Breach", "ECA", "Attestation", "RegMap", "ECM (Population Management)", "RRIS", "Engage2", "PHANTOM", "ITBM-DISCOVER", "RDH", "HELIOS", "RegAP"]

excel_only_down = ["CIMT", "UCM", "Engage2", "Risk Culture", "GFHR-INTEG", "PQM - CE RC", "PQM - I&M", "EUC M3302", "SUPERVISION", "M2799"]
excel_both_down = ["Rapid2", "Ask", "ECM (Population Management)", "RegMap", "Breach", "Vetting", "GPPS", "KYE-US-INTERFACE", "Hotline", "RRIS", "SDF", "ECA", "My trades"]

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/INTEGRATIONS.md"
with open(md_path, "r") as f:
    lines = f.readlines()

out_lines = []
mode = None

for line in lines:
    if line.startswith("## ⬆️"):
        mode = "up"
        out_lines.append(line)
    elif line.startswith("## ⬇️"):
        mode = "down"
        out_lines.append(line)
    elif line.startswith("| **"):
        parts = line.split("|")
        # Handle trailing/leading spaces properly
        sys_name = parts[1].strip().strip("* ")
        current_remark = parts[5].strip()
        
        source = "Architecture Diagram" # default for those missing from excel lists
        
        if mode == "up":
            if sys_name in excel_only_up:
                source = "Excel"
            elif sys_name in excel_both_up:
                source = "Diagram & Excel"
        elif mode == "down":
            if sys_name in excel_only_down:
                source = "Excel"
            elif sys_name in excel_both_down:
                source = "Diagram & Excel"
                
        if current_remark == "-" or current_remark == "":
            new_remark = f"Source: {source}"
        else:
            new_remark = f"Source: {source}. {current_remark}"
            
        parts[5] = f" {new_remark} "
        out_lines.append("|".join(parts))
    else:
        out_lines.append(line)

with open(md_path, "w") as f:
    f.writelines(out_lines)

