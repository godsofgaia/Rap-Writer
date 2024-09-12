"""
Module for detecting rhymes in text and categorizing them by rhyme type.
"""

import re
from collections import defaultdict


def detect_rhymes(text):
    """Detects rhymes in the text and categorizes them by rhyme type."""
    words = re.findall(r'\b\w+\b', text.lower())
    rhyme_groups = {}
    suffix_dict = defaultdict(list)
    group_index = 1

    # Group words by their last two and three characters
    for word in words:
        if len(word) >= 2:
            suffix_dict[word[-2:]].append(word)
        if len(word) >= 3:
            suffix_dict[word[-3:]].append(word)

    # Assign group indices based on suffix groups
    for group in suffix_dict.values():
        for word in group:
            if word not in rhyme_groups:
                rhyme_groups[word] = group_index
                group_index += 1

    return rhyme_groups
