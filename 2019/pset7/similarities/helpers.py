from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    match = set()
    # when reach a newline character

    #   split the strings
    setA = set(a.split('\n'))
    setB = set(b.split('\n'))

    #   test it with another string
    for line in setA:
        if line in setB:
            match.add(line)
    return list(match)


def sentences(a, b):
    """Return sentences in both a and b"""
    # TODO
    setA = sent_tokenize(a, language='english')
    setB = sent_tokenize(b, language='english')
    # check each sentence in a if its found in b
    match = []
    for sentence in setA:
        if sentence in setB and sentence not in match:
            match.append(sentence)
    return match


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    subA = set()
    subB = set()
    match = set()

    # strip all newline character
    a = a.rstrip()
    b = b.rstrip()

    # Extract substrings from string - an extra function
    for i in range(len(a)):
        substring = a[i:i+n]
        if len(substring) < n:
            break
        subA.add(substring)
    for i in range(len(b)):
        substring = b[i:i+n]
        if len(substring) < n:
            break
        subB.add(substring)

    for substring in subA:
        if substring in subB:
            match.add(substring)

    return list(match)

