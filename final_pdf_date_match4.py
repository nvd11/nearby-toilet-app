import fitz

pdf_path = '/home/gateman/.openclaw/media/inbound/6d782395-96d3-415d-afc2-1251c12332b3.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v12.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

font_path = "/home/gateman/.openclaw/workspace/ReenieBeanie.ttf"

# Match the faint greyish pencil/pen look
col = (0.35, 0.35, 0.35)

box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 1)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw_rb", fontsize=15, color=col)

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 10, dr.y1 - 1)
    # ReenieBeanie is very scribbly/informal, great for realistic handwriting
    page.insert_text(dp, "2026. 04. 23", fontfile=font_path, fontname="hw_rb", fontsize=18, color=col)

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
