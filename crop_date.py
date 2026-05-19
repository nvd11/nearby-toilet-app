import cv2
import numpy as np

img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
# crop around the middle where the date is likely to be
h, w = img.shape[:2]
crop = img[int(h*0.3):int(h*0.7), int(w*0.1):int(w*0.9)]

cv2.imwrite('/home/gateman/.openclaw/workspace/date_crop_test.jpg', crop)
