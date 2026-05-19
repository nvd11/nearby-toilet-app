import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "RCDP Centralised Secrets Management - Cyber Review Document"

body = """# Cybersecurity Review: Centralised Secrets Management Pre-Production Review (GCP)

## 1. Ticket Overview
* **Parent Ticket:** RITM42184935 (Initiate a Cybersecurity review)
* **Item Number:** RITM42184994
* **Context:** Centralised Secrets Management Pre-Production Review - GCP
* **Project:** RCDP (Risk & Compliance Data Platform)
* **Assignment Group:** Cyber - IAM FDE Global
* **Current State:** Awaiting Customer (Review Stage)
* **Pending Task:** SCTASK65025211 - Customer Input Required (Customer Remedial Task)

---

## 2. RCDP Access Control & Authentication Architecture

RCDP enforces a strict **Zero Direct User Access** policy to the underlying GCP data infrastructure. All access is programmatically gated and falls into two approved patterns:

### 2.1. Upstream and Downstream Data Integration (System-to-System)
* **Mechanism:** GCP Service Account (SA) Credential Files (JSON keys).
* **Usage:** Upstream systems pushing data into RCDP, and downstream systems (e.g., BI tools) pulling data from RCDP, authenticate exclusively via dedicated GCP Service Accounts.
* **Security Controls & Automated Key Rotation:** 
  To eliminate manual key sharing and comply with enterprise credential aging policies, RCDP has implemented a fully automated SA key rotation mechanism:
  * **Secure Distribution:** New SA keys are automatically generated and placed into secured, dedicated GCP Cloud Storage Buckets. Upstream/downstream systems programmatically fetch their respective keys from these buckets.
  * **Strict 80-Day Lifecycle:** SA keys are enforced with a strict maximum validity of 80 days. Any key older than 80 days is automatically deleted from the Service Account to prevent aging violations.
  * **Zero-Downtime Overlap:** To ensure uninterrupted service, the rotation process operates on a staggered timeline:
    * Key creation is scheduled bi-monthly on odd months.
    * A new key is generated and placed in the bucket.
    * After 2 months (~60 days), the next rotation cycle triggers: a new key is generated, and the 60-day-old key is removed from the bucket (though it remains valid for authentication).
    * At the 80-day mark, the original key hard-expires and is permanently deleted from the Service Account. Upstream systems must have switched to the new key during the 20-day overlap window.

### 2.2. Data Scientist Access via CMLP (Platform-to-Platform with Identity Passthrough)
* **Mechanism:** Authenticated access routed through the Compliance Machine Learning Platform (CMLP) querying BigQuery Authorized Views (BQ Auth Views) within RCDP.
* **Usage:** Data Scientists do not log directly into RCDP. They interact with the data exclusively through CMLP, which passes their session context downstream.
* **Security Controls:** 
  * **RBAC Entitlement Engine Integration:** RCDP's BigQuery Auth Views are seamlessly integrated with an RBAC-based entitlement engine.
  * **Dynamic Identity Detection:** When a query is executed from CMLP, the BQ Auth View dynamically detects the specific GCP account/identity of the logged-in Data Scientist.
  * **Row/Column-Level Security:** Based on the detected identity, the entitlement engine enforces strict access controls, ensuring the Data Scientist can only view the exact data subsets they are authorized to see, without exposing underlying base tables or requiring static shared credentials.

---

## 3. Review Summary
* The architecture described above confirms that no secrets are manually managed, hardcoded, or exposed to unauthorized users. 
* All system-to-system authentication relies on automated, strict-lifecycle GCP Service Accounts.
* All interactive data analysis relies on identity-passthrough and RBAC via BigQuery Auth Views.
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
