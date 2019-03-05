from cs50 import get_string
from sys import argv, exit


def main():

    # Accept dictionary of banned words
    # If no command line, quit
    if (len(argv) != 2):
        exit("Usage: " + __file__ + " dictionary")
    # Open, read and store the words into a list/set(preferable)
    dictionary = open(argv[1], "r")
    dictBuffer = set()

    c = dictionary.readline().strip()
    while c != '':
        dictBuffer.add(c)
        c = dictionary.readline().strip()

    # accept a sentence from user
    sentence = get_string("What message would you like to censor?\n")

    # Tokenize each of the words
    words = sentence.split()
    # Run check against the database
    for word in words:
        # If it matches either, print equal number of "*" on screen
        if word.lower() in dictBuffer:
            print("*" * len(word) + ' ', end='')
        # else, print back the word
        else:
            print(word + ' ', end='')

    print('\n')


if __name__ == "__main__":
    main()
