"""
Module for highlighting rhymes in the lyrics input.
"""

import re


def highlight_rhymes(text, rhyme_groups):
    """Highlights rhymes in the lyrics input."""
    word_pattern = re.compile(r'\W+')
    color_codes = {1: "ff0000", 2: "00ff00",
                   3: "0000ff", 4: "ffff00", 5: "ff00ff"}
    highlighted_text_parts = []
    words = text.split()

    for word in words:
        clean_word = word_pattern.sub('', word).lower()
        # Remove punctuation and convert to lowercase for matching
        if clean_word in rhyme_groups:
            color_code = color_codes.get(rhyme_groups
                                         [clean_word] % 5 + 1, "000000")
            highlighted_text_parts.append(
                f"[color={color_code}]{word}[/color]")
        else:
            highlighted_text_parts.append(word)

    return ' '.join(highlighted_text_parts)
