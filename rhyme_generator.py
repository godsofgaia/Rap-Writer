"""Module for generating rhymes and similar-sounding
   words using the Datamuse API."""

from concurrent.futures import ThreadPoolExecutor
from itertools import product
from functools import lru_cache
import requests
from kivy.clock import Clock

MIN_WORDS_IN_PHRASE = 2
MAX_WORDS_IN_PHRASE = 7


def fetch_rhymes(words):
    """Fetches rhymes for single or multiple words."""
    print(f"Fetching rhymes for: {words}")
    if len(words) == 1:
        result = fetch_single_word_rhymes(words[0])
    else:
        result = fetch_rhymes_for_multiple_words(words)
    print(f"Fetch rhymes result: {result}")  # Add this line
    return result


def fetch_single_word_rhymes(word):
    """Fetches single-word rhymes using the Datamuse API."""
    if not word:
        print("No word provided for fetching rhymes.")
        return []

    url = f"https://api.datamuse.com/words?rel_rhy={word}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        rhymes = [item['word'] for item in response.json()]
        print(f"Single-word rhymes for '{word}': {rhymes}")
        return rhymes
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return []


def fetch_rhymes_for_multiple_words(words):
    """Fetches rhymes for each word in the given list and combines them."""
    if len(words) < 2:
        print("Please provide at least two words for multi-word rhyme "
              "generation.")
        return []

    with ThreadPoolExecutor() as executor:
        rhymes_list = list(executor.map(fetch_single_word_rhymes, words))
    return combine_rhymes(rhymes_list)


def fetch_from_api(url, log_message):
    """Fetches data from the Datamuse API."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = [item['word'] for item in response.json()]
        print(f"{log_message}: {result}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return []


def combine_rhymes(rhymes_list):
    """Combines rhymes from each word to create multi-word rhymes."""
    if len(rhymes_list) < 2:
        print("Not enough rhymes lists to combine.")
        return {}

    combined_rhymes = {}
    for word_count in range(MIN_WORDS_IN_PHRASE, min(MAX_WORDS_IN_PHRASE, len(rhymes_list)) + 1):
        combinations = product(*rhymes_list[:word_count])
        logical_combinations = [' '.join(combo) for combo in combinations if is_logical_phrase(' '.join(combo))]
        if logical_combinations:
            combined_rhymes[word_count] = logical_combinations

    return combined_rhymes


@lru_cache(maxsize=128)
def is_logical_phrase(phrase):
    """Determines if a phrase is logical for a rhyme."""
    word_count = phrase.count(' ') + 1
    return MIN_WORDS_IN_PHRASE <= word_count <= MAX_WORDS_IN_PHRASE


def fetch_similar_sounding(word):
    """Fetches words with similar sounds using the Datamuse API."""
    if not word:
        print("No word provided for fetching similar sounds.")
        return []

    try:
        url = f"https://api.datamuse.com/words?sl={word}&max=20"
        response_similar = requests.get(url, timeout=5)
        response_similar.raise_for_status()
        similar_sounding = [item['word'] for item in response_similar.json()]
        print(f"Words that sound like '{word}': {similar_sounding}")
        return similar_sounding
    except requests.exceptions.RequestException as e:
        print(f"Request exception in fetch_similar_sounding: {e}")
        return []
