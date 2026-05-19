import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg', cv2.IMREAD_GRAYSCALE)
bg = cv2.medianBlur(img, 99)
diff = cv2.absdiff(img, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i, c in enumerate(contours):
    x,y,w,h = cv2.boundingRect(c)
    if w > 50 and h > 20 and w < 1000 and h < 500:
        print(f"Contour {i}: x={x}, y={y}, w={w}, h={h}")

