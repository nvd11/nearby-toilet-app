import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# --- PHASE 1 REPLACEMENT ---
p1_old = """### 1.1 Comprehensive Data Lineage & Dependency Mapping (CDR Team - Ajit)
*   **Task:** Create a definitive Source-to-Target mapping matrix.
*   **Detail:** For every downstream system (e.g., M2799, Rapid2), document the exact upstream data sources required to populate it. **This mapping is the engine of our migration plan.**
*   **Complexity Assessment:** Identify all PL/SQL stored procedures and complex business logic currently executed within Oracle CDR. 
*   **Manual Process Audit:** For EUC downstream dependencies marked as "Manual", investigate the exact extraction method currently used by human operators."""

p1_new = """| Task / Area | Owner | Description / Deliverable |
| :--- | :--- | :--- |
| **Source-to-Target Mapping** | CDR Team (Ajit) | Create a definitive mapping matrix. For every downstream system (e.g., M2799, Rapid2), document the exact upstream data sources required to populate it. **This mapping is the engine of our migration plan.** |
| **Complexity Assessment** | CDR Team (Ajit) | Identify and document all PL/SQL stored procedures and complex business logic currently executed within Oracle CDR to plan migration difficulty. |
| **Manual Process Audit** | CDR Team (Ajit) | For EUC downstream dependencies marked as "Manual", investigate the exact extraction method currently used by human operators. |"""

content = content.replace(p1_old, p1_new)

# --- PHASE 2 REPLACEMENT ---
p2_old = """### 2.1 NAS Integration & Common Ingestion Pipelines
*   **Task:** Establish secure connectivity to legacy on-prem NAS drives.
*   **Detail:** Mount existing CDR NAS paths to the GCP environment. Build robust, parameter-driven **Common Dataflow Jobs** designed to automatically monitor NAS directories, ingest arriving files, and load them securely into RCDP Landing GCS Buckets (and subsequently into BigQuery).

### 2.2 API Gateway & Layer Takeover
*   **Task:** Assume ownership of the existing CDR API ecosystem.
*   **Detail:** Confirm with Enterprise Architecture that RCDP can inherit the legacy API gateway configurations. Deploy backend microservices (e.g., Cloud Run or GKE) that mimic the legacy API contracts, transparently routing existing downstream API requests to the new BigQuery datasets.

### 2.3 SFTP Server (VM) Provisioning
*   **Task:** Build a dedicated GCP-hosted SFTP landing zone.
*   **Detail:** To prevent major refactoring for PaaS upstream systems that cannot mount NAS or call APIs, RCDP will provision a dedicated SFTP VM (Compute Engine). This VM will be integrated directly with Cloud Storage (via GCSFuse) so that files dropped via traditional SFTP instantly land in the RCDP data lake."""

p2_new = """| Infrastructure Component | Owner | Technical Implementation Details |
| :--- | :--- | :--- |
| **NAS & Common Ingestion Pipelines** | RCDP Team | Mount existing CDR NAS paths to GCP. Build parameter-driven **Common Dataflow Jobs** to automatically monitor NAS directories, ingest files, and load them into RCDP Landing GCS Buckets and BigQuery. |
| **API Gateway & Layer Takeover** | RCDP Team | Inherit legacy API gateway routing. Deploy backend microservices (Cloud Run/GKE) that mimic legacy API contracts, transparently routing downstream requests to BigQuery. |
| **SFTP Server (VM) Provisioning** | RCDP Team | Provision a dedicated SFTP VM (Compute Engine) integrated with Cloud Storage (via GCSFuse). This provides a drop zone for PaaS upstreams unable to mount NAS or call APIs, landing files instantly in the data lake. |"""

content = content.replace(p2_old, p2_new)

# --- PHASE 3 REPLACEMENT ---
p3_old = """**The Lifecycle of a Single Downstream Migration Case:**
1.  **Select Downstream Target:** Pick a downstream system from Ajit's mapping list.
2.  **Identify Upstream Dependency:** Determine exactly which upstream data feeds are required for this specific downstream.
3.  **Migrate Required Upstream Data (Pull Strategy):** Implement the ingestion pipeline in RCDP *only* for the required upstream data using the defined integration patterns (see Appendix A).
4.  **Migrate Downstream Provisioning:** Implement the data delivery mechanism in RCDP for the downstream consumer (see Appendix B).
5.  **UAT & Cutover:** Downstream system performs UAT. Once signed off, the specific downstream is cut over to RCDP.
6.  **Iterate:** Move to the next downstream system."""

p3_new = """**The Lifecycle of a Single Downstream Migration Case:**

| Step | Action | Description |
| :---: | :--- | :--- |
| **1** | **Select Target** | Pick a specific downstream system from the dependency mapping matrix. |
| **2** | **Identify Dependency** | Determine exactly which upstream data feeds are required for this downstream. |
| **3** | **Migrate Upstream (Pull)** | Implement the ingestion pipeline in RCDP *only* for the required upstream data using defined patterns (Appendix A). |
| **4** | **Migrate Downstream** | Implement the data delivery mechanism in RCDP for the downstream consumer (Appendix B). |
| **5** | **UAT & Cutover** | Downstream system performs User Acceptance Testing. Once signed off, routing is cut over to RCDP. |
| **6** | **Iterate** | Move to the next downstream system until the list is exhausted. |"""

content = content.replace(p3_old, p3_new)

# --- PHASE 4 REPLACEMENT (and fixing numbering) ---
p4_old = """### 3.1 Final Reconciliation
*   Ensure all 23 downstream business owners have formally signed off.
*   Verify that any unmigrated upstream data is officially designated as obsolete by the business.

### 3.2 Logical Demise
*   Sever all remaining upstream feeds to legacy CDR.
*   Set CDR Oracle database to "Read-Only".

### 3.3 Physical Decommissioning (Post-Migration)
*   Data archiving compliance review.
*   Physical server shutdown and license reclamation."""

p4_new = """| Milestone | Key Activities |
| :--- | :--- |
| **4.1 Final Reconciliation** | • Ensure all 23 downstream business owners have formally signed off.<br>• Verify unmigrated upstream data is officially designated as obsolete. |
| **4.2 Logical Demise** | • Sever all remaining upstream feeds to legacy CDR.<br>• Set CDR Oracle database to "Read-Only". |
| **4.3 Physical Decommissioning** | • Conduct data archiving compliance review.<br>• Execute physical server shutdown and reclaim Oracle licenses (Post-Migration). |"""

content = content.replace(p4_old, p4_new)
content = content.replace("## Phase 4: Parallel Run & Decommissioning\n\n|", "## Phase 4: Parallel Run & Decommissioning\n|")

with open(md_path, "w") as f:
    f.write(content)

