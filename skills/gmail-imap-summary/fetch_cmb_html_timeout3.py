import imaplib, email, ssl, datetime
import socket

socket.setdefaulttimeout(15)
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"

try:
    mail = imaplib.IMAP4_SSL(imap_server, ssl_context=ssl.create_default_context())
    mail.login(username, password)
    mail.select("inbox", readonly=True)
    last_month = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%d-%b-%Y")
    status, msgs = mail.search(None, f'(SINCE "{last_month}")')
    e_ids = msgs[0].split()
    
    for e_id in reversed(e_ids):
        status, data = mail.fetch(e_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT)])')
        subject_raw = data[0][1].decode('utf-8', errors='ignore')
        if "招商银行" in subject_raw and "账单" in subject_raw:
            status, text_data = mail.fetch(e_id, '(BODY.PEEK[TEXT])')
            html_content = text_data[0][1].decode('utf-8', errors='ignore')
            with open("/home/gateman/.openclaw/workspace/cmb_bill.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Saved to cmb_bill.html")
            break
            
    mail.logout()
except Exception as e:
    print(e)
