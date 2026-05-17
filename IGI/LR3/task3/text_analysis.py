"""
Module: text_analysis.py
Purpose: Text analysis functions for Lab 3.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

class EmptyStringError(Exception):
    """Raised when input string is empty."""
    pass

def count_lowercase_words(text: str) -> int:
    """
    Count words that start with a lowercase letter.
    Words are separated by whitespace. Non-letter first characters are ignored.

    Args:
        text (str): input string

    Returns:
        int: number of words starting with lowercase letter

    Raises:
        EmptyStringError: if text is empty or only whitespace
    """
    if not text or text.isspace():
        raise EmptyStringError("Input string is empty or contains only whitespace.")

    words = text.split()
    count = 0
    for word in words:
        if word and word[0].islower():
            # Ensure first character is a letter (islower() returns False for non-letters)
            # But we want only letters. Actually islower() for non-letter returns False, so it's fine.
            count += 1
    return count