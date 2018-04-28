//vigenere.c - encrypt the plain text using vigenere cipher and generate a ciphertext
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    //Check how many argc, if not equal to two prompt the user
    if (argc != 2)
    {
        printf("Usage: ./caesar k\n"); //prompt the user that usage is wrong
        return 1;
    }
    else
    {
        string k = argv[1];
        for (int cC = 0; cC < strlen(k); cC++) // cC stands for character Counter
        {
            if (isalpha(k[cC]) == false) // check if every character inside the 2nd argument passed is alphabets
            {
                printf("Usage: ./caesar k\n");
                return 1;
            }
            else
            {
                continue;
            }
        }
        //request the user for plaintext
        string plain_text = get_string("plaintext: ");
        //Get the first letter, apply the scrambling, and output, followed by the next
        printf("ciphertext: ");
        char cipher_text = 0;
        int kl = 0;
        for (int i = 0; i < strlen(plain_text); i++)
        {
            if (kl == strlen(k))
            {
                kl = 0;
            }
            if (isalpha(plain_text[i]) == false) // if its not an alphabet
            {
                cipher_text = (plain_text[i]);
            }
            else if (islower(plain_text[i])) // if its lower case
            {
                int kp = tolower(k[kl]) - 97;
                cipher_text = ((plain_text[i] - 97 + kp) % 26) + 97;
                kl++;
            }
            else if (isupper(plain_text[i])) // if its upper case
            {
                int kp = tolower(k[kl]) - 97;
                cipher_text = (plain_text[i] - 65 + kp) % 26 + 65;
                kl++;
            }
            printf("%c", (char) cipher_text); //print the character on screen
        }
        printf("\n");
    }
}
