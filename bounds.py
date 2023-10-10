def get_color(img: list[list[int]], pixel: tuple[int,int]):
    x, y = pixel
    return img[y][x]

def in_bounds(x: int, y: int, img_width: int, img_height: int):
    return 0 <= x < img_width and 0 <= y < img_height

def trace(img: list[list[int]], mask: list[list[int]], img_height: int, img_width: int, pixel: tuple[int,int], shape_color: int):
    x, y = pixel

    # Check if the current pixel is within bounds
    if in_bounds(x, y, img_width, img_height):
        # Check if the pixel hasn't been visited
        if mask[y][x] == 0:
            
            # Get the color of the pixel
            color = get_color(img, pixel)

            # Check if the pixel is part of the shape
            if color == shape_color:
                # Mark the pixel as visited
                mask[y][x] = shape_color

                directions = [
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]

                neighbors = []

                # Check each direction
                for dx, dy in directions:
                    # Check if the neighbor is in bounds and unvisited
                    if in_bounds(dx, dy, img_width, img_height) and mask[dy][dx] == 0:
                        # Get the color of the neighbor
                        neighbor_color = get_color(img, (dx, dy))

                        # Check if the neighbor is part of the shape
                        if neighbor_color == shape_color:
                            neighbors.append((dx, dy))

                # If surrounded by 4 neighbors, stop recursion    
                if len(neighbors) == 4:
                    return mask
                
                # For each valid neighbor continue recursion
                for neighbor in neighbors:
                    mask = trace(img, mask, img_height, img_width, neighbor, shape_color)

    return mask

                