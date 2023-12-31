# For the mandelbrot set, this should be replaced by an escape time algorithm
# You should also mark the color of the pixel on the img
# In this case, we have a predefined img so we can just "look it up"
def get_color(img, pixel):
    x, y = pixel
    return img[y][x]

# i = current index of directions[]
# n = number of shifts to the left
# i + 1 = rotate opposite direction to 2nd position
# i + 3 = rotate current direction to 2nd position

def rotate_directions(directions, i, n):
    d = (i + n) % 4 # 4 is always the length of directions, for this program
    return directions[d:] + directions[:d]

def init_trace(img, mask, img_width, img_height, directions, initial_pixel, boundary_color):
    x, y = initial_pixel  # Extract x and y coordinates
    mask[y][x] = 1 # Always mark the initial pixel as checked
    
    # Check pixels in all directions
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates
        
        # Check if the pixel is out of bounds
        if (new_x < 0 or new_x >= img_width 
        or new_y < 0 or new_y >= img_height):
            continue
        
        # Check if the pixel is a different color than the boundary
        if get_color(img, (new_x, new_y)) != boundary_color:
            mask[new_y][new_x] = 2
            # Set previous pixel as the initial pixel
            initial_pixel = (new_x - dx, new_y - dy)
            directions = rotate_directions(directions, i, 1)
            return mask, initial_pixel, directions
        
        # Else, just mark pixel as checked
        mask[new_y][new_x] = 1
    
    # If we finish the for loop, it means 
    # the initial pixel is surrounded by the same color
    
    # Find the closest direction to the bounds of the image
    # This guarantees that if the shape takes up the full image, 
    # we check the minimum number of pixels
    
    # Right, Down, Left, Up
    distances = [(img_width - x), (img_height - y), x, y]
    d = distances.index(min(distances))
    
    # Rotate closest direction to 0th index
    directions = rotate_directions(directions, d, 0)
    
    # Continue in the closest direction
    dx, dy = directions[0]
    x, y = x + dx, y + dy # Move over once, since its already been checked
    while True:
        new_x, new_y = x + dx, y + dy
        
        # If we don't go out of bounds
        if (0 <= new_x < img_width
        and 0 <= new_y < img_height):
           
            # If it's a different color
            if get_color(img, (new_x, new_y)) != boundary_color:
                mask[new_y][new_x] = 2
            
            else:
                # Same color, keep going
                mask[new_y][new_x] = 1
                x, y = new_x, new_y
                continue
        
        # Fall through (if its a different color) OR (if we go out of bounds)
        initial_pixel = (new_x - dx, new_y - dy)
        
        # In this case, the current direction will always be the 0th index
        # As described in rotate_directions(),
        # this rotates opposite direction to 2nd position
        directions = rotate_directions(directions, 0, 1)
        return mask, initial_pixel, directions      

def main_trace(img, mask, img_width, img_height, directions, current_pixel, initial_pixel, boundary_color):
    x, y = current_pixel  # Extract x and y coordinates
    
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = x + dx, y + dy
        
        # If we go out of bounds
        if (new_x < 0 or new_x >= img_width 
        or new_y < 0 or new_y >= img_height):
            continue

        # If pixel is initial pixel
        if (new_x, new_y) == initial_pixel:

            # Check surrounding pixels
            x, y = new_x, new_y
            for j, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                
                # If we go out of bounds
                if (new_x < 0 or new_x >= img_width 
                or new_y < 0 or new_y >= img_height):
                    continue

                # If pixel is unchecked && pixel is same color as boundary
                if (mask[new_y][new_x] == 0 
                and get_color(img, (new_x, new_y)) == boundary_color):
                    mask[new_y][new_x] = 1
                    directions = rotate_directions(directions, j, 3)
                    return main_trace(img, mask, img_width, img_height, directions, (new_x, new_y), (new_x, new_y), boundary_color)
                
                # Else, continue "for" loop
            
            # We have reached the initial pixel and there are no surrounding pixels of the same color
            return mask
        
        # If pixel has already been checked
        if mask[new_y][new_x] != 0:
            
            # Skip over the checked pixel and check for the same color
            skip_x, skip_y = new_x + dx, new_y + dy

            # If NOT out of bounds
            if (0 <= skip_x < img_width 
            and 0 <= skip_y < img_height):
                
                # If pixel is NOT the boundary color
                if get_color(img, (skip_x, skip_y)) != boundary_color:
                    
                    # Not checked, not out of bounds, not boundary color
                    mask[skip_y][skip_x] = 2
                    
                    # Check pixel in the opposite direction
                    dx, dy = directions[(i + 2) % 4]
                    new_x, new_y = x + dx, y + dy
                    
                    # If this pixel is out of bounds or is already checked
                    if (new_x < 0 or new_x >= img_width 
                    or new_y < 0 or new_y >= img_height
                    or mask[new_y][new_x] != 0):
                        return mask
                    
                    # Else, opposite direction is valid pixel, mark it depending on color
                    mask[new_y][new_x] = (
                        1 if get_color(img, (new_x, new_y)) == boundary_color 
                        else 2
                    )

                    # We just ran into our own tail going counterclockwise
                    # So we're going to flip the direction to hopefully keep going clockwise
                    directions = rotate_directions(directions, i, 1)
                    return main_trace(img, mask, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
                
                # Skip direction is valid and boundary color
                else:
                    mask[skip_y][skip_x] = 1

                    # We also need to backtrack and mark surrounding pixels,
                    # to avoid problems with flood fill
                    for (dx, dy) in directions:
                        
                        back_x, back_y = new_x + dx, new_y + dy

                        # If we go out of bounds
                        if (back_x < 0 or back_x >= img_width
                        or back_y < 0 or back_y >= img_height):
                            continue

                        # If pixel is unchecked
                        if mask[back_y][back_x] == 0:
                            
                            # Even if this pixel is the boundary color,
                            # we're going to mark it as not part of the boundary
                            # because this is a 1 pixel wide "bridge" to something else
                            # and if we traverse that bridge, it will be difficult to get back
                            # ... also it screws with the flood fill algorithm

                            # If its not a 1px bridge, we'll find out shortly 
                            # after we skip a pixel and run into our own tail
                            # but the flood fill will go around it
                            
                            get_color(img, (back_y, back_x)) # Assuming get_color() will mark the image
                            mask[back_y][back_x] = 2
                    
                    # After backtracking, we can fall through

            # Fall through if "skip direction" is out of bounds or boundary color
            directions = rotate_directions(directions, i, 3)
            return main_trace(img, mask, img_width, img_height, directions, (skip_x, skip_y), initial_pixel, boundary_color)
        
        # If pixel is same color as boundary
        if get_color(img, (new_x, new_y)) == boundary_color:
            mask[new_y][new_x] = 1
            directions = rotate_directions(directions, i, 3)
            return main_trace(img, mask, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
        
        # Pixel is different color
        mask[new_y][new_x] = 2
        continue
    
    # We have checked all directions except backwards, backtrack and continue tracing.
    new_x, new_y = x - dx, y - dy
    return main_trace(img, mask, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
