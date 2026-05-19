import imaplib
import email
from email.header import decode_header
import sys
import os

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

try:
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
                subject_tuple = decode_header(msg["Subject"])[0]
                subject = subject_tuple[0]
                encoding = subject_tuple[1]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                
                if "RE: Invite to Job Interview with Standard Chartered" in subject:
                    print(f"Found email: {subject}")
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get('Content-Disposition') is None:
                                continue
                            
                            filename = part.get_filename()
                            if filename:
                                print(f"Attachment found: {filename}")
                                filepath = os.path.join(os.getcwd(), filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                print(f"Saved: {filename}")
                    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
