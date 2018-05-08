// recover.c - Recovers deleted JPEG files from memory card.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define BLOCK 512

int main(int argc, char *argv[])
{
    //check if user gave correct argument count
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    //opens the file
    FILE *image = fopen(argv[1], "r");
    if (image == NULL)
    {
        fprintf(stderr, "File does not exist!\n");
        return 2;
    }
    //TODO: Go through 512 bytes at a time.
    uint8_t *buffer = malloc(512);
    if (buffer == NULL)
    {
        fprintf(stderr, "Not enough space for buffer!\n");
        return 3;
    }
    int onumber = 0; //file numbers
    char *oname = malloc(8); // variable to hold file name
    while (fread(buffer, BLOCK, 1, image) == 1) //if fread returns less than elements read, that means it has reached EOF.
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) //check for JPEG file.
        {
            snprintf(oname, 8, "%03i.jpg", onumber); //print filename to a string to hold it
            //Open a new JPEG
            FILE *ofile = fopen(oname, "w"); //open a new file to put the JPEG in
            //write until new JPEG is found
            fwrite(buffer, BLOCK, 1, ofile);
            while (fread(buffer, BLOCK, 1, image) == 1)
            {
                if (buffer[0] != 0xff || buffer[1] != 0xd8 || buffer[2] != 0xff || (buffer[3] & 0xf0) != 0xe0) // either false
                {
                    fwrite(buffer, BLOCK, 1, ofile); //write to JPEG
                }
                else
                {
                    fseek(image, -BLOCK, SEEK_CUR); //fread changes location, so need to go back one block to avoid twice fread.
                    break;
                }
            }
            onumber++; //increase file number
            fclose(ofile); //closes the file
        }
    }
    fclose(image); //close input file
    free(buffer); //free memory
    free(oname); //free memory
}
