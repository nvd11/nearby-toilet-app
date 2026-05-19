import sys
import os
import fitz
import cv2

pdf_path = '/home/gateman/.openclaw/media/inbound/c14b5fdc-e57d-49f3-b339-0280d76b0dc5.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_fixed.pdf'

# Let's verify which image is which
sig_img = cv2.imread('/home/gateman/.openclaw/workspace/sig.png', cv2.IMREAD_UNCHANGED)
id_img = cv2.imread('/home/gateman/.openclaw/workspace/id.png', cv2.IMREAD_UNCHANGED)
print("sig shape:", sig_img.shape)
print("id shape:", id_img.shape)

# Let's extract again but interactively if we need.
# Wait, I'll just look at the shapes. If ID is wider, it will have a larger width/height ratio.
if sig_img.shape[1] / sig_img.shape[0] > id_img.shape[1] / id_img.shape[0]:
    # Swap them
    print("Swapping sig and id based on aspect ratio")
    temp = sig_img
    sig_img = id_img
    id_img = temp

doc = fitz.open(pdf_path)
page = doc[-1]

# 1. Checkboxes
font_path = "/home/gateman/.openclaw/workspace/ZhiMangXing-Regular.ttf"
box_rects = page.search_for("☐")
for br in box_rects:
    # the box is roughly 10x10.
    bp = fitz.Point(br.x0 + 2, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=12, color=(0.1, 0.1, 0.2))

# 2. Date
date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 - 2)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=14, color=(0.1, 0.1, 0.2))

# 3. Signature
sh, sw = sig_img.shape[:2]
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect_w = 60
    rect_h = rect_w * (sh / sw)
    rect = fitz.Rect(sr.x1 + 10, sr.y0 - rect_h + 15, sr.x1 + 10 + rect_w, sr.y0 + 15)
    
    cv2.imwrite('/home/gateman/.openclaw/workspace/real_sig.png', sig_img)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/real_sig.png')

# 4. ID
idh, idw = id_img.shape[:2]
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect_w = 160
    rect_h = rect_w * (idh / idw)
    rect = fitz.Rect(ir.x1 + 10, ir.y0 - rect_h + 15, ir.x1 + 10 + rect_w, ir.y0 + 15)
    
    cv2.imwrite('/home/gateman/.openclaw/workspace/real_id.png', id_img)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/real_id.png')

doc.save(out_path)
print(out_path)
