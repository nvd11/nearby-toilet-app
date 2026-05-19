import re

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/CDR_1_YEAR_DEMISE_PLAN.md"
with open(md_path, "r") as f:
    content = f.read()

# We need to completely rewrite the Phase 2 and Phase 3 sections to reflect the new strategy.

new_content = """# CDR Demise & Migration to RCDP: Comprehensive Action Plan

**Date:** April 20, 2026
**Target:** 1-Year Demise Initiative (Conditional)
**Author:** Jason (RCDP Lead)

## Executive Summary
This document outlines the detailed, step-by-step technical and operational plan to decommission the legacy Oracle-based Compliance Data Repository (CDR) and migrate its dependencies to the GCP-based RC Data Platform (RCDP).

To achieve the aggressive 1-year demise target, this plan strictly mandates a **Downstream-Driven (Demand-Driven), Case-by-Case Migration Strategy**. We will NOT migrate upstreams first. Instead, we migrate downstream systems one by one, pulling only their required upstream data. Any upstream data not claimed by a downstream system by the end of the project will be considered obsolete and discarded.

Full decommissioning is strictly contingent upon downstream system compliance, upstream architecture refactoring, and critical resource allocations.

---

## Phase 1: Discovery, Mapping & Infrastructure Setup (Months 1-3)

### 1.1 Comprehensive Data Lineage & Dependency Mapping (CDR Team - Ajit)
*   **Task:** Create a definitive Source-to-Target mapping matrix.
*   **Detail:** For every downstream system (e.g., M2799, Rapid2), document the exact upstream data sources required to populate it. **This mapping is the engine of our migration plan.**
*   **Complexity Assessment:** Identify all PL/SQL stored procedures and complex business logic currently executed within Oracle CDR. 
*   **Manual Process Audit:** For EUC downstream dependencies marked as "Manual", investigate the exact extraction method currently used by human operators.

### 1.2 RCDP Infrastructure Provisioning (RCDP Team - Jason)
*   **Task:** Establish the foundational GCP architecture to support legacy integration patterns.
*   **API Layer Takeover:** Confirm RCDP can inherit the existing CDR API Gateway routing to make downstream API cutovers transparent.
*   **SFTP Landing Zone:** Provision a dedicated SFTP server (via GKE + TCP Load Balancer or GCP Storage Transfer Family) to ensure zero impact on file-based upstreams that cannot mount NAS.

---

## Phase 2: Downstream-Driven "Case-by-Case" Migration (Months 4-10)

We will NOT perform a mass migration of upstream data. Instead, we execute migration pods case-by-case based on the downstream consumer. 

**The Lifecycle of a Single Downstream Migration Case:**
1.  **Select Downstream Target:** Pick a downstream system from Ajit's mapping list.
2.  **Identify Upstream Dependency:** Determine exactly which upstream data feeds are required for this specific downstream.
3.  **Migrate Required Upstream Data (Pull Strategy):** Implement the ingestion pipeline in RCDP *only* for the required upstream data using the defined integration patterns (see Appendix A).
4.  **Migrate Downstream Provisioning:** Implement the data delivery mechanism in RCDP for the downstream consumer (see Appendix B).
5.  **UAT & Cutover:** Downstream system performs UAT. Once signed off, the specific downstream is cut over to RCDP.
6.  **Iterate:** Move to the next downstream system.

**Major Benefit:** By the time all downstream systems are migrated, all *necessary* upstream data will have naturally been migrated. Any legacy CDR upstream feeds that were not pulled by a downstream system are identified as "dead data" and will be abandoned, saving massive migration effort and avoiding technical debt.

---

## Phase 3: Parallel Run & Decommissioning (Months 11-12)

### 3.1 Final Reconciliation
*   Ensure all 23 downstream business owners have formally signed off.
*   Verify that any unmigrated upstream data is officially designated as obsolete by the business.

### 3.2 Logical Demise
*   Sever all remaining upstream feeds to legacy CDR.
*   Set CDR Oracle database to "Read-Only".

### 3.3 Physical Decommissioning (Post 1-Year Target)
*   Data archiving compliance review.
*   Physical server shutdown and license reclamation.

---

## ⚠️ Critical Assumptions & Prerequisites (The "1-Year" Caveats)

The 1-year timeline is highly aggressive and **strictly dependent** on the following conditions. Failure to meet any condition will trigger an automatic extension of the demise timeline.

1.  **Dedicated Resourcing:** RCDP requires an immediate allocation of dedicated Data Engineers. These resources cannot be shared with existing BAU tasks.
2.  **Mandatory Downstream SLA:** Downstream system owners are mandated by Executive Leadership to complete their connection migrations and UAT within a strict 60-day window upon RCDP's readiness notification. Downstream delays are not RCDP's responsibility.
3.  **Fast-Track InfoSec Approvals:** Creation of the RCDP SFTP server, firewall rule changes, and Service Account provisioning must bypass standard queues via a VIP fast-track process.
4.  **Transformation Logic Portability:** If Ajit's dependency mapping reveals highly complex, undocumented PL/SQL procedures that cannot be easily translated to Dataflow/BigQuery SQL, the timeline for those specific downstream dependencies will be renegotiated.

---

## Appendix A: Upstream Ingestion Patterns (Applied On-Demand)
When a downstream system requires upstream data, RCDP will ingest it using these strategies:
*   **Direct DB Connection:** Major Refactor. Upstream must transition to API calls or file batch drops.
*   **REST API:** Transparent. Upstream continues API calls to RCDP's new endpoints.
*   **File Transfer (NAS / SFTP / Connect:Direct):** Transparent to Minor Change. RCDP ingests from NAS or the newly built RCDP SFTP zone.
*   **Real-Time CDC:** Major Refactor. Upstream must transition to Pub/Sub streaming.

## Appendix B: Downstream Provisioning Patterns (Applied On-Demand)
*   **Direct Database Connection (MI Team):** Medium Change. Downstreams must connect to BigQuery Auth Views using GCP Service Accounts.
*   **REST API:** Transparent. RCDP mimics the legacy API contracts.
*   **File Extraction / NAS:** Transparent. RCDP pushes CSV/Parquet files to the downstream's target landing zone.
*   **Manual EUC (Rekey/Upload):** Major Business Process Change. Human users cannot access Prod GCS. Users must transition to querying BQ Auth Views via BI tools/Excel, or a SharePoint dropzone must be established.
"""

with open(md_path, "w") as f:
    f.write(new_content)

