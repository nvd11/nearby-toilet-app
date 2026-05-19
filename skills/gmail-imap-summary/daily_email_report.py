import imaplib
import email
from email.header import decode_header
import json
import ssl
import datetime

def fetch_daily_emails():
    username = "gateman56@gmail.com"
    password = "lekzjeuykwytooxj"
    imap_server = "imap.gmail.com"

    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
        mail.login(username, password)
        mail.select("inbox")

        # Get today's date in IMAP format (e.g., "15-Mar-2026")
        today = datetime.datetime.utcnow().strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{today}")')
        
        if status != "OK":
            print("没有找到今天的邮件")
            return

        email_ids = messages[0].split()
        if not email_ids:
            print("今天目前还没有收到任何新邮件哦！")
            return
            
        print(f"**今天共收到 {len(email_ids)} 封新邮件**\n")

        # Fetch the latest 10 if there are many
        for email_id in reversed(email_ids[-10:]):
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    from_name, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(from_name, bytes):
                        from_name = from_name.decode(encoding if encoding else 'utf-8')

                    date_ = msg.get("Date")

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', 'ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', 'ignore')

                    print(f"- **来自**: {from_name}")
                    print(f"  **时间**: {date_}")
                    print(f"  **主题**: {subject}")
                    print(f"  **摘要**: {body[:100].strip().replace(chr(10), ' ').replace(chr(13), '')}...\n")

        mail.logout()

    except Exception as e:
        print(f"抓取失败: {str(e)}")

if __name__ == "__main__":
    fetch_daily_emails()
