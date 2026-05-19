import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# Generate the massive Downstream Case-by-Case Execution table
table_content = """### 3.1 Downstream Case-by-Case Execution Matrix

The following table details the required RCDP engineering effort and downstream team coordination for each of the 41 downstream consumers. This demonstrates the granular, per-system workload required for a successful migration.

| # | Downstream Consumer (Target) | Downstream Provisioning Pattern (Action Required) | Upstream Dependencies (Ingestion Workload) |
| :---: | :--- | :--- | :--- |
| 1 | **ARCHER** | **ODBC:** Provision BigQuery Auth Views. Downstream must update JDBC/ODBC connection strings. | *Pending mapping from Ajit.* Will require building Dataflow pipelines for specific upstreams. |
| 2 | **Ask** | **File:** RCDP to build Cloud Run/Dataflow export job to push CSV to Ask's SFTP/NAS. | *Pending mapping.* RCDP to build ingest pipelines. |
| 3 | **Attestation** | **Rest API:** RCDP takes over SHP API code, rewrites Oracle ODBC to BQ. | *Pending mapping.* RCDP to build ingest pipelines. |
| 4 | **Breach** | **API:** RCDP takes over SHP API code, rewrites Oracle ODBC to BQ. | *Pending mapping.* RCDP to build ingest pipelines. |
| 5 | **CIMT** | **API & File:** Dual migration. Rewrite SHP API to BQ AND build batch export to NAS. | *Pending mapping.* High ingestion effort expected. |
| 6 | **EC - ECBA** | **Rest API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 7 | **EC - ECTA** | **Rest API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 8 | **ECA** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 9 | **ECM (Pop. Mgmt)** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 10 | **EDQ (Screening)** | **Rest API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 11 | **EUC M3302** | **Manual - Rekey:** Business process change. Users must adopt BQ UI / Excel to BQ Connector. | *Pending mapping.* |
| 12 | **Engage2** | **Database Conn:** Provision BigQuery Auth Views & Service Accounts. | *Pending mapping.* |
| 13 | **External Recipients**| **Mail:** Integrate RCDP with Centralized SMTP Dispatcher. | *Pending mapping.* |
| 14 | **GCMS** | **ODBC:** Provision BigQuery Auth Views & Service Accounts. | *Pending mapping.* |
| 15 | **GFHR-INTEG** | **Web Services:** High effort. Provide legacy SOAP/XML wrapper over BigQuery. | *Pending mapping.* |
| 16 | **GHRS** | **ODBC:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 17 | **GIAM (Employee)** | **ODBC:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 18 | **GPAD** | **ODBC:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 19 | **GPPS** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 20 | **HSBC SMTP Svcs** | **Mail:** Integrate RCDP with Centralized SMTP Dispatcher. | *Pending mapping.* |
| 21 | **Hotline (Navex)** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 22 | **Internal Recipients**| **Mail:** Integrate RCDP with Centralized SMTP Dispatcher. | *Pending mapping.* |
| 23 | **KYE-US-INTERFACE** | **Database Conn:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 24 | **M2799 (FinCrime)** | **Manual - Rekey:** Business process change. Users must connect to BQ via BI/Excel. | *Pending mapping.* |
| 25 | **My trades** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 26 | **NAS (Auditors)** | **File Based:** Set up generic GCS/NAS sync script for human auditors. | *Pending mapping.* |
| 27 | **NPrinting** | **ODBC:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 28 | **OSPD** | **ODBC:** Provision BigQuery Auth Views. | *Pending mapping.* |
| 29 | **PCRT** | **Rest API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 30 | **PQM - CE RC** | **Manual - Upload:** Business process change. Move from flat files to BQ direct query. | *Pending mapping.* |
| 31 | **PQM - I&M** | **Manual - Upload:** Business process change. Move from flat files to BQ direct query. | *Pending mapping.* |
| 32 | **QlikSense** | **ODBC:** Provision BigQuery Auth Views. MI Team to update connections. | *Pending mapping.* |
| 33 | **QlikView** | **ODBC:** Provision BigQuery Auth Views. MI Team to update connections. | *Pending mapping.* |
| 34 | **RRIS** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 35 | **RTS (Screening)** | **Rest API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 36 | **Rapid2** | **API & File:** Dual migration. Rewrite API & build batch export. | *Pending mapping.* |
| 37 | **RegMap** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 38 | **Risk Culture** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
| 39 | **SDF** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 40 | **SUPERVISION** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 41 | **UCM** | **File:** Develop scheduled BQ export job to target NAS/SFTP. | *Pending mapping.* |
| 42 | **Vetting** | **API:** Rewrite SHP API code to connect to BigQuery. | *Pending mapping.* |
"""

# Replace the old Phase 3 table with this new massive table

old_p3 = """**The Lifecycle of a Single Downstream Migration Case:**

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Select Target** | Pick a specific downstream system from the dependency mapping matrix. |
| **2** | **Identify Dependency** | Determine exactly which upstream data feeds are required for this downstream. |
| **3** | **Migrate Upstream (Pull)** | Implement the ingestion pipeline in RCDP *only* for the required upstream data using defined patterns (Appendix A). |
| **4** | **Migrate Downstream** | Implement the data delivery mechanism in RCDP for the downstream consumer (Appendix B). |
| **5** | **UAT & Cutover** | Downstream system performs User Acceptance Testing. Once signed off, routing is cut over to RCDP. |
| **6** | **Iterate** | Move to the next downstream system until the list is exhausted. |"""

new_p3 = old_p3 + "\n\n" + table_content

content = content.replace(old_p3, new_p3)

with open(md_path, "w") as f:
    f.write(content)

