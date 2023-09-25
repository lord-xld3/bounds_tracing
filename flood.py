def fill(img, initial_pixel, fill_color):
    x, y = initial_pixel

    def move(x, y):
        if x < 0 or x >= len(img[0]) or y < 0 or y >= len(img):
            return

        # If the current pixel is not the same color as the initial pixel, return the new initial pixel
        if img[y][x] != fill_color:
            return x, y

        # Recursively move in all four directions
        new_pixel = move(x + 1, y)  # Right
        if new_pixel:
            return new_pixel
        new_pixel = move(x - 1, y)  # Left
        if new_pixel:
            return new_pixel
        new_pixel = move(x, y + 1)  # Down
        if new_pixel:
            return new_pixel
        new_pixel = move(x, y - 1)  # Up
        return new_pixel

    def recur(x, y):
        if x < 0 or x >= len(img[0]) or y < 0 or y >= len(img):
            return

        # If the current pixel is not the same color as the initial pixel, return
        if img[y][x] != fill_color:
            return

        # Fill the current cell
        img[y][x] = fill_color

        # Recursively fill adjacent cells in all four directions
        recur(x + 1, y)  # Right
        recur(x - 1, y)  # Left
        recur(x, y + 1)  # Down
        recur(x, y - 1)  # Up

    # Start by moving until you hit a different color or border
    new_pixel = move(x, y)

    # If all surrounding pixels have the same color, new_pixel will be None
    if new_pixel is None:
        return img

    # Otherwise, start the recursive fill from the new initial pixel
    recur(new_pixel[0], new_pixel[1])
    return img
