import imaplib, email, ssl, datetime
import socks
import socket
username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"

# Set up SOCKS proxy if needed or just let it timeout
socket.setdefaulttimeout(15)

try:
    mail = imaplib.IMAP4_SSL(imap_server, ssl_context=ssl.create_default_context())
    mail.login(username, password)
    mail.select("inbox", readonly=True)
    status, msgs = mail.search('utf-8', 'SUBJECT', '招商银行信用卡电子账单')
    e_ids = msgs[0].split()
    if e_ids:
        # fetch only body text/html part to be faster than RFC822
        status, data = mail.fetch(e_ids[-1], '(BODY.PEEK[TEXT])')
        html_content = data[0][1].decode('utf-8', errors='ignore')
        
        with open("/home/gateman/.openclaw/workspace/cmb_bill.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Saved to cmb_bill.html")
    else:
        print("未找到账单")
    mail.logout()
except Exception as e:
    print(e)
