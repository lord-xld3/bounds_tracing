def get_color(
    img: list[list[int]], 
    pixel: tuple[int,int]
):
    x, y = pixel
    return img[y][x]

def in_bounds(
    pixel: tuple[int,int],
    img_width: int,
    img_height: int
):
    x, y = pixel
    return 0 <= x < img_width and 0 <= y < img_height

def rotate_directions(
    directions: list[tuple[int,int]],
    index: int,
    shifts: int,
):
    slice = (index + shifts) % len(directions)
    return directions[slice:] + directions[:slice]

# Initialize tracing by finding the nearest boundary
def init_trace(
    img: list[list[int]],
    mask: list[list[int]],
    img_height: int,
    img_width: int,
    pixel: tuple[int,int],
    shape_color: int,
    directions: list[tuple[int,int]]
):
    x, y = pixel

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if in_bounds(
            (new_x, new_y),
            img_width, img_height
        ):
            color = get_color(img, (new_x, new_y))
            
            if color == shape_color:
                mask[new_y][new_x] = color
                new_x, new_y = x + dx, y + dy
                while in_bounds(
                    (new_x, new_y),
                    img_width, img_height
                ):
                    color = get_color(img, (new_x, new_y))
                
                    if color != shape_color:
                        new_x, new_y = new_x - dx, new_y - dy
                        mask = main_trace(
                            img, mask,
                            img_height, img_width,
                            (new_x, new_y), shape_color,
                            directions
                        )
                    
                    mask[new_y][new_x] = color
                    new_x, new_y = new_x + dx, new_y + dy

    # All directions are the same color up to the img bounds
    # TODO: Trace borders of the img
    print("ERROR: All directions are the same color up to the img bounds")
    return mask

# Recursively trace the boundary of the shape
def main_trace(
    img: list[list[int]],
    mask: list[list[int]],
    img_height: int,
    img_width: int,
    pixel: tuple[int,int],
    shape_color: int,
    directions: list[tuple[int,int]]
):
    x, y = pixel
    
    if in_bounds(
        (x, y), 
        img_width, img_height
    ):
        # Check if the pixel hasn't been visited
        if mask[y][x] == 0:
            color = get_color(img, pixel)
            mask[y][x] = color
            
            if color == shape_color:
                neighbors: list[tuple[int, int]] = []
                valid_pixels: list[tuple[int, int]] = []

                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if in_bounds(
                        (new_x, new_y),
                        img_width, img_height
                    ):
                        color = get_color(img, (new_x, new_y))
                        
                        if color == shape_color:
                            neighbors.append((new_x, new_y))
                            
                            if mask[new_y][new_x] == 0:
                                valid_pixels.append((new_x, new_y))
                        
                        else:
                            mask[new_y][new_x] = color

                # If surrounded by 4 neighbors, stop recursion    
                if len(neighbors) == 4:
                    for dx, dy in directions:
                        new_x, new_y = x + dx, y + dy
                        mask[new_y][new_x] = shape_color
                    return mask
                
                # For each valid neighbor continue recursion
                for px in valid_pixels:
                    mask = trace(
                        img, mask,
                        img_height, img_width, 
                        px, shape_color
                    )
                    
    return mask

def trace(
    img: list[list[int]],
    mask: list[list[int]],
    img_height: int,
    img_width: int,
    pixel: tuple[int,int],
    shape_color: int
):
    # Right, Down, Left, Up
    # To traverse "down" in the image, we need to increment the y coordinate
    directions: list[tuple[int,int]] = [(1,0),(0,1),(-1,0),(0,-1)]
    mask = init_trace(
        img, mask,
        img_height, img_width,
        pixel, shape_color, directions
    )
    return mask