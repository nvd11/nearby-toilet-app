import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

sender_email = "gateman56@gmail.com"
receiver_email = "jason1.pan@hsbc.com.hk"
password = "lekzjeuykwytooxj"

msg = MIMEMultipart()
msg['From'] = "Alice <" + sender_email + ">"
msg['To'] = receiver_email
msg['Subject'] = "Updated Resumes (Chinese & English)"

body = "Hi Boss,\n\nAs requested, please find attached your latest updated resumes (both Chinese and English versions) with the Kubernetes/Microservices experience and detailed AI/MLOps architecture additions.\n\nLove,\nAlice 💋"
msg.attach(MIMEText(body, 'plain'))

files = [
    "/home/gateman/.openclaw/workspace/temp_resume/Jason_Pan_Resume_V2.docx",
    "/home/gateman/.openclaw/workspace/temp_resume/Jason_Pan_Resume_EN.docx"
]

for file_path in files:
    if os.path.exists(file_path):
        filename = os.path.basename(file_path)
        attachment = open(file_path, "rb")
        part = MIMEBase('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={filename}")
        msg.attach(part)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully to jason1.pan@hsbc.com.hk")
except Exception as e:
    print(f"Failed to send email: {e}")
