import imaplib
import email
import ssl

username = "gateman56@gmail.com"
password = "lekzjeuykwytooxj"
imap_server = "imap.gmail.com"

context = ssl.create_default_context()
mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
mail.login(username, password)
mail.select("inbox", readonly=True)

status, messages = mail.search(None, '(FROM "googleplay-noreply@google.com")')
e_id = messages[0].split()[-1]

status, msg_data = mail.fetch(e_id, "(BODY.PEEK[TEXT])")
body = msg_data[0][1].decode('utf-8', errors='ignore')

# print snippets containing HK, USD, total, etc.
lines = body.splitlines()
for line in lines:
    if "HK" in line or "USD" in line or "$" in line or "¥" in line or "total" in line.lower() or "合计" in line or "总计" in line:
        print(line.strip())

mail.logout()
