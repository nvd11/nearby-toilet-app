import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Re: CDR Demise Approach & Pattern Mapping Discussion (Draft for Ajit)"

body = """Hi Ajit,

Thanks for putting together the pattern mapping. It gives us a very clear overview of the 28 upstream/downstream integrations and will be extremely helpful for our sizing.

I’ve been reviewing the proposed 3-phase approach. While I understand the rationale behind Phase 1 (Global Data Sync from CDR to RCDP), I have significant concerns about the feasibility of executing a "horizontal sync" across the board. I strongly suggest we pivot to a Demand-Driven (Vertical Slice / Case-by-case) migration strategy instead.

Here is why establishing a global Phase 1 sync is highly problematic:

1. Architectural Mismatch (OLAP vs. OLTP): We need to respect the architectural nature of BigQuery. BQ is an analytical data warehouse that excels at massive, append-only workloads. Oracle, however, is designed for high-frequency, row-level updates and deletes. Forcing BigQuery to continuously mirror Oracle’s row-level mutations to maintain synchronization goes against its core design principles and introduces massive performance overhead.
2. Prohibitive Costs & Resource Waste: If we try to avoid the row-level mutation issue by repeatedly executing massive full-data migrations (truncate and load) to keep the systems synced, we hit another wall. Running these massive daily extracts will incur huge, unnecessary GCP compute costs, severely strain the legacy Oracle database, and risk missing our daily SLA/batch windows.
3. Migrating Technical Debt: A global sync means we will inevitably lift and shift obsolete, unused, or redundant data into our new platform before we even know if downstream consumers still need it.

Proposed Alternative: The Vertical Slice Approach
Instead of syncing the entire database first, we should migrate on a case-by-case basis driven by downstream consumers. 
We pick a specific consumer (e.g., a reporting tool or downstream API), identify the exact upstream feeds they need, redirect those specific feeds into RCDP, migrate only their necessary historical data *once*, and then cut over the consumer immediately.

This approach ensures:
* We align with BigQuery's best practices.
* We completely avoid the cost and risk of maintaining a massive, continuous global data sync.
* We can deliver end-to-end value incrementally (Agile delivery).

Let's use tomorrow's meeting to discuss and align on this demand-driven strategy. Once we agree on the direction, I will need 1 to 2 days to draft a detailed execution plan with specific effort estimations based on the patterns you provided.

Regards,
Jason
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
