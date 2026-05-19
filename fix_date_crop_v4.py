import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

h, w = thresh.shape
# The user probably centered the date. Crop to center 60%
cy1, cy2 = int(h*0.2), int(h*0.8)
cx1, cx2 = int(w*0.2), int(w*0.8)

thresh_center = thresh[cy1:cy2, cx1:cx2]

contours, _ = cv2.findContours(thresh_center, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
valid_rects = []
for c in contours:
    x,y,cw,ch = cv2.boundingRect(c)
    if cw > 20 and ch > 20 and cw < 500 and ch < 500:
        valid_rects.append((x,y,cw,ch))

if valid_rects:
    # merge them to find the text line
    valid_rects.sort(key=lambda r: r[0])
    # just find min x, min y, max x, max y of valid rects
    min_x = min([r[0] for r in valid_rects])
    min_y = min([r[1] for r in valid_rects])
    max_x = max([r[0]+r[2] for r in valid_rects])
    max_y = max([r[1]+r[3] for r in valid_rects])
    
    pad = 20
    fx = max(0, cx1 + min_x - pad)
    fy = max(0, cy1 + min_y - pad)
    fw = min(w - fx, max_x - min_x + 2*pad)
    fh = min(h - fy, max_y - min_y + 2*pad)
    
    crop = img[fy:fy+fh, fx:fx+fw]
    crop_thresh = thresh[fy:fy+fh, fx:fx+fw]
    alpha = np.clip(crop_thresh.astype(np.float32) * 2.0, 0, 255).astype(np.uint8)
    
    # Deskew
    c_coords = np.column_stack(np.where(alpha > 0))
    if len(c_coords) > 0:
        best_angle = 0
        min_var = float('inf')
        for a in range(-25, 25):
            M = cv2.getRotationMatrix2D((alpha.shape[1]//2, alpha.shape[0]//2), a, 1.0)
            rotated_coords = cv2.transform(np.array([c_coords[:,::-1]]), M)[0]
            var = np.var(rotated_coords[:,1])
            if var < min_var:
                min_var = var
                best_angle = a
                
        h_img, w_img = alpha.shape[:2]
        center = (w_img // 2, h_img // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        
        abs_cos = abs(M[0,0])
        abs_sin = abs(M[0,1])
        bound_w = int(h_img * abs_sin + w_img * abs_cos)
        bound_h = int(h_img * abs_cos + w_img * abs_sin)
        M[0, 2] += bound_w/2 - center[0]
        M[1, 2] += bound_h/2 - center[1]
        
        alpha = cv2.warpAffine(alpha, M, (bound_w, bound_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        crop = cv2.warpAffine(crop, M, (bound_w, bound_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
        
        rc = cv2.findNonZero(alpha)
        if rc is not None:
            rx,ry,rw,rh = cv2.boundingRect(rc)
            alpha = alpha[ry:ry+rh, rx:rx+rw]
            crop = crop[ry:ry+rh, rx:rx+rw]

    b, g, r = cv2.split(crop)
    rgba = cv2.merge((b, g, r, alpha))
    cv2.imwrite('/home/gateman/.openclaw/workspace/true_date_fixed3.png', rgba)
    print("Fixed date crop v4:", rgba.shape)

