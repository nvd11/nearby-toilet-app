import sys
import os
import fitz
import cv2

pdf_path = '/home/gateman/.openclaw/media/inbound/c14b5fdc-e57d-49f3-b339-0280d76b0dc5.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_perfect.pdf'

# As seen in the user's screenshot, sig.png is actually the ID, and id.png is actually the signature.
real_id_img = cv2.imread('/home/gateman/.openclaw/workspace/sig.png', cv2.IMREAD_UNCHANGED)
real_sig_img = cv2.imread('/home/gateman/.openclaw/workspace/id.png', cv2.IMREAD_UNCHANGED)

cv2.imwrite('/home/gateman/.openclaw/workspace/final_id.png', real_id_img)
cv2.imwrite('/home/gateman/.openclaw/workspace/final_sig.png', real_sig_img)

doc = fitz.open(pdf_path)
page = doc[-1]

font_path = "/home/gateman/.openclaw/workspace/ZhiMangXing-Regular.ttf"
box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=12, color=(0.1, 0.1, 0.2))

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 - 2)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=14, color=(0.1, 0.1, 0.2))

sh, sw = real_sig_img.shape[:2]
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect_w = 70
    rect_h = rect_w * (sh / sw)
    # Align bottom of signature roughly with the line
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - rect_h + 5, sr.x1 + 10 + rect_w, sr.y1 + 5)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_sig.png')

idh, idw = real_id_img.shape[:2]
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect_w = 160
    rect_h = rect_w * (idh / idw)
    rect = fitz.Rect(ir.x1 + 5, ir.y1 - rect_h + 5, ir.x1 + 5 + rect_w, ir.y1 + 5)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_id.png')

doc.save(out_path)
print(out_path)
