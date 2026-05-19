import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = "Alice <gateman56@gmail.com>"
msg['To'] = receiver_email
msg['Subject'] = "Draft Reply for Archana - Regular Feeds"

body = """Hi Archana,

Yes, once a policy has been changed/created in GPPS, GPPS will send the latest to us. But RCDP mainly acts as a pass-through pipeline to feed NPL for the latest policies. Since NPL is the business application that holds the active 'golden state' of these policies, it makes architectural sense for SFC to fetch the latest data directly from NPL, and only come to RCDP for historical records.

Best regards,
"""

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")
