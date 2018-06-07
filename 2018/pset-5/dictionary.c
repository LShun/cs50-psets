// Implements a dictionary's functionality

#include "dictionary.h"

typedef struct node
{
    bool isWord; //indicating if its the last character of word
    struct node *letter[27]; //pointer to nodes, 26 letters A-Z + Apostrophe
}
node;

//prototypes
void reunload(node *pointer);

node *root;
unsigned int wordCount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *ptr = root;
    for (int i = 0; word[i] != '\0'; i++) //for each letter
    {
        int wordVal = ((tolower(word[i]) != 39) ? (tolower(word[i]) - 97) : 26); //check if its a letter or an apostrophe
        if (ptr->letter[wordVal] != NULL) //if the letter exists in dict
        {
            ptr = ptr->letter[wordVal]; //move the pointer into the array pointed by the letter in the current array.
        }
        else //if letter of word doesn't exist in dict
        {
            return false;
        }
    }
    if (ptr->isWord == true) //if its a word in dict
    {
        return true; //return
    }
    else // if its not a word
    {
        return false;
    }

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    char *word = malloc(LENGTH + 2  * sizeof(char));
    root = calloc(1, sizeof(node));
    node *ptr = root;
    if (word == NULL)
    {
        fprintf(stderr, "Cannot allocate memory!");
        return false;
    }
    while (fgets(word, LENGTH + 2, dict) != NULL) //get a string from dict until it hits a \n, and place it into word
    {
        word[strcspn(word, "\n")] = 0; //removes trailing '\n' if have << problem
        ptr = root; // a pointer to point at the root directory
        for (int i = 0; word[i] != '\0'; i++)
        {
            int wordVal = 0;
            wordVal = (word[i] != 39 ? word[i] - 97 : 26);
            if (ptr->letter[wordVal] == NULL) // if the word's ith letter is not found in the letter array
            {
                node *child = calloc(1, sizeof(node)); //create a new child node
                ptr->letter[wordVal] = child; //link the wordVal-th entry in the letter array to the child node
                ptr = ptr->letter[wordVal]; // traverse the pointer into the child node
            }
            else
            {
                ptr = ptr->letter[wordVal]; // move the pointer to that letter's array
            }
        }
        ptr->isWord = true; //indicate this node is the last character of a word
        wordCount++;
    }

    fclose(dict);
    free(word);
    return true; //success
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *tra = root;
    if (tra != NULL)
    {
        reunload(tra);
    }
    else
    {
        return false;
    }
    return true;
}

void reunload(node *pointer)
{
    for (int i = 0; i < 27; i++) //for each alphabet
    {
        if (pointer->letter[i] != NULL) //if alphabet uses memory
        {
            reunload(pointer->letter[i]);
        }
    }
    free(pointer); //free the current alphabet
    return;
}