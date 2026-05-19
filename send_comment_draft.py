import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "Draft comment for RITM42184994"

body = "Confirmed. RCDP is now fully configured to utilize Google IAM, GCP Secret Manager, and an automated 80-day Service Account key rotation mechanism to enforce strict least-privilege controls and a zero-direct-user-access policy."

msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
