import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "[V3 FINAL] Jira Epic Breakdown: Data migration from CDR to RCDP (RRIS)"

body = """
Hi Jason,

Here is the updated Jira story breakdown. The presentation layer (previously Story 2.2) has been split into an Analysis story (2.3.1) and a Build story (2.3.2) as per your latest logic tree.

### Epic: Data migration from CDR to RCDP : RRIS

#### Part 1: Data Gap Analysis & Remediation

**Story 1.1**
**Subject:** [Analysis] Assess Historical Data Gap for RRIS MI
**Description:**
*   **Background:** Before migrating RRIS MI from CDR to RCDP, we must determine if RCDP already contains all the historical data required by the downstream MI reports.
*   **As a** RCDP Data Engineer
*   **I want to** compare the existing RRIS historical data in RCDP against what is currently used in CDR
*   **So that** we can definitively answer whether a historical data gap exists (Yes or No).
**Acceptance Criteria:**
1.  A data profiling comparison is completed between RCDP and CDR.
2.  A definitive "Yes" or "No" conclusion is documented regarding the existence of a historical data gap.

**Story 1.1.1**
**Subject:** [Analysis] Determine Sourcing Strategy for Missing Historical Data
**Description:**
*   **Background:** Story 1.1 confirmed that a historical data gap exists. We now need to decide the most efficient and reliable source to backfill this data: fetching directly from the upstream system (RRIS) or migrating the legacy data from CDR.
*   **As a** RCDP Tech Lead
*   **I want to** evaluate the feasibility of ingesting from RRIS versus migrating from CDR
*   **So that** we can finalize the technical approach for the historical data remediation.
**Acceptance Criteria:**
1.  (Blocked by Story 1.1; only required if 1.1 outcome is "Yes").
2.  A decision is documented on Confluence: Sourcing strategy is chosen as either "Ingest from RRIS" or "Migrate from CDR".

**Story 1.2**
**Subject:** [Data Eng] Remediate RRIS Historical Data Gap (Placeholder)
**Description:**
*   **Background:** This is a placeholder story that depends entirely on the outcome of the analysis in Story 1.1.1. The implementation details will be defined once the sourcing strategy is chosen.
*   **As a** RCDP Data Engineer
*   **I want to** execute the chosen data backfill strategy (either RRIS ingestion or CDR migration)
*   **So that** RCDP's historical data is completely synced and ready for downstream MI usage.
**Acceptance Criteria:**
1.  (Blocked by Story 1.1.1).
2.  If strategy is "Ingest from RRIS": Develop and run a one-off ingestion job from RRIS.
3.  If strategy is "Migrate from CDR": Develop and run a data extraction script from Oracle CDR into RCDP.
4.  Data reconciliation matches expected record counts and checksums.

**Story 1.3**
**Subject:** [Analysis] Assess Schema Gap (Missing Tables or Fields)
**Description:**
*   **Background:** Beyond historical data, we must check if there are specific RRIS tables or columns currently used by MI in CDR that are not being ingested into RCDP's daily feeds.
*   **As a** RCDP Data Engineer
*   **I want to** perform a schema mapping comparison between CDR and RCDP for RRIS data
*   **So that** we know exactly if any pipeline enhancements are required (Yes or No).
**Acceptance Criteria:**
1.  A schema gap report is generated mapping CDR fields to RCDP fields.
2.  A definitive list of missing tables/fields is documented (if any).

**Story 1.3.1**
**Subject:** [Data Eng] Enhance Pipeline for Missing RRIS Tables & Fields
**Description:**
*   **Background:** Story 1.3 identified specific schema gaps (missing tables/fields).
*   **As a** RCDP Data Engineer
*   **I want to** enhance the RCDP ingestion pipeline
*   **So that** all newly identified tables and fields are ingested and landed in RCDP daily.
**Acceptance Criteria:**
1.  (Blocked by Story 1.3; only required if a gap is found).
2.  Ingestion pipelines are updated to include the missing tables/fields.
3.  Daily delta scheduling is verified in the RCDP raw layer.

#### Part 2: Downstream Integration & Presentation Layer

**Story 2.1**
**Subject:** [Infra] Setup Connectivity & IAM for RRIS MI
**Description:**
*   **Background:** The RRIS MI team needs infrastructure access to query RCDP (BigQuery) to replace their legacy CDR connection.
*   **As a** RCDP Infra/Security Admin
*   **I want to** provision Service Accounts and grant appropriate BigQuery IAM roles to the RRIS MI team
*   **So that** they have the necessary connectivity and permissions to access RCDP data securely.
**Acceptance Criteria:**
1.  Dedicated Service Account(s) are created for RRIS MI.
2.  Appropriate IAM roles (e.g., BigQuery Data Viewer) are granted.
3.  Connectivity is successfully tested with the MI team.

**Story 2.2**
**Subject:** [Analysis] Analyze and Document RRIS MI Translation Logic
**Description:**
*   **Background:** Before building the new presentation layer, we need to fully understand the existing data transformation logic used by RRIS MI reports in the legacy CDR.
*   **As a** RCDP Data Engineer
*   **I want to** check with the MI team and CDR team to analyze the current RRIS reporting translation logic
*   **So that** we have clear SQL mapping requirements before building the presentation views.
**Acceptance Criteria:**
1.  Translation logic and SQL scripts are extracted from CDR.
2.  The transformation logic is reviewed and confirmed with the MI team.
3.  A mapping specification document is published on Confluence.

**Story 2.3**
**Subject:** [Data Eng] Build Presentation Layer Views for RRIS MI
**Description:**
*   **Background:** The translation logic mapping is complete (Story 2.2). We must now implement this logic in BigQuery to serve the MI team.
*   **As a** RCDP Data Engineer
*   **I want to** build Authorized/Presentation Views in BigQuery that encapsulate the legacy CDR translation logic
*   **So that** the RRIS MI team can query RCDP using a structure and logic as close to their existing CDR setup as possible.
**Acceptance Criteria:**
1.  BigQuery SQL views are created strictly based on the logic documented in Story 2.2.
2.  The output data structure successfully matches the agreed-upon MI requirements.

**Story 2.4**
**Subject:** [Testing] End-to-End Testing & Parallel Run with RRIS MI
**Description:**
*   **Background:** Before cutting over to production, we must ensure the data generated by RCDP exactly matches or safely replaces what CDR currently provides.
*   **As a** RCDP Tech Lead / QA
*   **I want to** support the RRIS MI team in executing end-to-end tests and parallel runs
*   **So that** we can verify data accuracy and obtain UAT sign-off.
**Acceptance Criteria:**
1.  Parallel run results (CDR reports vs RCDP reports) are compared.
2.  Formal UAT sign-off is provided.

#### Part 3: Decommission & Disconnect

**Story 3.1**
**Subject:** [Cutover] Disconnect RRIS and RRIS MI from Legacy CDR
**Description:**
*   **Background:** RCDP is now successfully serving RRIS MI data in production. The legacy pipelines must be shut down.
*   **As a** RCDP Tech Lead
*   **I want to** coordinate with the RRIS and CDR teams to disable legacy data feeds and MI extracts
*   **So that** CDR is completely decoupled from the RRIS data flow.
**Acceptance Criteria:**
1.  RRIS upstream stops sending data feeds to CDR.
2.  RRIS MI downstream stops fetching data from CDR.
3.  Legacy CDR jobs are decommissioned.

Best regards,
Alice (OpenClaw)
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
