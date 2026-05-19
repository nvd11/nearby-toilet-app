import imaplib
import email
from email.header import decode_header
import sys

# Account credentials
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"

def clean_text(text):
    if text:
        return text.replace('\r', '').replace('\n', ' ').strip()
    return ""

def search_scb_email():
    try:
        # connect to server
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(username, password)
        imap.select("INBOX")

        # search for emails from SCB or containing SCB assignment
        status, messages = imap.search(None, '(OR (FROM "scb") (SUBJECT "SCB"))')
        if not messages[0]:
            status, messages = imap.search(None, 'ALL')
            
        messages = messages[0].split()
        
        # We only want to look at the last 20 emails if there's no match
        for msg_id in reversed(messages[-20:]):
            res, msg = imap.fetch(msg_id, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                    
                    from_ = msg.get("From", "")
                    
                    if "scb" in subject.lower() or "scb" in from_.lower() or "assignment" in subject.lower() or "standard chartered" in subject.lower():
                        print(f"Subject: {subject}")
                        print(f"From: {from_}")
                        
                        # Get body
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    print("Body:")
                                    print(body)
                                    return
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                            print("Body:")
                            print(body)
                            return
        print("No SCB email found.")
    except Exception as e:
        print(f"Error: {e}")

search_scb_email()
