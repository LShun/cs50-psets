# Questions

## What's `stdint.h`?

stdint.h is a header file in the C standard library introduced in the C99 standard library section 7.18 that allow programmers to write more portable code by providing a set of typedefs that specify exact-width integer types, together with the defined minimum and maximum allowable values for each type, using macros.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

To define the minimum and maximum values allowed for each type of value.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

'BYTE' contains 1 byte.
'DWORD' contains 4 bytes.
'LONG' contains 4 bytes.
'WORD' contains 2 bytes.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

( In ASCII ) BM

## What's the difference between `bfSize` and `biSize`?

bfSize stores the size of the bitmap file while biSize stores the size required by the structure portion of the bitmap file.

## What does it mean if `biHeight` is negative?

Indicates a top-down DIB file, the stride is negative ( going down ) and it cannot be compressed.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

There is not enough space for the memory or the directory is invalid.

## Why is the third argument to `fread` always `1` in our code?

Because we only want to read 1 struct one time into the memory, so we only need '1' in 'fread'.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

Change the seeking location of the pointer in the file.

## What is `SEEK_CUR`?

Set the offset to be based on the current pointer location.
