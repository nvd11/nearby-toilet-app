import sys
import os
import urllib.request

try:
    import fitz
except ImportError:
    os.system("pip install --user PyMuPDF")
    import fitz

pdf_path = '/home/gateman/.openclaw/media/inbound/9c8bc720-f344-4aa0-8446-299dca29ba6a.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document.pdf'

font_url = "https://github.com/google/fonts/raw/main/ofl/mashanzheng/MaShanZheng-Regular.ttf"
font_path = "/home/gateman/.openclaw/workspace/MaShanZheng-Regular.ttf"
if not os.path.exists(font_path):
    urllib.request.urlretrieve(font_url, font_path)

doc = fitz.open(pdf_path)
page = doc[-1]

# Find signature line
rects = page.search_for("签字：")
if rects:
    r = rects[-1]
    p = fitz.Point(r.x1 + 5, r.y1 + 12)
    # Dark blue handwriting
    page.insert_text(p, "潘文林", fontfile=font_path, fontname="hw", fontsize=18, color=(0.1, 0.1, 0.6))

# Find date line
date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 + 12)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=14, color=(0.1, 0.1, 0.6))

# Tick checkboxes
box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 1)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=12, color=(0.1, 0.1, 0.6))

doc.save(out_path)
print(out_path)
