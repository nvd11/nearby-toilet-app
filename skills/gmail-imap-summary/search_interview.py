import imaplib
import email
from email.header import decode_header
import json
import ssl

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"

context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
mail.login(username, password)
mail.select("inbox")

# Search for emails containing "interview" or "Standard Chartered"
status, messages = mail.search(None, '(OR FROM "sc.com" SUBJECT "interview")')
email_ids = messages[0].split()

for email_id in email_ids[-3:]:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject_parts = decode_header(msg["Subject"])
            subject = ""
            for part, encoding in subject_parts:
                if isinstance(part, bytes):
                    subject += part.decode(encoding if encoding else 'utf-8', 'ignore')
                else:
                    subject += part
            print("Subject:", subject)
            date_ = msg.get("Date")
            print("Date:", date_)
            
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', 'ignore')
            else:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', 'ignore')
            print("Body:", body[:500])
            print("-" * 50)
mail.logout()
