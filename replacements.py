import random

vocals = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'


def convert(string):
    list1 = []
    list1[:0] = string
    return list1


def shuffle(string):
    orig = convert(string)
    new = random.sample(orig, len(orig))
    return new


def permute(txt, letters, new_letters, nb_of_permutations=1):
    for i in range(nb_of_permutations):
        transTable = txt.maketrans(f"{letters[i]}{new_letters[i]}", f"{new_letters[i]}{letters[i]}", "")
        txt = txt.translate(transTable)
    return txt
