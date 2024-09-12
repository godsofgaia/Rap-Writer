import re
import string

def format_output(text):
    """Utility function to format text output."""
    return ' '.join(text.split())

def validate_input(input_text):
    """Utility function to validate user input."""
    # Basic validation: input should not be empty and should contain valid characters
    return bool(input_text and input_text.strip())

def count_words(text):
    """Counts the number of words in the given text."""
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_lines(text):
    """Counts the number of non-empty lines in the given text."""
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return len(non_empty_lines)

def split_lines(text):
    """Splits text into lines and removes trailing whitespace from each line."""
    return [line.strip() for line in text.split('\n')]

def remove_punctuation(text):
    """Removes punctuation from the text."""
    return text.translate(str.maketrans('', '', string.punctuation))

def calculate_average_word_length(text):
    """Calculates the average word length in the given text."""
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

def calculate_readability_score(text):
    """Calculates a simple readability score based on word and sentence length."""
    words = count_words(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    if sentences == 0:
        sentences = 1  # To avoid division by zero if no sentences are found
    return words / sentences