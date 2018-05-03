# Resize - Less Version

**Guide**

This is the problem set involving resizing an image. The user first make the file executable in CS50 IDE using

`make e`

where `e` is the c file name ( such as `resizeRecopy` ) of the executable ( not .c file ) then runs the program using the command-line: 

`./e n infile outfile`

where `n` is the scale factor, which has to be less than 100. `infile` is the input file and `outfile` is the output file to scale the image.

**Versions**

There are two versions that I make to experiment with pointers and dynamic memory allocation.

1. **resizeRecopy.c** - resizes the image horizontally by first writing `n` times pixel in the first line of the `infile` to the `outfile`. Then, it resizes the image vertically by moving back the pointer `(n-1)` times to the start of the line and repeatedly writing them before moving to the next line.

2. **resizeRewrite.c** - resizes the image horizontally by first writing `n` times pixel in the first line of the `infile` to the `buffer`. Then resizes the image vertically by writing `n` times `buffer` into the `outfile`.

