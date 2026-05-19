import imaplib
import email
from email.header import decode_header
import ssl
import datetime

def fetch_weekly_headers():
    username = "gateman56@gmail.com"
    password = "lekzjeuykwytooxj"
    imap_server = "imap.gmail.com"

    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
        mail.login(username, password)
        mail.select("inbox", readonly=True)

        last_week = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{last_week}")')
        
        if status != "OK":
            print("没有找到过去一周的邮件")
            return

        email_ids = messages[0].split()
        if not email_ids:
            print("过去一周没有收到任何新邮件。")
            return
            
        print(f"**过去一周（自 {last_week} 起）共收到 {len(email_ids)} 封新邮件**\n")

        # Fetch headers only for the latest 30
        for email_id in reversed(email_ids[-30:]):
            # Fetch only specific headers (fast)
            status, msg_data = mail.fetch(email_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject_header = msg.get("Subject", "")
                    if subject_header:
                        subject, encoding = decode_header(subject_header)[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else 'utf-8', errors='ignore')
                    else:
                        subject = "无主题"
                    
                    from_header = msg.get("From", "")
                    if from_header:
                        from_name, encoding = decode_header(from_header)[0]
                        if isinstance(from_name, bytes):
                            from_name = from_name.decode(encoding if encoding else 'utf-8', errors='ignore')
                    else:
                        from_name = "未知发件人"

                    date_ = msg.get("Date", "未知时间")

                    print(f"- **来自**: {from_name}")
                    print(f"  **时间**: {date_}")
                    print(f"  **主题**: {subject}\n")

        mail.logout()

    except Exception as e:
        print(f"抓取失败: {str(e)}")

if __name__ == "__main__":
    fetch_weekly_headers()
