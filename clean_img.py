import cv2
import numpy as np
import fitz

img_path = '/home/gateman/.openclaw/media/inbound/88a367fe-2e5f-4ebf-9798-ae3aafecfff0.jpg'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Better thresholding to remove shadows
# Apply blurring to estimate background
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff

_, thresh = cv2.threshold(diff, 220, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Keep only large contours (actual text)
valid_rects = []
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if w > 50 and h > 50: # filter out tiny noise
        valid_rects.append((x,y,w,h))

# Sort rects by Y coordinate
valid_rects.sort(key=lambda r: r[1])

# We expect two main clumps of text: "潘文林" and "44..."
# Let's merge intersecting/close bounding boxes
def merge_rects(rects, merge_dist=200):
    merged = []
    for r in rects:
        x,y,w,h = r
        merged_with_existing = False
        for i, (mx, my, mw, mh) in enumerate(merged):
            # Check if close
            if (x < mx + mw + merge_dist and x + w + merge_dist > mx and
                y < my + mh + merge_dist and y + h + merge_dist > my):
                # Merge
                nx = min(x, mx)
                ny = min(y, my)
                nw = max(x+w, mx+mw) - nx
                nh = max(y+h, my+mh) - ny
                merged[i] = (nx, ny, nw, nh)
                merged_with_existing = True
                break
        if not merged_with_existing:
            merged.append(r)
    return merged

merged_rects = merge_rects(valid_rects)
# do it a few times to be sure
for _ in range(3):
    merged_rects = merge_rects(merged_rects)

merged_rects.sort(key=lambda r: r[1])
print("Found merged rects:", merged_rects)

if len(merged_rects) >= 2:
    # Top one is signature, bottom is ID
    sig_r = merged_rects[0]
    id_r = merged_rects[1]
    
    def extract_transparent(rect, name):
        x,y,w,h = rect
        crop_gray = gray[y:y+h, x:x+w]
        crop_thresh = thresh[y:y+h, x:x+w]
        
        alpha = crop_thresh.copy()
        
        # Dark blue pen color
        b = np.full_like(crop_gray, 40)
        g = np.full_like(crop_gray, 40)
        r = np.full_like(crop_gray, 40)
        rgba = cv2.merge((b, g, r, alpha))
        cv2.imwrite(name, rgba)

    extract_transparent(sig_r, '/home/gateman/.openclaw/workspace/clean_sig.png')
    extract_transparent(id_r, '/home/gateman/.openclaw/workspace/clean_id.png')

