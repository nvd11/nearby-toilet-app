import cv2
import numpy as np

# Let's inspect the original crop to see what color it actually is
sig_rgba = cv2.imread('/home/gateman/.openclaw/workspace/final_perfect_sig.png', cv2.IMREAD_UNCHANGED)
alpha = sig_rgba[:,:,3]
mask = alpha > 100
mean_b = np.mean(sig_rgba[:,:,0][mask])
mean_g = np.mean(sig_rgba[:,:,1][mask])
mean_r = np.mean(sig_rgba[:,:,2][mask])

print(f"Original signature color (BGR): {mean_b}, {mean_g}, {mean_r}")

# Actually wait, in extract_perfect.py I FORCED it to be (30,30,30)!
# No wonder it's black/grey and not matching the exact original pen color if the original pen wasn't (30,30,30)!
# Let's re-extract but KEEP the original color from the photo.

img = cv2.imread('/home/gateman/.openclaw/media/inbound/88a367fe-2e5f-4ebf-9798-ae3aafecfff0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

def get_true_color_crop(x, y, w, h, out_path):
    pad = 200
    ex = max(0, x - pad)
    ey = max(0, y - pad)
    ew = min(gray.shape[1] - ex, w + 2*pad)
    eh = min(gray.shape[0] - ey, h + 2*pad)
    
    crop_bgr = img[ey:ey+eh, ex:ex+ew]
    crop_thresh = thresh[ey:ey+eh, ex:ex+ew]
    
    alpha = crop_thresh.astype(np.float32)
    alpha = np.clip(alpha * 2.0, 0, 255).astype(np.uint8)
    
    coords = cv2.findNonZero(alpha)
    if coords is not None:
        cx,cy,cw,ch = cv2.boundingRect(coords)
        crop_bgr = crop_bgr[cy:cy+ch, cx:cx+cw]
        alpha = alpha[cy:cy+ch, cx:cx+cw]
        
    b, g, r = cv2.split(crop_bgr)
    
    # Actually, because of lighting, the original paper might make the pen look weird.
    # But let's just use the true color from the pixels that have ink.
    # To remove the paper background tint, we can normalize the colors or just use them as is since alpha handles transparency.
    rgba = cv2.merge((b, g, r, alpha))
    
    # deskew
    coords = np.column_stack(np.where(alpha > 0))
    best_angle = 0
    if len(coords) > 0:
        min_var = float('inf')
        for a in range(-25, 25):
            M = cv2.getRotationMatrix2D((rgba.shape[1]//2, rgba.shape[0]//2), a, 1.0)
            rotated_coords = cv2.transform(np.array([coords[:,::-1]]), M)[0]
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
    
    # Calculate average color of the ink for the text font
    m_alpha = rgba[:,:,3] > 100
    avg_b = np.mean(rgba[:,:,0][m_alpha])
    avg_g = np.mean(rgba[:,:,1][m_alpha])
    avg_r = np.mean(rgba[:,:,2][m_alpha])
    
    # calculate average thickness of strokes
    # distance transform can give us stroke thickness
    dist = cv2.distanceTransform(rgba[:,:,3], cv2.DIST_L2, 5)
    thickness = np.mean(dist[m_alpha]) * 2
    
    return avg_b, avg_g, avg_r, thickness

b1, g1, r1, t1 = get_true_color_crop(414, 1263, 1247, 491, '/home/gateman/.openclaw/workspace/true_sig.png')
b2, g2, r2, t2 = get_true_color_crop(360, 2059, 2141, 561, '/home/gateman/.openclaw/workspace/true_id.png')

print(f"Color: {b1},{g1},{r1}  Thickness: {t1}")

