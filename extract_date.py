import cv2
import numpy as np

img_path = '/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg'
out_path = '/home/gateman/.openclaw/workspace/true_date.png'

img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff

# The image is quite clear, but lighting is a bit uneven.
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

# Make alpha
alpha = thresh.astype(np.float32)
alpha = np.clip(alpha * 2.0, 0, 255).astype(np.uint8)

# Find bounding box
coords = cv2.findNonZero(alpha)
if coords is not None:
    x,y,w,h = cv2.boundingRect(coords)
    # add some padding just in case
    pad = 20
    x = max(0, x - pad)
    y = max(0, y - pad)
    w = min(img.shape[1] - x, w + 2*pad)
    h = min(img.shape[0] - y, h + 2*pad)
    
    crop_bgr = img[y:y+h, x:x+w]
    alpha = alpha[y:y+h, x:x+w]
    
    b, g, r = cv2.split(crop_bgr)
    rgba = cv2.merge((b, g, r, alpha))
    
    # Deskew
    c_coords = np.column_stack(np.where(alpha > 0))
    if len(c_coords) > 0:
        best_angle = 0
        min_var = float('inf')
        for a in range(-25, 25):
            M = cv2.getRotationMatrix2D((rgba.shape[1]//2, rgba.shape[0]//2), a, 1.0)
            rotated_coords = cv2.transform(np.array([c_coords[:,::-1]]), M)[0]
            var = np.var(rotated_coords[:,1])
            if var < min_var:
                min_var = var
                best_angle = a
                
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
        
        a = rgba[:,:,3]
        rc = cv2.findNonZero(a)
        if rc is not None:
            rx,ry,rw,rh = cv2.boundingRect(rc)
            rgba = rgba[ry:ry+rh, rx:rx+rw]
            
    cv2.imwrite(out_path, rgba)
    print("Date extracted successfully")

