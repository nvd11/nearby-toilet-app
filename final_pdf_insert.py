import fitz
import cv2

pdf_path = '/home/gateman/.openclaw/media/inbound/c14b5fdc-e57d-49f3-b339-0280d76b0dc5.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v4.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

# Font for Date and Checkboxes
font_path = "/home/gateman/.openclaw/workspace/ZhiMangXing-Regular.ttf"

# Checkboxes
box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=12, color=(0.1, 0.1, 0.2))

# Date
date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 - 2)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=14, color=(0.1, 0.1, 0.2))

# Signature
sig_img = cv2.imread('/home/gateman/.openclaw/workspace/clean_sig.png', cv2.IMREAD_UNCHANGED)
sh, sw = sig_img.shape[:2]
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect_w = 60
    rect_h = rect_w * (sh / sw)
    rect = fitz.Rect(sr.x1 + 5, sr.y1 - rect_h, sr.x1 + 5 + rect_w, sr.y1)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/clean_sig.png')

# ID
id_img = cv2.imread('/home/gateman/.openclaw/workspace/clean_id.png', cv2.IMREAD_UNCHANGED)
idh, idw = id_img.shape[:2]
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect_w = 120
    rect_h = rect_w * (idh / idw)
    rect = fitz.Rect(ir.x1 + 5, ir.y1 - rect_h, ir.x1 + 5 + rect_w, ir.y1)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/clean_id.png')

doc.save(out_path)
print(out_path)
