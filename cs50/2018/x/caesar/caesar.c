//caesar.c - encrypt the plain text using caesar cipher and generate a ciphertext
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    //Check how many argc, if more than two prompt the user
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    else
    {
        int k = atoi(argv[1]);
        //request the user for plaintext
        string plain_text = get_string("plaintext: ");
        //Get the first letter, apply the scrambling, and output, followed by the next
        printf("ciphertext: ");
        char cipher_text = 0;
        for (int i = 0; i < strlen(plain_text); i++)
        {
            if (isalpha(plain_text[i]) == false) // if its not an alphabet
            {
                cipher_text = (plain_text[i]);
            }
            else if (islower(plain_text[i])) // if its lower case
            {
                cipher_text = ((plain_text[i] - 96 + k) % 26) + 96;
            }
            else if (isupper(plain_text[i])) // if its upper case
            {
                cipher_text = (plain_text[i] + k % 26);
            }
            printf("%c", (char) cipher_text);
        }
        printf("\n");
    }
}
