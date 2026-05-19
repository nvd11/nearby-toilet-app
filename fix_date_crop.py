import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 220, 255, cv2.THRESH_BINARY_INV)

# Find the largest contours which should be the text
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Filter by area
contours = [c for c in contours if cv2.contourArea(c) > 50]
if contours:
    # combine all text contours to find the bounding box of the actual date text
    # Assuming the date is the ONLY thing in the center of the image.
    # Let's just find the bounding box of the largest connected components.
    c = np.vstack(contours)
    x, y, w, h = cv2.boundingRect(c)
    
    pad = 20
    x = max(0, x - pad)
    y = max(0, y - pad)
    w = min(img.shape[1] - x, w + 2*pad)
    h = min(img.shape[0] - y, h + 2*pad)
    
    crop = img[y:y+h, x:x+w]
    crop_thresh = thresh[y:y+h, x:x+w]
    alpha = np.clip(crop_thresh.astype(np.float32) * 2.0, 0, 255).astype(np.uint8)
    
    b, g, r = cv2.split(crop)
    rgba = cv2.merge((b, g, r, alpha))
    cv2.imwrite('/home/gateman/.openclaw/workspace/true_date_fixed.png', rgba)
    print("Fixed date crop:", rgba.shape)
