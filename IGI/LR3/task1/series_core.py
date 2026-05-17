"""
Module: series_core.py
Purpose: Core mathematical functions for series expansion.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

import math

class MaxIterError(Exception):
    """Raised when required accuracy is not reached within max_iter terms."""
    pass

def compute_series(x: float, eps: float, max_iter: int = 500):
    """
    Compute ln((x+1)/(x-1)) using series:
        2 * sum_{n=0}^{∞} 1 / ((2n+1) * x^{2n+1})

    Args:
        x (float): argument, must satisfy |x| > 1
        eps (float): required absolute accuracy (positive)
        max_iter (int): maximum number of terms to sum

    Returns:
        tuple: (series_sum, number_of_terms_used)

    Raises:
        ValueError: if |x| <= 1
        MaxIterError: if accuracy not reached within max_iter terms
    """
    if abs(x) <= 1:
        raise ValueError("|x| must be > 1 for convergence")

    total = 0.0
    n = 0
    while n < max_iter:
        # term = 2 / ((2n+1) * x^(2n+1))
        term = 2.0 / ((2 * n + 1) * (x ** (2 * n + 1)))
        total += term
        if abs(term) < eps:
            return total, n + 1
        n += 1
    raise MaxIterError(f"Accuracy {eps} not reached after {max_iter} terms")

def math_value(x: float) -> float:
    """Reference value using math.log."""
    return math.log((x + 1) / (x - 1))