import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

# Let's project on X and Y to find the text line.
proj_y = np.sum(thresh, axis=1)
# Find the largest peak in Y which should be the text line
y_indices = np.where(proj_y > 0)[0]

if len(y_indices) > 0:
    min_y = y_indices[0]
    max_y = y_indices[-1]
    
    proj_x = np.sum(thresh[min_y:max_y, :], axis=0)
    x_indices = np.where(proj_x > 0)[0]
    min_x = x_indices[0]
    max_x = x_indices[-1]
    
    pad = 20
    x = max(0, min_x - pad)
    y = max(0, min_y - pad)
    w = min(img.shape[1] - x, max_x - min_x + 2*pad)
    h = min(img.shape[0] - y, max_y - min_y + 2*pad)
    
    crop = img[y:y+h, x:x+w]
    crop_thresh = thresh[y:y+h, x:x+w]
    alpha = np.clip(crop_thresh.astype(np.float32) * 2.0, 0, 255).astype(np.uint8)
    
    # We only want the text, not stray noise.
    # Keep only the largest connected components in the crop
    contours, _ = cv2.findContours(alpha, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(alpha)
    for c in contours:
        if cv2.contourArea(c) > 50:
            cv2.drawContours(mask, [c], -1, 255, -1)
    
    alpha = cv2.bitwise_and(alpha, mask)
    
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
    cv2.imwrite('/home/gateman/.openclaw/workspace/true_date_fixed2.png', rgba)
    print("Fixed date crop v3:", rgba.shape)

