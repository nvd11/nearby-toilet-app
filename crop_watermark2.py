from PIL import Image
import sys

img_path = sys.argv[1]
out_path = sys.argv[2]

img = Image.open(img_path)
width, height = img.size

# Doubao watermarks can be quite high from the bottom edge
# Let's crop the bottom 140 pixels to be absolutely sure.
# Also, we can crop the left and right edges slightly if it's on the side, but usually it's at the bottom.
cropped_img = img.crop((0, 0, width, height - 160))
cropped_img.save(out_path)
print(f"Original size: {width}x{height}, New size: {cropped_img.size}")
