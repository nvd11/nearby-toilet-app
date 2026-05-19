from PIL import Image
import sys

img_path = sys.argv[1]
out_path = sys.argv[2]

img = Image.open(img_path)
width, height = img.size

# Let's see if the watermark is a strip at the bottom
# We will just crop the bottom 45 pixels off. This usually removes bottom-corner watermarks.
cropped_img = img.crop((0, 0, width, height - 45))
cropped_img.save(out_path)
print(f"Original size: {width}x{height}, New size: {cropped_img.size}")
