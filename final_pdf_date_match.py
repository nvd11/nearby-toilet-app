import fitz

pdf_path = '/home/gateman/.openclaw/media/inbound/7fed1e30-1d23-4bd5-96b8-cd59b1e7d360.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v9.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

font_path = "/home/gateman/.openclaw/workspace/Kalam.ttf"
# We'll use bold if possible, but Kalam doesn't have bold.
# We can simulate bold by drawing the text multiple times with slight offsets or using a bigger size.
# Actually, Kalam-Bold exists. Let's download it.
font_path = "/home/gateman/.openclaw/workspace/Kalam-Bold.ttf"

# The color extracted was around (67, 67, 67) BGR, which is ~ #434343.
# PyMuPDF color is RGB (0 to 1). So r=67/255, g=67/255, b=67/255 -> ~0.26
col = (67/255.0, 67/255.0, 67/255.0)

box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hwb", fontsize=16, color=col)

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 10, dr.y1 - 2)
    page.insert_text(dp, "2026.04.23", fontfile=font_path, fontname="hwb", fontsize=18, color=col)

sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - 24, sr.x1 + 10 + 70, sr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_sig.png')

id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect = fitz.Rect(ir.x1 + 10, ir.y1 - 22, ir.x1 + 10 + 170, ir.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/true_id.png')

doc.save(out_path)
print(out_path)
