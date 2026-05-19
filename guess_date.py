import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

rects = []
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    if w > 20 and h > 20 and w < 1000 and h < 800:
        rects.append([x, y, x+w, y+h])

# Group rects that are close horizontally
rects = sorted(rects, key=lambda r: r[0])

grouped = []
for r in rects:
    x1, y1, x2, y2 = r
    merged = False
    for i, gr in enumerate(grouped):
        gx1, gy1, gx2, gy2 = gr
        # If they overlap vertically and are close horizontally
        if max(y1, gy1) < min(y2, gy2) + 50 and x1 < gx2 + 150:
            grouped[i] = [min(x1, gx1), min(y1, gy1), max(x2, gx2), max(y2, gy2)]
            merged = True
            break
    if not merged:
        grouped.append(r)

for g in grouped:
    x1, y1, x2, y2 = g
    w = x2 - x1
    h = y2 - y1
    print(f"Group: x={x1}, y={y1}, w={w}, h={h}")

