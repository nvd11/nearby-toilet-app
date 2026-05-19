import fitz
import cv2

pdf_path = '/home/gateman/.openclaw/media/inbound/6d782395-96d3-415d-afc2-1251c12332b3.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v16.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

# Checkboxes
font_path = "/home/gateman/.openclaw/workspace/Kalam-Light.ttf"
col = (0.35, 0.35, 0.35)
box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 3)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw_l", fontsize=14, color=col)

# Date Image
date_img = cv2.imread('/home/gateman/.openclaw/workspace/true_date_fixed_final.png', cv2.IMREAD_UNCHANGED)
dh, dw = date_img.shape[:2]

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    rect_w = 90  # Give it enough width
    rect_h = rect_w * (dh / dw)
    # the date might have lots of padding, let's adjust Y
    rect = fitz.Rect(dr.x1 + 5, dr.y1 - rect_h + 8, dr.x1 + 5 + rect_w, dr.y1 + 8)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_date_fixed_final.png')

# Signature
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - 24, sr.x1 + 10 + 70, sr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_sig.png')

# ID
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect = fitz.Rect(ir.x1 + 10, ir.y1 - 22, ir.x1 + 10 + 170, ir.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_id.png')

doc.save(out_path)
print(out_path)
