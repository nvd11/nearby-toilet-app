import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/MEETING_MINUTES_AJIT.md"
with open(md_path, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    
    # Insert extra upstream patterns after pattern d
    if "| **d. Send to SFTP Landing**" in line:
        new_lines.append("| **e. Real-Time CDC (Change Data Capture)** | **Major Change.** Discovered in deep-dive (e.g., RRIS using GoldenGate). BigQuery does not natively support direct Oracle CDC ingestion. Upstream must redesign to use GCP Pub/Sub streaming or Dataflow. | 🔴 High |\n")
        new_lines.append("| **f. MFT / Connect:Direct** | **Transparent.** Found in architecture diagram (e.g., Whistleblow). Similar to SFTP, the enterprise MFT agent can simply be repointed to deliver files to a GCP Cloud Storage bucket. | 🟢 Low |\n")
        
    # Insert extra downstream patterns after pattern c
    if "| **c. Through File Transfer**" in line:
        new_lines.append("| **d. Automated Email / SMTP Dispatch** | **Minor Change.** Architecture diagram shows CDR sending emails to recipients. RCDP must implement a new email notification mechanism (e.g., Cloud Functions triggering SendGrid or an internal SMTP relay). | 🟢 Low |\n")
        new_lines.append("| **e. Legacy Web Services (SOAP)** | **Medium Change.** Found in Excel mapping (e.g., GFHR-INTEG). If RCDP's new API layer only supports REST/JSON, downstreams relying on old SOAP/XML endpoints will require adapter logic or client-side rewrites. | 🟡 Medium |\n")
        new_lines.append("| **f. Manual EUC (Rekey / Upload)** | **Business Process Change.** Excel shows manual processes (e.g., M2799, PQM). RCDP is a backend data platform, not a UI frontend. These manual business users must transition to connecting Excel directly to BQ Auth Views. | 🔴 High (Process) |\n")

with open(md_path, "w") as f:
    f.writelines(new_lines)

