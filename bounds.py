# Before entering main tracing loop,
# We need to check if we're in the center of the shape.
# If we are, travel to the edge of the shape and set that as the initial pixel.
def init_trace(img, img_width, img_height, directions, initial_pixel, boundary_color):
    x, y = initial_pixel  # Extract x and y coordinates
    
    # Check pixels in all directions
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates
        
        # Check if the pixel is out of bounds
        if new_x < 0 or new_x >= img_width or new_y < 0 or new_y >= img_height:
            continue
        
        # Check if the pixel is a different color than the initial pixel
        if img[new_y][new_x] != boundary_color:
            img[new_y][new_x] = 2 # 2 indicates that the pixel has been checked
            # Set previous pixel as the initial pixel and rotate the opposite direction to the second position
            initial_pixel = (new_x - dx, new_y - dy)
            d = (i + 2) % 4
            directions = directions[d:] + directions[:d]
            return img, initial_pixel, directions
        
        # Mark pixel as checked
        img[new_y][new_x] = 2
    
    # If we finish the for loop, it means the initial pixel is surrounded by the same color
    # Continue in the current direction
    img[y][x] = 2
    dx, dy = directions[0]
    x, y = x + dx, y + dy # Move over once, since its already been checked
    while True:
        new_x, new_y = x + dx, y + dy  # Calculate new coordinates

        # If we go out of bounds
        if new_x < 0 or new_x >= img_width or new_y < 0 or new_y >= img_height:
            initial_pixel = (new_x - dx, new_y - dy)
            d = (i + 2) % 4
            directions = directions[d:] + directions[:d]
            return img, initial_pixel, directions
        
        # If it's a different color
        if img[new_y][new_x] != boundary_color:
            img[new_y][new_x] = 2
            initial_pixel = (new_x - dx, new_y - dy)
            d = (i + 2) % 4
            directions = directions[d:] + directions[:d]
            return img, initial_pixel, directions
        
        # Same color, keep going
        img[new_y][new_x] = 2
        x, y = new_x, new_y

def main_trace(img, img_width, img_height, directions, current_pixel, initial_pixel, boundary_color):
    x, y = current_pixel  # Extract x and y coordinates
    
    for i, (dx, dy) in enumerate(directions):
        new_x, new_y = x + dx, y + dy
        
        # If we go out of bounds
        if new_x < 0 or new_x >= img_width or new_y < 0 or new_y >= img_height:
            continue
        
        # If pixel is initial pixel
        if (new_x, new_y) == initial_pixel:
            # Check surrounding pixels
            for j, (dx, dy) in enumerate(directions):
                new_x, new_y = x + dx, y + dy
                
                # If we go out of bounds
                if new_x < 0 or new_x >= img_width or new_y < 0 or new_y >= img_height:
                    continue
                
                # If pixel is unchecked && pixel is same color as boundary
                if img[new_y][new_x] == 0 and img[new_y][new_x] == boundary_color:
                    img[new_y][new_x] = 2
                    # Rotate the current direction to the second position
                    d = (j + 3) % 4
                    directions = directions[d:] + directions[:d]
                    # Set new initial pixel and continue tracing
                    return main_trace(img, img_width, img_height, directions, (new_x, new_y), (new_x, new_y), boundary_color)
            
            # We have reached the initial pixel and there are no surrounding pixels of the same color
            return img
        
        # If pixel has already been checked
        if img[new_y][new_x] == 2:
            # Skip over the checked pixel and check for the same color
            skip_x, skip_y = new_x + dx, new_y + dy
            if img[skip_y][skip_x] == boundary_color:
                img[skip_y][skip_x] = 2
                # Rotate current direction to second position
                d = (i + 3) % 4
                directions = directions[d:] + directions[:d]
                # Set new current pixel and continue tracing
                return main_trace(img, img_width, img_height, directions, (skip_x, skip_y), initial_pixel, boundary_color)
                
            # Check pixel in the opposite direction
            dx, dy = directions[(i + 2) % 4]
            new_x, new_y = x + dx, y + dy
            # If this pixel is out of bounds or is already checked
            if new_x < 0 or new_x >= img_width or new_y < 0 or new_y >= img_height or img[new_y][new_x] == 2:
                return img
            # Move to this pixel and rotate current direction to second position
            img[new_y][new_x] = 2
            d = (i + 3) % 4
            directions = directions[d:] + directions[:d]
            # Set new current pixel and continue tracing
            return main_trace(img, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
        
        # If pixel is same color as boundary
        if img[new_y][new_x] == boundary_color:
            img[new_y][new_x] = 2
            # Rotate current direction to second position
            d = (i + 3) % 4
            directions = directions[d:] + directions[:d]
            # Set new current pixel and continue tracing
            return main_trace(img, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)
        
        else:
            # Pixel is different color
            img[new_y][new_x] = 2
            continue
    
    # We have checked all directions except backwards.
    new_x, new_y = x - dx, y - dy
    return main_trace(img, img_width, img_height, directions, (new_x, new_y), initial_pixel, boundary_color)