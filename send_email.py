import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
receiver_email = "jason1.pan@hsbc.com.hk"
password = "lekzjeuykwytooxj"

md_path = "/home/gateman/.openclaw/workspace/cdr-demise-docs/EMAIL_DRAFT_TO_AJIT.md"
with open(md_path, "r") as f:
    draft_content = f.read()

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Draft: Follow-up: CDR to RCDP Migration - Clarification on Downstream EUCs & SMTP Dispatch"

# Adding the markdown content as plain text (or we could convert to HTML, but plain text is fine for a draft to copy/paste)
body = f"""Hi Jason,

Here is the draft email to Ajit that we prepared earlier regarding the manual EUCs and SMTP dispatch. You can copy and paste this into your corporate Outlook.

---

{draft_content}

---

Best,
Alice
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully to " + receiver_email)
except Exception as e:
    print(f"Failed to send email: {e}")

