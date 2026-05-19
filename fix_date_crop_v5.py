import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

# Find all contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
valid_rects = []
for c in contours:
    x,y,cw,ch = cv2.boundingRect(c)
    # keep reasonable sized contours
    if cw > 15 and ch > 15 and cw < 800 and ch < 800:
        valid_rects.append((x,y,cw,ch))

if valid_rects:
    # Just take the min x, min y, max x, max y of ALL valid text blobs in the image!
    min_x = min([r[0] for r in valid_rects])
    min_y = min([r[1] for r in valid_rects])
    max_x = max([r[0]+r[2] for r in valid_rects])
    max_y = max([r[1]+r[3] for r in valid_rects])
    
    pad = 30
    fx = max(0, min_x - pad)
    fy = max(0, min_y - pad)
    fw = min(img.shape[1] - fx, max_x - min_x + 2*pad)
    fh = min(img.shape[0] - fy, max_y - min_y + 2*pad)
    
    crop = img[fy:fy+fh, fx:fx+fw]
    crop_thresh = thresh[fy:fy+fh, fx:fx+fw]
    alpha = np.clip(crop_thresh.astype(np.float32) * 2.0, 0, 255).astype(np.uint8)
    
    b, g, r = cv2.split(crop)
    rgba = cv2.merge((b, g, r, alpha))
    
    # Let's save a diagnostic to ensure we got it all
    cv2.imwrite('/home/gateman/.openclaw/workspace/true_date_fixed_final.png', rgba)
    print("Fixed date crop v5:", rgba.shape)
