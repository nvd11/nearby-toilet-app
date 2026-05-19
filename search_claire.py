import imaplib
import email
from email.header import decode_header
import sys

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(username, password)
imap.select("INBOX")

status, messages = imap.search(None, 'ALL')
msg_ids = messages[0].split()

found = 0
for msg_id in reversed(msg_ids[-60:]):
    res, msg_data = imap.fetch(msg_id, "(RFC822)")
    for response in msg_data:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject_tuple = decode_header(msg["Subject"])[0]
            subject = subject_tuple[0]
            encoding = subject_tuple[1]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
            
            from_ = str(msg.get("From", ""))
            
            if "claire" in from_.lower() or "scb" in from_.lower() or "standard" in from_.lower() or "assignment" in str(subject).lower():
                print(f"[{found}] Subject: {subject}")
                print(f"From: {from_}")
                
                # Check for attachments
                if msg.is_multipart():
                    for part in msg.walk():
                        filename = part.get_filename()
                        if filename:
                            print(f"   Attachment: {filename}")
                found += 1
