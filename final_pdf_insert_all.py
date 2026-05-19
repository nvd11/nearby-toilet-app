import fitz
import cv2
import numpy as np

def deskew(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    alpha = img[:,:,3]
    coords = np.column_stack(np.where(alpha > 0))
    best_angle = 0
    min_var = float('inf')
    for a in range(-45, 45):
        M = cv2.getRotationMatrix2D((img.shape[1]//2, img.shape[0]//2), a, 1.0)
        rotated_coords = cv2.transform(np.array([coords[:,::-1]]), M)[0]
        var = np.var(rotated_coords[:,1])
        if var < min_var:
            min_var = var
            best_angle = a
            
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    
    abs_cos = abs(M[0,0])
    abs_sin = abs(M[0,1])
    bound_w = int(h * abs_sin + w * abs_cos)
    bound_h = int(h * abs_cos + w * abs_sin)
    M[0, 2] += bound_w/2 - center[0]
    M[1, 2] += bound_h/2 - center[1]
    
    rotated = cv2.warpAffine(img, M, (bound_w, bound_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    
    alpha = rotated[:,:,3]
    coords = cv2.findNonZero(alpha)
    if coords is not None:
        x,y,w,h = cv2.boundingRect(coords)
        rotated = rotated[y:y+h, x:x+w]
        
    cv2.imwrite(out_path, rotated)

deskew('/home/gateman/.openclaw/workspace/all_sig.png', '/home/gateman/.openclaw/workspace/flat_all_sig.png')
deskew('/home/gateman/.openclaw/workspace/all_id.png', '/home/gateman/.openclaw/workspace/flat_all_id.png')

pdf_path = '/home/gateman/.openclaw/media/inbound/993a1338-0ee8-4e41-aa3a-84fadf9399ac.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v6.pdf'

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

sig_img = cv2.imread('/home/gateman/.openclaw/workspace/flat_all_sig.png', cv2.IMREAD_UNCHANGED)
sh, sw = sig_img.shape[:2]
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect_w = 60
    rect_h = rect_w * (sh / sw)
    rect = fitz.Rect(sr.x1 + 5, sr.y1 - rect_h, sr.x1 + 5 + rect_w, sr.y1)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/flat_all_sig.png')

id_img = cv2.imread('/home/gateman/.openclaw/workspace/flat_all_id.png', cv2.IMREAD_UNCHANGED)
idh, idw = id_img.shape[:2]
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect_w = 120
    rect_h = rect_w * (idh / idw)
    rect = fitz.Rect(ir.x1 + 5, ir.y1 - rect_h, ir.x1 + 5 + rect_w, ir.y1)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/flat_all_id.png')

doc.save(out_path)
print(out_path)
