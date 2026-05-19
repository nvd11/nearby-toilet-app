import cv2
import numpy as np
import fitz

img_path = '/home/gateman/.openclaw/media/inbound/88a367fe-2e5f-4ebf-9798-ae3aafecfff0.jpg'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff

# Lower threshold to catch faint strokes
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

# The bounding boxes we found earlier:
# sig: (414, 1263, 1247, 491)
# id: (360, 2059, 2141, 561)
# Let's expand them by 150 pixels in all directions to catch the missing strokes!
def get_expanded_crop(x, y, w, h, out_path, is_sig=False):
    pad = 200
    ex = max(0, x - pad)
    ey = max(0, y - pad)
    ew = min(gray.shape[1] - ex, w + 2*pad)
    eh = min(gray.shape[0] - ey, h + 2*pad)
    
    crop_gray = gray[ey:ey+eh, ex:ex+ew]
    crop_thresh = thresh[ey:ey+eh, ex:ex+ew]
    
    # Amplify alpha so it's not faint
    alpha = crop_thresh.astype(np.float32)
    alpha = np.clip(alpha * 2.0, 0, 255).astype(np.uint8)
    
    # Trim empty space
    coords = cv2.findNonZero(alpha)
    if coords is not None:
        cx,cy,cw,ch = cv2.boundingRect(coords)
        crop_gray = crop_gray[cy:cy+ch, cx:cx+cw]
        alpha = alpha[cy:cy+ch, cx:cx+cw]
    
    # Pure dark blue/black ink color
    b = np.full_like(crop_gray, 30)
    g = np.full_like(crop_gray, 30)
    r = np.full_like(crop_gray, 30)
    
    rgba = cv2.merge((b, g, r, alpha))
    
    # Deskew
    coords = np.column_stack(np.where(alpha > 0))
    if len(coords) > 0:
        best_angle = 0
        min_var = float('inf')
        # Check angles -45 to 45
        for a in range(-25, 25):
            M = cv2.getRotationMatrix2D((rgba.shape[1]//2, rgba.shape[0]//2), a, 1.0)
            rotated_coords = cv2.transform(np.array([coords[:,::-1]]), M)[0]
            var = np.var(rotated_coords[:,1])
            if var < min_var:
                min_var = var
                best_angle = a
        
        print(f"Angle for {out_path}: {best_angle}")
        h_img, w_img = rgba.shape[:2]
        center = (w_img // 2, h_img // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        
        abs_cos = abs(M[0,0])
        abs_sin = abs(M[0,1])
        bound_w = int(h_img * abs_sin + w_img * abs_cos)
        bound_h = int(h_img * abs_cos + w_img * abs_sin)
        M[0, 2] += bound_w/2 - center[0]
        M[1, 2] += bound_h/2 - center[1]
        
        rgba = cv2.warpAffine(rgba, M, (bound_w, bound_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        
        # final trim
        a = rgba[:,:,3]
        rc = cv2.findNonZero(a)
        if rc is not None:
            rx,ry,rw,rh = cv2.boundingRect(rc)
            rgba = rgba[ry:ry+rh, rx:rx+rw]
            
    cv2.imwrite(out_path, rgba)
    return rgba

sig_rgba = get_expanded_crop(414, 1263, 1247, 491, '/home/gateman/.openclaw/workspace/final_perfect_sig.png', True)
id_rgba = get_expanded_crop(360, 2059, 2141, 561, '/home/gateman/.openclaw/workspace/final_perfect_id.png', False)

# Now PDF
pdf_path = '/home/gateman/.openclaw/media/inbound/ac9e01cc-e16d-4abc-84e5-b4d032475332.pdf' # No wait, use original!
# Actually original is 9c8bc720-f344-4aa0-8446-299dca29ba6a.pdf
pdf_path = '/home/gateman/.openclaw/media/inbound/9c8bc720-f344-4aa0-8446-299dca29ba6a.pdf'
out_path = '/home/gateman/.openclaw/workspace/signed_document_v7.pdf'

doc = fitz.open(pdf_path)
page = doc[-1]

font_path = "/home/gateman/.openclaw/workspace/ZhiMangXing-Regular.ttf"

box_rects = page.search_for("☐")
for br in box_rects:
    bp = fitz.Point(br.x0 + 1, br.y1 - 2)
    page.insert_text(bp, "√", fontfile=font_path, fontname="hw", fontsize=14, color=(0.1, 0.1, 0.2))

date_rects = page.search_for("日期：")
if date_rects:
    dr = date_rects[-1]
    dp = fitz.Point(dr.x1 + 5, dr.y1 - 2)
    page.insert_text(dp, "2026-04-23", fontfile=font_path, fontname="hw", fontsize=16, color=(0.1, 0.1, 0.2))

sh, sw = sig_rgba.shape[:2]
sig_rects = page.search_for("签字：")
if sig_rects:
    sr = sig_rects[-1]
    rect_w = 70
    rect_h = rect_w * (sh / sw)
    # Put it strictly after "签字："
    rect = fitz.Rect(sr.x1 + 10, sr.y1 - rect_h + 3, sr.x1 + 10 + rect_w, sr.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_perfect_sig.png')

idh, idw = id_rgba.shape[:2]
id_rects = page.search_for("中国身份证：")
if id_rects:
    ir = id_rects[-1]
    rect_w = 170
    rect_h = rect_w * (idh / idw)
    # Put it strictly after "中国身份证："
    rect = fitz.Rect(ir.x1 + 10, ir.y1 - rect_h + 3, ir.x1 + 10 + rect_w, ir.y1 + 3)
    page.insert_image(rect, filename='/home/gateman/.openclaw/workspace/final_perfect_id.png')

doc.save(out_path)
print(out_path)

