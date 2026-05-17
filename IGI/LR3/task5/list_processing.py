"""
Module: list_processing.py
Purpose: Core functions for list processing (sum of negatives, product between min and max).
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

class EmptyListError(Exception):
    """Raised when list is empty."""
    pass

class SingleElementError(Exception):
    """Raised when list has only one element (no interval between min and max)."""
    pass

def sum_negative(numbers):
    """
    Calculate sum of negative numbers in the list.

    Args:
        numbers (list of float): input list

    Returns:
        float: sum of negative elements (0 if none)
    """
    return sum(x for x in numbers if x < 0)

def find_min_max_indices(numbers):
    """
    Find indices of minimum and maximum elements.
    If multiple occurrences, returns first occurrences.

    Args:
        numbers (list of float): input list

    Returns:
        tuple: (index_of_min, index_of_max)
    """
    if not numbers:
        raise EmptyListError("Cannot find indices in empty list.")
    min_idx = 0
    max_idx = 0
    for i, val in enumerate(numbers):
        if val < numbers[min_idx]:
            min_idx = i
        if val > numbers[max_idx]:
            max_idx = i
    return min_idx, max_idx

def product_between_min_max(numbers):
    """
    Calculate product of elements between min and max (exclusive).

    Args:
        numbers (list of float): input list

    Returns:
        float: product (1 if no elements in between)

    Raises:
        EmptyListError: if list is empty
        SingleElementError: if list has only one element (no min/max pair)
    """
    if len(numbers) < 2:
        raise SingleElementError("List must have at least 2 elements to define an interval.")

    min_idx, max_idx = find_min_max_indices(numbers)
    start = min(min_idx, max_idx) + 1
    end = max(min_idx, max_idx)

    if start >= end:
        return 1.0  # no elements between

    product = 1.0
    for i in range(start, end):
        product *= numbers[i]
    return product