import fitz
doc = fitz.open('/home/gateman/.openclaw/media/inbound/c14b5fdc-e57d-49f3-b339-0280d76b0dc5.pdf')
page = doc[-1]

print("签字：", page.search_for("签字："))
print("日期：", page.search_for("日期："))
print("中国身份证：", page.search_for("中国身份证："))
print("☐", page.search_for("☐"))
