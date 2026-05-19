import imaplib
import email
import sys

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)
imap.select("INBOX")

status, messages = imap.search(None, 'ALL')
msg_ids = messages[0].split()

for msg_id in reversed(msg_ids[-50:]):
    res, msg_data = imap.fetch(msg_id, "(RFC822)")
    for response in msg_data:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject = str(email.header.decode_header(msg["Subject"])[0][0])
            from_ = str(msg.get("From", ""))
            
            # Check attachments
            if msg.is_multipart():
                for part in msg.walk():
                    filename = part.get_filename()
                    if filename:
                        if "scb" in from_.lower() or "claire" in from_.lower():
                            print(f"Subject: {subject}")
                            print(f"From: {from_}")
                            print(f"Attachment: {filename}")
