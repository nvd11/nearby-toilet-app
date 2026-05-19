import imaplib, email, ssl, datetime
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"
import socket

socket.setdefaulttimeout(10)

try:
    mail = imaplib.IMAP4_SSL(imap_server, ssl_context=ssl.create_default_context())
    mail.login(username, password)
    mail.select("inbox", readonly=True)
    last_month = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%d-%b-%Y")
    status, msgs = mail.search(None, f'(SINCE "{last_month}" FROM "cmbchina")')
    e_ids = msgs[0].split()
    if e_ids:
        for e_id in e_ids[-1:]:
            status, data = mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            html_content = ""
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                    break
            with open("/home/gateman/.openclaw/workspace/cmb_bill.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("Saved to cmb_bill.html")
    mail.logout()
except Exception as e:
    print(e)
