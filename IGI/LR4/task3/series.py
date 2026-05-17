# ---------------------------------------------------------
# Lab Work №4 - Task 3 (Variant 27)
# Module: series.py
# Purpose: Arcsin series calculation
# Version: 1.0
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------

import math
from statistics import mean, median, mode, variance, stdev


class BaseSeries:
    """Abstract base class for series calculations."""

    def __init__(self, x: float, eps: float):
        """
        Initialize series calculator.

        Args:
            x (float): Argument value where |x| < 1
            eps (float): Precision (epsilon) for convergence
        """
        self.x = x
        self.eps = eps
        self.n = 0
        self.fx = 0
        self.math_fx = 0
        self.terms = []

    def calculate(self):
        """Calculate series expansion. Must be implemented by subclass."""
        raise NotImplementedError("Must implement calculate method")

    def get_results(self):
        """
        Get calculation results.

        Returns:
            tuple: (x, n, F(x), Math F(x), eps)
        """
        return self.x, self.n, self.fx, self.math_fx, self.eps


class ArcsinSeries(BaseSeries):
    """
    Calculator for computing arcsin(x) using series expansion.
    
    Formula: arcsin(x) = Σ (2n)! / (4^n * (n!)^2 * (2n+1)) * x^(2n+1)
                       = x + x^3/6 + 3x^5/40 + ...
    Valid for |x| < 1
    """
    MAX_ITERATION = 500

    def calculate(self):
        """
        Calculate arcsin(x) using series expansion with recurrence relation.
        
        Recurrence: a_(n+1) = a_n * ((2n+1)^2 * x^2) / ((2n+3)(2n+2))
        where a_n is the term for x^(2n+1)
        """
        self.math_fx = math.asin(self.x)
        
        # First term: a0 = x
        term = self.x
        self.fx = term
        self.terms = [self.fx]
        self.n = 0
        
        # If x is 0, arcsin(0) = 0, no more terms needed
        if abs(self.x) < 1e-15:
            self.n = 0
            return
        
        for n in range(0, self.MAX_ITERATION):
            # Calculate next term using recurrence
            # a_{n+1} = a_n * ((2n+1)^2 * x^2) / ((2n+3)(2n+2))
            n_current = n
            numerator = (2 * n_current + 1) ** 2 * self.x * self.x
            denominator = (2 * n_current + 3) * (2 * n_current + 2)
            
            term *= numerator / denominator
            self.fx += term
            self.terms.append(self.fx)
            self.n = n + 1
            
            if abs(term) < self.eps:
                break
    
    def get_statistics(self) -> dict:
        """
        Calculate statistical measures of series terms.

        Returns:
            dict: Contains Mean, Median, Mode, Variance, Stdev

        Raises:
            Exception: If not enough data points (< 2)
        """
        if len(self.terms) < 2:
            raise Exception(
                f"Not enough data points: {len(self.terms)} < 2. "
                f"Try smaller epsilon value (< 0.1)"
            )
        
        try:
            mode_val = mode(self.terms)
        except Exception:
            mode_val = "N/A"
        
        # Handle case when variance is zero (all terms equal)
        try:
            var_val = variance(self.terms)
        except Exception:
            var_val = 0.0
        
        try:
            stdev_val = stdev(self.terms)
        except Exception:
            stdev_val = 0.0
        
        return {
            "Mean": mean(self.terms),
            "Median": median(self.terms),
            "Mode": mode_val,
            "Variance": var_val,
            "Stdev": stdev_val,
        }