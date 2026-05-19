import cv2
import numpy as np
import pytesseract

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bg = cv2.medianBlur(gray, 99)
diff = cv2.absdiff(gray, bg)
diff = 255 - diff
_, thresh = cv2.threshold(diff, 230, 255, cv2.THRESH_BINARY_INV)

d = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
for i in range(len(d['text'])):
    if int(d['conf'][i]) > 0 and len(d['text'][i].strip()) > 0:
        print(f"Found '{d['text'][i]}' at {d['left'][i]}, {d['top'][i]}, {d['width'][i]}, {d['height'][i]}")
