# i = current index of directions[]
# n = number of shifts to the left
# i + 1 = rotate opposite direction to 2nd position
# i + 3 = rotate current direction to 2nd position

def rotate_directions(directions, i, n):
    d = (i + n) % 4
    return directions[d:] + directions[:d]

def init_trace(img, img_width, img_height, directions, initial_pixel, boundary_color):
    x, y = initial_pixel  # Extract x and y coordinates
    
    # Check pixels in all directions
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates
        
        # Check if the pixel is out of bounds
        if (new_x < 0 or new_x >= img_width 
        or new_y < 0 or new_y >= img_height):
            continue
        
        # Check if the pixel is a different color than the initial pixel
        if img[new_y][new_x] != boundary_color:
            img[new_y][new_x] = 2 # 2 indicates that the pixel has been checked
            # Set previous pixel as the initial pixel
            initial_pixel = (new_x - dx, new_y - dy)
            directions = rotate_directions(directions, i, 1)
            return img, initial_pixel, directions
        
        # Mark pixel as checked
        img[new_y][new_x] = 2
    
    # If we finish the for loop, it means the initial pixel is surrounded by the same color
    img[y][x] = 2
    # Continue in the initial direction
    dx, dy = directions[0]
    x, y = x + dx, y + dy # Move over once, since its already been checked
    while True:
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates

        # If we go out of bounds
        if (new_x < 0 or new_x >= img_width 
        or new_y < 0 or new_y >= img_height):
            initial_pixel = (new_x - dx, new_y - dy)
        
        # If it's a different color
        elif img[new_y][new_x] != boundary_color:
            img[new_y][new_x] = 2
        
        else:
            # Same color, keep going
            img[new_y][new_x] = 2
            x, y = new_x, new_y
            continue

        initial_pixel = (new_x - dx, new_y - dy)
        # When we rotate directions here, the current direction will always be the 0th index
        directions = rotate_directions(directions, 0, 1)
        return img, initial_pixel, directions
        
        

def main_trace(img, img_width, img_height, directions, current_pixel, initial_pixel, boundary_color):
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
            for j, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                
                # If we go out of bounds
                if (new_x < 0 or new_x >= img_width 
                or new_y < 0 or new_y >= img_height):
                    continue
                
                # If pixel is unchecked && pixel is same color as boundary
                if (img[new_y][new_x] == 0 
                and img[new_y][new_x] == boundary_color):
                    img[new_y][new_x] = 2
                    directions = rotate_directions(directions, j, 3)
                    # Set new initial pixel and continue tracing
                    return main_trace(img, img_width, img_height, directions, (new_x, new_y), (new_x, new_y), boundary_color)
            
            # We have reached the initial pixel and there are no surrounding pixels of the same color
            return img
        
        # If pixel has already been checked
        if img[new_y][new_x] == 2:
            # Skip over the checked pixel and check for the same color
            skip_x, skip_y = new_x + dx, new_y + dy
            
            # TODO: Check if this next condition is necessary
            # It seems to never evaluate to true
            # Likely because of the "skip check" we introduced above

            # If out of bounds or not the boundary color
            if (skip_x < 0 or skip_x >= img_width 
            or skip_y < 0 or skip_y >= img_height
            or img[skip_y][skip_x] != boundary_color):
                # Check pixel in the opposite direction
                dx, dy = directions[(i + 2) % 4]
                new_x, new_y = x + dx, y + dy
                # If this pixel is out of bounds or is already checked
                if (new_x < 0 or new_x >= img_width
                or new_y < 0 or new_y >= img_height 
                or img[new_y][new_x] == 2):
                    return img
            # Else, mark it and rotate directions
            img[skip_y][skip_x] = 2
            directions = rotate_directions(directions, i, 3)
            return main_trace(img, img_width, img_height, directions, (skip_x, skip_y), initial_pixel, boundary_color)
        
        # If pixel is same color as boundary
        if img[new_y][new_x] == boundary_color:
            img[new_y][new_x] = 2
            directions = rotate_directions(directions, i, 3)
            return main_trace(img, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
        
        # Pixel is different color
        img[new_y][new_x] = 2
        continue
    
    # We have checked all directions except backwards, backtrack and continue tracing.
    new_x, new_y = x - dx, y - dy
    return main_trace(img, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
