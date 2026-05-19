from PIL import Image, ImageDraw
import sys

img_path = sys.argv[1]
out_path = sys.argv[2]

img = Image.open(img_path).convert("RGB")
width, height = img.size

draw = ImageDraw.Draw(img)

# The watermark "豆包AI生成" is usually very small and right at the bottom edge.
# Let's cover ONLY the bottom 40 pixels on the far right (e.g. from x=2000 to 2273, y=1240 to 1280)
# This should avoid the address which is likely slightly higher.

bg_color = img.getpixel((2000, height - 60)) # sample color just above the watermark

# Draw a small rectangle over just the very bottom right corner
draw.rectangle([1900, height - 40, width, height], fill=bg_color)

img.save(out_path)
print(f"Size: {width}x{height}, filled rectangle with color {bg_color}")
