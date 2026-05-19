import sys
import os
import cv2
import numpy as np
import fitz

img_path = '/home/gateman/.openclaw/media/inbound/88a367fe-2e5f-4ebf-9798-ae3aafecfff0.jpg'
pdf_path = '/home/gateman/.openclaw/media/inbound/07488063-5a83-4185-b0bb-d25271940dde.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_real.pdf'

img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Normalize and create alpha
gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
# Apply adaptive threshold to handle uneven lighting
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 51, 15)

alpha = 255 - thresh

# Remove noise
kernel = np.ones((2,2), np.uint8)
alpha = cv2.morphologyEx(alpha, cv2.MORPH_OPEN, kernel)
alpha = cv2.GaussianBlur(alpha, (3,3), 0)
alpha = np.clip(alpha * 1.5, 0, 255).astype(np.uint8)

# Make it a dark blue/black pen color
b = np.full_like(gray, 40)
g = np.full_like(gray, 40)
r = np.full_like(gray, 40)
rgba = cv2.merge((b, g, r, alpha))

h, w = gray.shape
split_y = int(h * 0.55)

sig_rgba = rgba[0:split_y, :]
id_rgba = rgba[split_y:h, :]

def crop_to_content(img_rgba):
    a = img_rgba[:,:,3]
    coords = cv2.findNonZero(a)
    if coords is not None:
        x,y,w,h = cv2.boundingRect(coords)
        return img_rgba[y:y+h, x:x+w]
    return img_rgba

sig_cropped = crop_to_content(sig_rgba)
id_cropped = crop_to_content(id_rgba)

cv2.imwrite('/home/gateman/.openclaw/workspace/sig.png', sig_cropped)
cv2.imwrite('/home/gateman/.openclaw/workspace/id.png', id_cropped)

# Now PDF
doc = fitz.open(pdf_path)
page = doc[-1]

# 1. Checkboxes
font_path = "/home/gateman/.openclaw/workspace/ZhiMangXing-Regular.ttf"
box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=16, color=(0.1, 0.1, 0.2))

# 2. Date
date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 + 8)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=18, color=(0.1, 0.1, 0.2))

# 3. Signature
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    # Calculate aspect ratio
    sh, sw = sig_cropped.shape[:2]
    rect_w = 60
    rect_h = rect_w * (sh / sw)
    rect = fitz.Rect(sr.x1 + 5, sr.y1 - rect_h + 10, sr.x1 + 5 + rect_w, sr.y1 + 10)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/sig.png')

# 4. ID
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    idh, idw = id_cropped.shape[:2]
    rect_w = 120
    rect_h = rect_w * (idh / idw)
    rect = fitz.Rect(ir.x1 + 5, ir.y1 - rect_h + 10, ir.x1 + 5 + rect_w, ir.y1 + 10)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/id.png')

doc.save(out_path)
print(out_path)
