import imaplib
import email
from email.header import decode_header

# Credentials
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
mail.select("inbox")

# Search for emails from Cloudflare
status, messages = mail.search(None, '(FROM "abuse@notify.cloudflare.com")')

if status == "OK":
    email_ids = messages[0].split()
    for num in email_ids[-2:]: # Get the last two (most recent)
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                print(f"Subject: {subject}")
                
                # Get email body
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            print(part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace'))
                            break
                else:
                    print(msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace'))
                print("-" * 50)
mail.logout()
