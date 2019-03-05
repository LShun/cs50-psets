from cs50 import get_int

# prints mario blocks

while(True):
    # ask for half-pyramid's height
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# if it is within the range, print the pyramid
for row in range(height):
    print(" " * (height-row-1), end="")
    print("#" * (row+1), end="")
    print("")