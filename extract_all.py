import cv2
import numpy as np

img_path = '/home/gateman/.openclaw/media/inbound/88a367fe-2e5f-4ebf-9798-ae3aafecfff0.jpg'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff

_, thresh = cv2.threshold(diff, 220, 255, cv2.THRESH_BINARY_INV)

h, w = thresh.shape
split_y = int(h * 0.55)

# Top half = ID (wait, earlier I found out top half is ID, bottom half is signature!)
# Let's verify by size again, or just split them and check aspect ratio.
top_thresh = thresh[0:split_y, :]
bot_thresh = thresh[split_y:h, :]

def get_crop(thresh_img, gray_img):
    coords = cv2.findNonZero(thresh_img)
    if coords is not None:
        x,y,w,h = cv2.boundingRect(coords)
        crop_gray = gray_img[y:y+h, x:x+w]
        crop_thresh = thresh_img[y:y+h, x:x+w]
        alpha = crop_thresh.copy()
        b = np.full_like(crop_gray, 40)
        g = np.full_like(crop_gray, 40)
        r = np.full_like(crop_gray, 40)
        return cv2.merge((b, g, r, alpha))
    return None

top_rgba = get_crop(top_thresh, gray[0:split_y, :])
bot_rgba = get_crop(bot_thresh, gray[split_y:h, :])

if top_rgba.shape[1] / top_rgba.shape[0] > bot_rgba.shape[1] / bot_rgba.shape[0]:
    # Top is wider, so Top is ID
    cv2.imwrite('/home/gateman/.openclaw/workspace/all_id.png', top_rgba)
    cv2.imwrite('/home/gateman/.openclaw/workspace/all_sig.png', bot_rgba)
else:
    cv2.imwrite('/home/gateman/.openclaw/workspace/all_sig.png', top_rgba)
    cv2.imwrite('/home/gateman/.openclaw/workspace/all_id.png', bot_rgba)

