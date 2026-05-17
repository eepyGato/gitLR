# ---------------------------------------------------------
# Lab Work №4 - Task 5 (Variant 9)
# Module: matrix_creator.py
# Purpose: Matrix creation and statistical operations
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import numpy as np
from abc import ABC, abstractmethod


class MatrixBase(ABC):
    """Abstract base class for matrix operations."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.matrix = None

    @abstractmethod
    def generate_matrix(self):
        """Generate a matrix."""
        pass

    def get_matrix(self):
        """Return the matrix."""
        return self.matrix


class MatrixCreator(MatrixBase):
    """Creates integer matrix using random values."""

    def generate_matrix(self):
        """Generate random integer matrix [-100, 100]."""
        self.matrix = np.random.randint(-100, 101, (self.rows, self.cols))

    def get_first_column(self):
        """Get first column."""
        return self.matrix[:, 0]

    def get_last_column(self):
        """Get last column."""
        return self.matrix[:, -1]

    def find_max_in_first_col(self):
        """Find max element and index in first column."""
        col = self.get_first_column()
        max_val = col.max()
        max_idx = np.argmax(col)
        return max_val, max_idx

    def find_max_in_last_col(self):
        """Find max element and index in last column."""
        col = self.get_last_column()
        max_val = col.max()
        max_idx = np.argmax(col)
        return max_val, max_idx

    def swap_max_elements(self):
        """Swap maximum elements in first and last columns."""
        max_first, idx_first = self.find_max_in_first_col()
        max_last, idx_last = self.find_max_in_last_col()

        self.matrix[idx_first, 0] = max_last
        self.matrix[idx_last, -1] = max_first

        return (max_first, idx_first), (max_last, idx_last)

    def find_min_elements(self):
        """Return min value and its indices."""
        min_val = self.matrix.min()
        indices = np.argwhere(self.matrix == min_val)
        return min_val, indices


class MatrixAnalyzer:
    """Performs statistical operations on matrix."""

    def __init__(self, matrix):
        self.matrix = matrix

    def mean(self):
        """Mean = sum(elements) / count"""
        return np.mean(self.matrix)

    def median(self):
        """Median = middle value when sorted"""
        return np.median(self.matrix)

    def variance(self):
        """Variance = mean((x - mean)^2)"""
        return np.var(self.matrix)

    def std_builtin(self):
        """Std = sqrt(variance) using NumPy"""
        return round(np.std(self.matrix), 4)

    def std_manual(self):
        """Std = sqrt(variance) manual calculation"""
        mean_val = np.mean(self.matrix)
        variance = np.mean((self.matrix - mean_val) ** 2)
        return round(np.sqrt(variance), 4)

    @staticmethod
    def correlation_columns(col1, col2):
        """Calculate correlation coefficient between two columns.

        Returns value rounded to 2 decimal places.
        """
        stacked = np.vstack([col1, col2])
        corr_matrix = np.corrcoef(stacked)
        corr_coef = corr_matrix[0, 1]
        return round(corr_coef, 2)

    @property
    def all_stats(self):
        """Return all statistical measures."""
        return {
            'mean': self.mean(),
            'median': self.median(),
            'variance': self.variance(),
            'std_builtin': self.std_builtin(),
            'std_manual': self.std_manual()
        }
