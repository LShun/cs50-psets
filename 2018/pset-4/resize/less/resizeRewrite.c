// Resizes a BMP file using a factor of n using the "rewrite" method

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4 || atoi(argv[1]) > 100)
    {
        fprintf(stderr, "Usage: ./resizeRewrite n(<=100) infile outfile\n");
        return 1;
    }

    // remember the scale factor
    int n = atoi(argv[1]);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding_resized = (4 - (bi.biWidth * n * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biWidth *= n;
    bi.biHeight *= n;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding_resized) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight / n); i < biHeight; i++)
    {
        int k = 0; //k is placed outside of the pixel increment so that it will not get reset before the line ends.
        RGBTRIPLE buffer[bi.biWidth]; //                                 <<either one of these two
        //RGBTRIPLE *buffer = calloc(bi.biWidth, sizeof(RGBTRIPLE)); //  <<remember to comment out the other
        // iterate over pixels in scanline
        for (int j = 0; j < abs(bi.biWidth / n); j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr); // read RGB triple from infile
            for (int l = 0; l < n; l++)
            {
                buffer[k] = triple; //write from triple, the RGBTRIPLE value into the buffer array
                k++; //increment k so that it does not overwrite the old array
            }
        }
        // for n times
        for (int w = 0; w < n; w++) 
            {
                //write from buffer to the pointer
                fwrite(buffer, sizeof(RGBTRIPLE), bi.biWidth, outptr);
                for (int a = 0; a < padding_resized; a++)
                {
                    fputc(0x00, outptr); //write padding
                }
            }
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
        k = 0;
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
