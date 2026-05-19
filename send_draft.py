import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = "Alice <gateman56@gmail.com>"
msg['To'] = receiver_email
msg['Subject'] = "Draft Reply for Golden Source Discussion"

body = """Hi [Architect], 

To answer your question: No, NPL currently does not publish any data. 

However, just a quick reminder that [Colleague] is still waiting for our confirmation on a specific item: whether RCDP or NPL should be the Golden Source for 'policy & procedures data'. Since NPL is currently just a consumer, could you provide some architectural guidance on this so we can unblock [Colleague]?

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
