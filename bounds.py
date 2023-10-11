def trace(
    img: list[list[int]],
    mask: list[list[int]],
    img_height: int,
    img_width: int,
    pixel: tuple[int,int],
    shape_color: int
) -> list[list[int]]:
    """
    Trace the boundary of a shape in the image.

    Parameters:
        img: Image matrix.
        mask: Mask to mark visited pixels.
        img_height: Image height.
        img_width: Image width.
        pixel: Starting pixel coordinates.
        shape_color: Color of the shape to trace.

    Returns:
        The updated mask with the traced boundary.
    """

    # Right, Down, Left, Up
    # To traverse "down" in the image, we need to increment the y coordinate
    directions: list[tuple[int,int]] = [(1,0),(0,1),(-1,0),(0,-1)]

    def get_color(
        pixel: tuple[int,int]
    ) -> int:
        """
        Return the color of the given pixel from the image.
        """
        x, y = pixel
        return img[y][x]
    
    def in_bounds(
        pixel: tuple[int,int],
    ) -> bool:
        """
        Return True if the pixel is in bounds of the image.
        """
        x, y = pixel
        return 0 <= x < img_width and 0 <= y < img_height
        
    
    def rotate_directions(
        index: int,
        shifts: int,
    ) -> list[tuple[int,int]]:
        """
        Rotate the directions list based on the given index and shifts. Moves index to a certain position.

        Parameters:
            index: Index of the current direction.
            shifts: Number of shifts to rotate by. Positive = clockwise, Negative = counter-clockwise.

        Returns:
            directions: The rotated directions list.
        """
        slice = (index + shifts) % len(directions)
        return directions[slice:] + directions[:slice]
    
    def init_trace() -> list[list[int]]:
        """
        Handles the case where the initial pixel is surrounded by the same color, or in other words, its not next to the boundary.
        
        Moves in one direction until it reaches a boundary and starts tracing from there.

        Returns:
            mask: The updated mask with the traced boundary.
        """
        nonlocal mask
        x, y = pixel
        # Check every pixel around initial pixel
        for index, (dx, dy) in enumerate(directions):
            new_x, new_y = x + dx, y + dy
            while (
                in_bounds((new_x, new_y))
                and get_color((new_x, new_y)) == shape_color
            ):
                mask[new_y][new_x] = shape_color
                new_x, new_y = x + dx, y + dy
            
            # If the pixel is out of bounds or a different color, 
            # Set previous pixel as the starting pixel and rotate directions
            new_x, new_y = new_x - dx, new_y - dy
            current_directions = rotate_directions(index, 1)
            mask = main_trace((new_x, new_y), current_directions)
            return mask
        print("ERROR: All surrounding pixels are out of bounds OR different color")
        return mask

    def main_trace(
        pixel: tuple[int,int],
        current_directions: list[tuple[int,int]]
    ) -> list[list[int]]:
        """
        Main boundary tracing function.

        Parameters:
            pixel: x, y coordinates.
            current_directions: List of directions to move in.
        
        Returns:
            mask: The updated mask with the traced boundary.
        """
        nonlocal mask
        x, y = pixel
        for index, (dx, dy) in enumerate(current_directions):
            new_x, new_y = x + dx, y + dy
            if in_bounds((new_x, new_y)):
                if mask[new_y][new_x] == 0:
                    if get_color((new_x, new_y)) == shape_color:
                        mask[new_y][new_x] = shape_color
                        # Rotate counter-clockwise
                        current_directions = rotate_directions(index, -1)
                        mask = main_trace((new_x, new_y), current_directions)
                    
                    else: # Pixel is a different color
                        mask[new_y][new_x] = 2
                
                else: # Pixel is already visited
                    # Is this pixel part of set of pixels checked in init_trace()?
                    # If so, skip over it
                    # TODO
                    pass

        return mask

    mask = init_trace()
    return mask