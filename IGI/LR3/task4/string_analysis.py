"""
Module: string_analysis.py
Purpose: Text analysis functions for Lab 4.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

class EmptyTextError(Exception):
    """Raised when input text is empty."""
    pass

def split_words(text: str):
    """
    Split text into words using spaces and commas as delimiters.
    No regular expressions.
    Args:
        text (str): input string
    Returns:
        list of str: words
    """
    # Replace commas with spaces, then split by whitespace
    # Also handle multiple spaces
    cleaned = text.replace(',', ' ')
    words = cleaned.split()
    return words

def count_words(words: list) -> int:
    """Return number of words."""
    return len(words)

def find_longest_word(words: list):
    """
    Find the longest word and its 1-based index.
    Args:
        words (list): list of words
    Returns:
        tuple: (longest_word, index) or (None, None) if empty
    """
    if not words:
        return None, None
    longest = ""
    idx = 0
    for i, w in enumerate(words, start=1):
        if len(w) > len(longest):
            longest = w
            idx = i
    return longest, idx

def get_odd_words(words: list) -> list:
    """Return words at odd positions (1-based: 1,3,5...)."""
    return [w for i, w in enumerate(words) if i % 2 == 0]  # i=0 -> position 1 (odd)