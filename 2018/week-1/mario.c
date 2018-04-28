#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h, s;
    do
    {
        h = get_int("Height: "); //asks the user for the pyramid height.
    }
    while (h < 0 || h > 23);
    //Loop through the number of rows of pyramid based on h
    for (int i = 0; i < h; i++)
    {
        //For 'x' row, print out 'h-x' spaces followed by 'x' hashes.
        for (s = 1; s < h - i; s++)
        {
            printf(" ");
        }
        printf("#");
        for (int hash = 0; hash <= h - s; hash++)
        {
            printf("#");
        }
        //At the end, print a new line.
        printf("\n");
    }
}