import imaplib
import email
from email.header import decode_header
import ssl
import datetime

def decode_mime_words(s):
    if not s: return ""
    results = []
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            results.append(word.decode(encoding or 'utf-8', errors='ignore'))
        else:
            results.append(word)
    return "".join(results)

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

if not email_ids:
    print("No emails found.")
else:
    # Bulk fetch
    fetch_ids = b",".join(email_ids)
    status, msg_data = mail.fetch(fetch_ids, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
    
    keywords = ["收据", "receipt", "账单", "bill", "order", "订单", "google play", "payment", "招商银行"]
    
    for response_part in reversed(msg_data):
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_mime_words(msg.get("Subject", ""))
            from_name = decode_mime_words(msg.get("From", ""))
            date_ = msg.get("Date", "")
            
            is_bill = False
            for kw in keywords:
                if kw.lower() in subject.lower() or kw.lower() in from_name.lower():
                    is_bill = True
                    break
                    
            if is_bill:
                print(f"[{date_}] {from_name} : {subject}")

mail.logout()
