"""
Module for counting syllables in words and lines using Pyphen.
"""

import pyphen

pyphen_dic = pyphen.Pyphen(lang='en')


def count_syllables(word):
    """Returns the syllable count of a word using Pyphen."""
    word = word.lower()
    syllables = pyphen_dic.inserted(word).split('-')
    return len(syllables)


def count_syllables_in_line(line):
    """Returns the total syllable count of a line."""
    line = line.lower()
    syllables = pyphen_dic.inserted(line).split('-')
    return len(syllables)
