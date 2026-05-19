import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 15)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
dilated = cv2.dilate(thresh, kernel, iterations=3)

contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

min_x, min_y, max_x, max_y = img.shape[1], img.shape[0], 0, 0
found = False

for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if y > 1500 and y < 2500 and w > 20 and h > 20: # Middle of the image
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
        found = True

if found:
    pad = 20
    x1 = max(0, min_x - pad)
    y1 = max(0, min_y - pad)
    x2 = min(img.shape[1], max_x + pad)
    y2 = min(img.shape[0], max_y + pad)
    
    crop = img[y1:y2, x1:x2]
    crop_thresh = thresh[y1:y2, x1:x2]
    
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

    cv2.imwrite('/home/gateman/.openclaw/workspace/true_date_perfect.png', rgba)
    print("Saved perfect date crop:", rgba.shape)

