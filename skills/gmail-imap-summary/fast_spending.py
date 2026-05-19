import imaplib
import email
from email.header import decode_header
import ssl
import datetime

def get_fast_spending():
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
        
        for e_id in reversed(email_ids):
            # Fetch headers only
            status, msg_data = mail.fetch(e_id, "(BODY.PEEK[HEADER.FIELDS (SUBJECT FROM DATE)])")
            if status != "OK": continue
            
            subject = ""
            from_name = ""
            date_ = ""
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    sub_raw = msg.get("Subject", "")
                    if sub_raw:
                        dec = decode_header(sub_raw)[0]
                        subject = dec[0].decode(dec[1] or 'utf-8', errors='ignore') if isinstance(dec[0], bytes) else dec[0]
                    
                    from_raw = msg.get("From", "")
                    if from_raw:
                        dec = decode_header(from_raw)[0]
                        from_name = dec[0].decode(dec[1] or 'utf-8', errors='ignore') if isinstance(dec[0], bytes) else dec[0]
                    
                    date_ = msg.get("Date", "")
            
            # Check if it's a bill
            is_bill = False
            for kw in keywords:
                if kw.lower() in subject.lower() or kw.lower() in from_name.lower():
                    is_bill = True
                    break
                    
            if is_bill:
                print(f"[{date_}] {from_name} : {subject}")
                
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_fast_spending()
