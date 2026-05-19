import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
receiver_email = "jason1.pan@hsbc.com.hk"

msg = MIMEMultipart()
msg['From'] = "Alice <gateman56@gmail.com>"
msg['To'] = receiver_email
msg['Subject'] = "Draft Reply: Architecture Confirmation on Golden Source"

body = """Hi [External Consumer],

Thanks for sharing the summary. 

Regarding the point about RCDP being the Golden Source for GPPS data, this architectural designation is actually still under review. I am looping in our Architecture leads, [Architect 1] and [Architect 2], to provide the official confirmation on this.

@[Architect 1] / @[Architect 2] - Following our earlier discussion, I am looping you into this thread as RCDP is being communicated to external teams as the Golden Source for GPPS data. Could you please help review and confirm the target architecture and the correct system of record here for [External Consumer]'s team?

Thanks,
Jason
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
