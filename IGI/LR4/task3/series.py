# ---------------------------------------------------------
# Lab Work №4 - Task 3 (Variant 9)
# Module: series.py
# Purpose: Arccos series calculation
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import math
from statistics import mean, median, mode, variance, stdev


class BaseSeries:
    """Abstract base class for series calculations."""

    def __init__(self, x: float, eps: float):
        """
        Initialize series calculator.

        Args:
            x (float): Argument value where |x| ≤ 1
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


class ArccosSeries(BaseSeries):
    """
    Calculator for computing arccos(x) using series expansion.
    """
    MAX_ITERATION = 500

    def calculate(self):
        """
        Calculate arccos(x) using series expansion with recurrence relation.

        Uses: a_n = a_(n-1) * (2n)(2n-1) / (4n^2) * x^2
        """
        self.math_fx = math.acos(self.x)

        self.fx = math.pi / 2
        self.terms = [self.fx]
        self.n = 0

        x_squared = self.x * self.x

        term = self.x
        self.fx -= term
        self.terms.append(self.fx)

        for n in range(1, self.MAX_ITERATION):

            coeff = (2 * n) * (2 * n - 1) / (4 * n * n)
            term *= coeff * x_squared

            self.fx -= term
            self.terms.append(self.fx)
            self.n = n

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

        return {
            "Mean": mean(self.terms),
            "Median": median(self.terms),
            "Mode": mode_val,
            "Variance": variance(self.terms),
            "Stdev": stdev(self.terms),
        }
