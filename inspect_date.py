import cv2
img = cv2.imread('/home/gateman/.openclaw/media/inbound/4c46c0d4-b625-4be4-b480-800568b313d0.jpg')
h, w = img.shape[:2]
print(f"Original image shape: {w}x{h}")
