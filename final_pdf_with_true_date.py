import fitz
import cv2

pdf_path = '/home/gateman/.openclaw/media/inbound/6d782395-96d3-415d-afc2-1251c12332b3.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v13.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

# Checkboxes (using simple font)
font_path = "/home/gateman/.openclaw/workspace/Kalam-Light.ttf"
col = (0.35, 0.35, 0.35)

box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 3)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw_l", fontsize=14, color=col)

# Real Date Image
date_img = cv2.imread('/home/gateman/.openclaw/workspace/true_date.png', cv2.IMREAD_UNCHANGED)
dh, dw = date_img.shape[:2]

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    rect_w = 90
    rect_h = rect_w * (dh / dw)
    rect = fitz.Rect(dr.x1 + 5, dr.y1 - rect_h + 3, dr.x1 + 5 + rect_w, dr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_date.png')

# Real Signature Image
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - 24, sr.x1 + 10 + 70, sr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_sig.png')

# Real ID Image
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect = fitz.Rect(ir.x1 + 10, ir.y1 - 22, ir.x1 + 10 + 170, ir.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_id.png')

doc.save(out_path)
print(out_path)
