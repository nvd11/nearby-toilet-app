import imaplib
import email
from email.header import decode_header
import json
import ssl
import datetime

def fetch_weekly_emails():
    username = "gateman56@gmail.com"
    password = "lekzjeuykwytooxj"
    imap_server = "imap.gmail.com"

    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
        mail.login(username, password)
        mail.select("inbox")

        # Get date 7 days ago
        last_week = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{last_week}")')
        
        if status != "OK":
            print("没有找到过去一周的邮件")
            return

        email_ids = messages[0].split()
        if not email_ids:
            print("过去一周没有收到任何新邮件哦！")
            return
            
        print(f"**过去一周（自 {last_week} 起）共收到 {len(email_ids)} 封新邮件**\n")

        # Fetch the latest 20 to summarize
        for email_id in reversed(email_ids[-20:]):
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
                    print(f"  **摘要**: {body[:150].strip().replace(chr(10), ' ').replace(chr(13), '')}...\n")

        mail.logout()

    except Exception as e:
        print(f"抓取失败: {str(e)}")

if __name__ == "__main__":
    fetch_weekly_emails()
