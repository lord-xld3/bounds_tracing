# Boundary tracing program

# In this example, we set the "canvas" to all 0's
# Then we draw a continuous shape of 1's

import random
import bounds, flood
import copy

# Right, Down, Left, Up
# To traverse "down" in the image, we need to increment the y coordinate
directions = [(1,0),(0,1),(-1,0),(0,-1)]

# Create an empty img of width x height
img_height = 10
img_width = 10
img = [[0 for _ in range(img_width)] for _ in range(img_height)]
# Clone the mask here to keep it as all "0's"
mask = copy.deepcopy(img)

init_px = (img_width // 2, img_height // 2)
shape_color = 1

def continuous_fill(img, img_height, img_width, pixel):
    x, y = pixel
    if (0 <= x < img_width
    and 0 <= y < img_height
    and img[y][x] == 0):
        if random.randint(0, 10) > 4: # Probability of recursion
            img[y][x] = 1
            continuous_fill(img, img_height, img_width, (x+1, y))
            continuous_fill(img, img_height, img_width, (x-1, y))
            continuous_fill(img, img_height, img_width, (x, y+1))
            continuous_fill(img, img_height, img_width, (x, y-1))
        else: # Different color / boundary, don't fill beyond it
            img[y][x] = 2
            return

# Set the initial pixel to correct color
x, y = init_px
img[y][x] = 1
continuous_fill(img, img_height, img_width, (x+1, y))
continuous_fill(img, img_height, img_width, (x-1, y))
continuous_fill(img, img_height, img_width, (x, y+1))
continuous_fill(img, img_height, img_width, (x, y-1))

print("Image:")
for line in img:
    print(line)

mask = bounds.trace(img, mask, img_height, img_width, init_px, shape_color)

print("Mask:")
for line in mask:
    print(line)

# # Flood fill
# img = flood.fill(img, mask, directions, img_height, img_width, init_px, 3)

# print("Filled:")
# for line in img:
#     print(line)

