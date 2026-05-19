import imaplib
import email
from email.header import decode_header
import sys

# Account credentials
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

try:
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("INBOX")
    
    # Search for SCB, assignment, standard chartered in all recent emails
    status, messages = imap.search(None, 'ALL')
    msg_ids = messages[0].split()
    
    found = 0
    for msg_id in reversed(msg_ids[-50:]): # check last 50
        res, msg = imap.fetch(msg_id, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject_tuple = decode_header(msg["Subject"])[0]
                subject = subject_tuple[0]
                encoding = subject_tuple[1]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                
                from_ = msg.get("From", "")
                
                subject_lower = str(subject).lower()
                from_lower = str(from_).lower()
                
                # Check for assignment
                if "assignment" in subject_lower or "scb" in subject_lower or "standard chartered" in subject_lower or "claire.huang" in from_lower:
                    print(f"--- EMAIL {found+1} ---")
                    print(f"Subject: {subject}")
                    print(f"From: {from_}")
                    
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body += part.get_payload(decode=True).decode(errors="ignore")
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                    
                    print("Body:")
                    print(body[:3000])
                    found += 1
except Exception as e:
    print(f"Error: {e}")
