import imaplib
import email
from email.header import decode_header
import ssl
import re
import datetime

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"

context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
mail.login(username, password)
mail.select("inbox", readonly=True)

two_weeks_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=14)).strftime("%d-%b-%Y")
status, messages = mail.search(None, f'(SINCE "{two_weeks_ago}")')
email_ids = messages[0].split()

for e_id in email_ids:
    status, msg_data = mail.fetch(e_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT)])")
    subject = ""
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            sub_raw = msg.get("Subject", "")
            if sub_raw:
                dec = decode_header(sub_raw)[0]
                subject = dec[0].decode(dec[1] or 'utf-8', errors='ignore') if isinstance(dec[0], bytes) else dec[0]
                
    if "招商银行" in subject and "账单" in subject:
        status, full_data = mail.fetch(e_id, "(RFC822)")
        for response_part in full_data:
            if isinstance(response_part, tuple):
                full_msg = email.message_from_bytes(response_part[1])
                body = ""
                if full_msg.is_multipart():
                    for part in full_msg.walk():
                        if part.get_content_type() in ["text/html"]:
                            body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                else:
                    body = full_msg.get_payload(decode=True).decode(full_msg.get_content_charset() or 'utf-8', errors='ignore')
                
                clean_body = re.sub(r'<[^>]+>', ' ', body)
                clean_body = re.sub(r'\s+', ' ', clean_body)
                print(clean_body[:1000])
mail.logout()
