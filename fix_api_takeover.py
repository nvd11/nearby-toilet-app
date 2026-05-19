import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Replace the API Takeover section in Phase 2
old_p2 = """| **API Gateway & Layer Takeover** | RCDP Team | Inherit legacy API gateway routing. Deploy backend API microservices that mimic legacy API contracts, transparently routing downstream requests to BigQuery. |"""
new_p2 = """| **API Layer Takeover (SHP Platform)** | RCDP Team | Take ownership of the existing CDR API layer currently hosted on the HSBC common API platform (SHP). Modify the existing API code to replace Oracle ODBC connections with BigQuery Client/ODBC drivers, preserving the original API contracts without provisioning new compute infrastructure. |"""
content = content.replace(old_p2, new_p2)

# Replace the Downstream Provisioning Pattern B
old_b = """*   **REST API:** Transparent. RCDP mimics the legacy API contracts."""
new_b = """*   **REST API:** Transparent. RCDP takes over the existing CDR API code on the SHP platform and repoints the backend to BigQuery."""
content = content.replace(old_b, new_b)

with open(md_path, "w") as f:
    f.write(content)

