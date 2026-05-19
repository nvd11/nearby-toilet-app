import fitz

pdf_path = '/home/gateman/.openclaw/media/inbound/4d8300d9-62d3-4f75-8955-abe8543c88e1.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v8.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

font_path = "/home/gateman/.openclaw/workspace/Kalam.ttf"

box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    # Checkbox check with Kalam
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw_k", fontsize=14, color=(0.12, 0.12, 0.12))

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 10, dr.y1 - 2)
    # Date with Kalam handwritten digits, dark blue/black
    page.insert_text(dp, "2026.04.23", fontfile=font_path, fontname="hw_k", fontsize=16, color=(0.12, 0.12, 0.12))

# Signature and ID
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - 24, sr.x1 + 10 + 70, sr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_perfect_sig.png')

id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect = fitz.Rect(ir.x1 + 10, ir.y1 - 22, ir.x1 + 10 + 170, ir.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_perfect_id.png')

doc.save(out_path)
print(out_path)
