import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = "Alice <" + sender_email + ">"
msg['To'] = receiver_email
msg['Subject'] = "20道资深架构师/中间件专家 面试题与参考答案 - 简历分析"

try:
    with open("/home/gateman/.openclaw/workspace/cv_interview_qa.md", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("Error: Markdown file not found.")
    sys.exit(1)

# Adding some intro text
intro = "Boss, \n\n这是您要求基于那份资深候选人简历生成的 20 道面试题及参考答案，请查收！\n\n------------------------\n\n"
full_content = intro + content

msg.attach(MIMEText(full_content, 'plain', 'utf-8'))

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email sent successfully to " + receiver_email)
except Exception as e:
    print(f"Error sending email: {e}")
    sys.exit(1)
