# caesar.py - encrypt the plain text using caesar cipher and generate a ciphertext

import sys
from cs50 import get_string

if (len(sys.argv) != 2):
    exit("Usage: python " + __file__ + " key.")

# get the key
key = int(sys.argv[1])

# get the plain text
plaintext = get_string("plaintext:  ")

# encipher the text
print("ciphertext: ", end="")
for ch in plaintext:
    if (ord(ch) >= ord('a')):
        print(chr((ord(ch) - ord('a') + key) % 26 + ord('a')), end="")
    elif (ord(ch) >= ord('A')):
        print(chr((ord(ch) - ord('A') + key) % 26 + ord('A')), end="")
    else:
        print(ch, end="")
print()