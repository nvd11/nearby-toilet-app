from PIL import Image, ImageDraw
import sys

img_path = sys.argv[1]
out_path = sys.argv[2]

img = Image.open(img_path).convert("RGB")
width, height = img.size

draw = ImageDraw.Draw(img)

# We want to cover the bottom right corner where the watermark is.
# The watermark "豆包AI生成" is at the very bottom right.
# Let's say from x=1800 to width, and y=1150 to height.
# We will pick the background color just to the left of this area.
bg_color = img.getpixel((1750, 1220))

# Draw a rectangle over the watermark
draw.rectangle([1800, 1150, width, height], fill=bg_color)

img.save(out_path)
print(f"Filled rectangle with color {bg_color}")
