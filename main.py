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
img_height = 6
img_width = 6
img = [[0 for _ in range(img_width)] for _ in range(img_height)]
# Clone the mask here to keep it as all "0's"
mask = copy.deepcopy(img)

# Draw a random shape and pick a random, valid starting point
shape_size = (random.randint(3, img_width), random.randint(3, img_height))
shape_init = (random.randint(0, img_width - shape_size[0]), random.randint(0, img_height - shape_size[1]))

# Draw a random continuous shape of color 1
for x in range(shape_init[0], shape_init[0] + shape_size[0]):
    for y in range(shape_init[1], shape_init[1] + shape_size[1]):
        img[y][x] = 1

# Starting pixel and color must be within the shape
# For now, just try to start in the center of the shape
initial_pixel = (shape_init[0] + (shape_size[0] // 2), shape_init[1] + (shape_size[1] // 2))
boundary_color = img[initial_pixel[1]][initial_pixel[0]]

print("Image:")
for line in img:
    print(line)

# Initialize tracing
mask, initial_pixel, directions = bounds.init_trace(img, mask, img_width, img_height, directions, initial_pixel, boundary_color)

# Start main trace
mask = bounds.main_trace(img, mask, img_width, img_height, directions, initial_pixel, initial_pixel, boundary_color)

print("Mask:")
for line in mask:
    print(line)

# Flood fill
img = flood.fill(img, mask, directions, img_height, img_width, initial_pixel, 3)

print("Filled:")
for line in img:
    print(line)

