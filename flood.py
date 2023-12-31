def fill(img, mask, directions, img_height, img_width, initial_pixel, fill_color):
    def is_valid(x, y):
        return (
            # Important note, we need to check bounds
            # before trying to access it from img or mask.
            
            # Although, it would be faster
            # to check the "most likely false" conditions first.
            # ... can't do it though
            0 <= x < img_width 
            and 0 <= y < img_height
            and img[y][x] != fill_color
            and mask[y][x] != 2
        )

    # Get directions that are not bound by the screen/image
    # or, going beyond the boundary per the mask
    def is_unbound(x, y, directions):
        neighbors = [
            (x + dx, y + dy) 
            for dx, dy in directions
        ]
        return [
            i 
            for i, (dx, dy) in enumerate(neighbors) 
            if not (
                0 <= (x + dx) < img_width 
                and 0 <= (y + dy) < img_height 
                and mask[y + dy][x + dx] == 2
            )
        ]

    # Good old recursive flood fill
    def flood_fill(x, y, directions):
        if not is_valid(x, y):
            return

        img[y][x] = fill_color

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                flood_fill(nx, ny, directions)

    # This is where fill() actually starts
    x, y = initial_pixel
    for i in is_unbound(x, y, directions):
        # Move in unbound directions twice
        dx, dy = directions[i]
        x, y = x + (dx * 2), y + (dy * 2)
        flood_fill(x, y, directions)

    return img