from PIL import Image, ImageDraw
import sys

img_path = sys.argv[1]
out_path = sys.argv[2]

img = Image.open(img_path)
width, height = img.size

# In the bottom right corner, we have "AI生成" text
# Let's crop it out or cover it. It's overlapping with some text, maybe we just cover the exact "AI生成" box
# Let's use a patch of the red background from nearby
draw = ImageDraw.Draw(img)
# Coordinates for bottom right (approximate, we need to guess)
# We can take a slice from just above it and paste it over
box_width = 150
box_height = 50
x = width - box_width
y = height - box_height

# copy a patch from above it
patch = img.crop((x, y - box_height, width, y))
img.paste(patch, (x, y))

img.save(out_path)
print("Done")
