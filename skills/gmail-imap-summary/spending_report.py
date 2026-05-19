import imaplib
import email
from email.header import decode_header
import ssl
import datetime
import re

def decode_mime_words(s):
    if not s: return ""
    results = []
    for word, encoding in decode_header(s):
        if isinstance(word, bytes):
            results.append(word.decode(encoding or 'utf-8', errors='ignore'))
        else:
            results.append(word)
    return "".join(results)

def get_spending():
    username = "gateman56@gmail.com"
    password = "lekzjeuykwytooxj"
    imap_server = "imap.gmail.com"

    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, ssl_context=context)
        mail.login(username, password)
        mail.select("inbox", readonly=True)

        two_weeks_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=14)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{two_weeks_ago}")')
        
        email_ids = messages[0].split()
        if not email_ids:
            print("最近两周没有邮件。")
            return
            
        print(f"正在扫描自 {two_weeks_ago} 以来的账单/收据...\n")

        keywords = ["收据", "receipt", "账单", "bill", "order", "订单", "google play", "payment", "招商银行"]
        
        for e_id in email_ids:
            # Fetch headers first
            status, msg_data = mail.fetch(e_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            if status != "OK": continue
            
            subject = ""
            from_name = ""
            date_ = ""
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_mime_words(msg.get("Subject", ""))
                    from_name = decode_mime_words(msg.get("From", ""))
                    date_ = msg.get("Date", "")
            
            # Check if it's a bill
            is_bill = any(kw.lower() in subject.lower() or kw.lower() in from_name.lower() for kw in keywords)
            if is_bill:
                # Fetch full email
                status, full_data = mail.fetch(e_id, "(RFC822)")
                for response_part in full_data:
                    if isinstance(response_part, tuple):
                        full_msg = email.message_from_bytes(response_part[1])
                        
                        body = ""
                        if full_msg.is_multipart():
                            for part in full_msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                        else:
                            body = full_msg.get_payload(decode=True).decode(full_msg.get_content_charset() or 'utf-8', errors='ignore')
                        
                        # Extract currency amounts
                        # Match HK$, $, ¥, USD, HKD followed by numbers
                        amounts = re.findall(r'(HK\$|HKD|\$|¥|USD|RMB|CNY)\s*\d+(?:\.\d{2})?', body, re.IGNORECASE)
                        amount_context = []
                        for line in body.splitlines():
                            if any(curr in line.upper() for curr in ['HK$', 'HKD', '$', '¥', 'USD', 'RMB', 'CNY', 'TOTAL', '合计', '总计', '金额']):
                                if line.strip() and len(line) < 100:
                                    amount_context.append(line.strip())
                        
                        print(f"[{date_}]")
                        print(f"来源: {from_name} | 主题: {subject}")
                        if amount_context:
                            print("相关金额内容: ", " | ".join(amount_context[:5]))
                        else:
                            print("相关金额内容: 未直接提取到明文数字")
                        print("-" * 50)
                        
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_spending()
