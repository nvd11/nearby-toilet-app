md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_DEMISE_STRATEGY_PLAN.md"

with open(md_path, "r") as f:
    content = f.read()

import re

# We will replace everything from "## Phase 1" down to "## Phase 2" (exclusive)
# Then increment the old Phase 2 and Phase 3.

new_phases = """## Phase 1: Discovery & Dependency Mapping

### 1.1 Comprehensive Data Lineage & Dependency Mapping (CDR Team - Ajit)
*   **Task:** Create a definitive Source-to-Target mapping matrix.
*   **Detail:** For every downstream system (e.g., M2799, Rapid2), document the exact upstream data sources required to populate it. **This mapping is the engine of our migration plan.**
*   **Complexity Assessment:** Identify all PL/SQL stored procedures and complex business logic currently executed within Oracle CDR. 
*   **Manual Process Audit:** For EUC downstream dependencies marked as "Manual", investigate the exact extraction method currently used by human operators.

---

## Phase 2: RCDP Foundational Infrastructure Setup

Before executing case-by-case migrations, RCDP must build the core GCP infrastructure to intercept and handle legacy integration patterns.

### 2.1 NAS Integration & Common Ingestion Pipelines
*   **Task:** Establish secure connectivity to legacy on-prem NAS drives.
*   **Detail:** Mount existing CDR NAS paths to the GCP environment. Build robust, parameter-driven **Common Dataflow Jobs** designed to automatically monitor NAS directories, ingest arriving files, and load them securely into RCDP Landing GCS Buckets (and subsequently into BigQuery).

### 2.2 API Gateway & Layer Takeover
*   **Task:** Assume ownership of the existing CDR API ecosystem.
*   **Detail:** Confirm with Enterprise Architecture that RCDP can inherit the legacy API gateway configurations. Deploy backend microservices (e.g., Cloud Run or GKE) that mimic the legacy API contracts, transparently routing existing downstream API requests to the new BigQuery datasets.

### 2.3 SFTP Server (VM) Provisioning
*   **Task:** Build a dedicated GCP-hosted SFTP landing zone.
*   **Detail:** To prevent major refactoring for PaaS upstream systems that cannot mount NAS or call APIs, RCDP will provision a dedicated SFTP VM (Compute Engine). This VM will be integrated directly with Cloud Storage (via GCSFuse) so that files dropped via traditional SFTP instantly land in the RCDP data lake.

---

## Phase 3: Downstream-Driven "Case-by-Case" Migration"""

# Perform the replacements
# First, replace Phase 1 and old 1.2
content = re.sub(r'## Phase 1: Discovery.*?## Phase 2: Downstream-Driven "Case-by-Case" Migration', new_phases, content, flags=re.DOTALL)

# Now, bump the old Phase 3 to Phase 4
content = re.sub(r'## Phase 3: Parallel Run', r'## Phase 4: Parallel Run', content)

with open(md_path, "w") as f:
    f.write(content)

