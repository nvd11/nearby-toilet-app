import cv2
import numpy as np

def deskew(img_path, out_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    if img.shape[2] == 4:
        alpha = img[:,:,3]
        coords = np.column_stack(np.where(alpha > 0))
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        coords = np.column_stack(np.where(gray < 200))
        
    if len(coords) == 0:
        cv2.imwrite(out_path, img)
        return
        
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    # The signature in the image looks like it's rotated clockwise by ~15-20 degrees
    # Let's force a counter-clockwise rotation to make it horizontal
    
    # We can use PCA or minAreaRect, but minAreaRect sometimes gives 90 deg offsets.
    # Let's try to find the best angle that minimizes the vertical variance.
    best_angle = 0
    min_var = float('inf')
    for a in range(-45, 45):
        M = cv2.getRotationMatrix2D((img.shape[1]//2, img.shape[0]//2), a, 1.0)
        rotated_coords = cv2.transform(np.array([coords[:,::-1]]), M)[0]
        var = np.var(rotated_coords[:,1])
        if var < min_var:
            min_var = var
            best_angle = a
            
    print(f"Best angle for {img_path} is {best_angle}")
    
    # Pad image so it doesn't get cut off when rotating
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
    
    # Crop again to tight bounding box
    if rotated.shape[2] == 4:
        alpha = rotated[:,:,3]
        coords = cv2.findNonZero(alpha)
        if coords is not None:
            x,y,w,h = cv2.boundingRect(coords)
            rotated = rotated[y:y+h, x:x+w]
            
    cv2.imwrite(out_path, rotated)

deskew('/home/gateman/.openclaw/workspace/clean_sig.png', '/home/gateman/.openclaw/workspace/flat_sig.png')
deskew('/home/gateman/.openclaw/workspace/clean_id.png', '/home/gateman/.openclaw/workspace/flat_id.png')
