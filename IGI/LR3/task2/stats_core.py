"""
Module: stats_core.py
Purpose: Core statistics functions for Lab 2.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

class NoEvenNumbersError(Exception):
    """Raised when no even numbers are present in the list."""
    pass

def average_even(numbers):
    """
    Calculate arithmetic mean of even numbers in a list.

    Args:
        numbers (list of int): list of integers

    Returns:
        float: average of even numbers

    Raises:
        NoEvenNumbersError: if no even numbers found
        TypeError: if list contains non-integer
    """
    evens = [n for n in numbers if n % 2 == 0]
    if not evens:
        raise NoEvenNumbersError("No even numbers provided.")
    return sum(evens) / len(evens)