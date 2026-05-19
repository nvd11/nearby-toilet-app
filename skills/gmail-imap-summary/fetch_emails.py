import imaplib
import email
from email.header import decode_header
import json
import ssl

def fetch_latest_emails():
    # Credentials
    username = "gateman56@gmail.com"
    password = "lekzjeuykwytooxj"
    imap_server = "imap.gmail.com"

    try:
        # Connect to server
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
        mail.login(username, password)
        mail.select("inbox")

        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print(json.dumps({"error": "Failed to search inbox"}))
            return

        # Get list of email IDs
        email_ids = messages[0].split()
        latest_email_ids = email_ids[-5:] # Get last 5 emails
        latest_email_ids.reverse()

        results = []

        for email_id in latest_email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    # Decode from
                    from_name, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(from_name, bytes):
                        from_name = from_name.decode(encoding if encoding else 'utf-8')

                    date_ = msg.get("Date")

                    # Get body snippet
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', 'ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', 'ignore')

                    results.append({
                        "subject": subject,
                        "from": from_name,
                        "date": date_,
                        "snippet": body[:150].strip().replace('\r', '').replace('\n', ' ') + "..."
                    })

        mail.logout()
        print(json.dumps(results, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    fetch_latest_emails()