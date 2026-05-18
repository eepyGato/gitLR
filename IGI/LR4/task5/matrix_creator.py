# ---------------------------------------------------------
# Lab Work №4 - Task 5 (Variant 26)
# Module: matrix_creator.py
# Purpose: Matrix creation and statistical operations
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
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

    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)
        self.min_value = None
        self.min_indices = None

    def generate_matrix(self):
        """Generate random integer matrix [-100, 100]."""
        self.matrix = np.random.randint(-100, 101, (self.rows, self.cols))

    def find_first_min_element(self):
        """
        Find the first occurrence of the minimum element in the matrix.
        Returns (row_index, col_index) of the first minimum element.
        """
        self.min_value = self.matrix.min()
        self.min_indices = np.argwhere(self.matrix == self.min_value)
        # Return the first occurrence (row-major order)
        return tuple(self.min_indices[0])

    def insert_row_after_min(self):
        """
        Insert the first row after the row containing the first minimum element.
        
        Returns:
            tuple: (inserted_row_index, first_min_row_index)
        """
        # Find the first minimum element
        min_row, min_col = self.find_first_min_element()
        
        # Get the first row (row index 0)
        first_row = self.matrix[0, :].copy()
        
        # Insert the first row after the row with the minimum element
        # Insert at position min_row + 1
        self.matrix = np.insert(self.matrix, min_row + 1, first_row, axis=0)
        
        return min_row + 1, min_row

    def get_first_row(self):
        """Get the first row of the matrix."""
        return self.matrix[0, :]

    def get_row(self, index: int):
        """Get a specific row by index."""
        return self.matrix[index, :]

    def get_matrix_info(self):
        """Get matrix dimensions and basic info."""
        return {
            "shape": self.matrix.shape,
            "size": self.matrix.size,
            "min_value": self.min_value if self.min_value is not None else self.matrix.min()
        }


class MatrixAnalyzer:
    """Performs statistical operations on matrix rows."""

    def __init__(self, matrix):
        self.matrix = matrix

    def median_builtin(self, row_index: int = 0):
        """
        Calculate median of a row using NumPy's built-in function.
        
        Args:
            row_index (int): Index of the row (default: 0 - first row)
        
        Returns:
            float: Median value
        """
        row = self.matrix[row_index, :]
        return np.median(row)

    def median_manual(self, row_index: int = 0):
        """
        Calculate median of a row manually (without using np.median).
        
        Manual calculation:
        1. Sort the array
        2. If length is odd: middle element
        3. If length is even: average of two middle elements
        
        Args:
            row_index (int): Index of the row (default: 0 - first row)
        
        Returns:
            float: Median value
        """
        row = self.matrix[row_index, :].copy()
        
        # Sort the row
        sorted_row = np.sort(row)
        n = len(sorted_row)
        
        if n % 2 == 1:
            # Odd number of elements - take the middle
            median = float(sorted_row[n // 2])
        else:
            # Even number of elements - average of two middle
            median = (sorted_row[n // 2 - 1] + sorted_row[n // 2]) / 2.0
        
        return median

    def mean(self, row_index: int = 0):
        """Calculate mean of a row."""
        row = self.matrix[row_index, :]
        return np.mean(row)

    def variance(self, row_index: int = 0):
        """Calculate variance of a row."""
        row = self.matrix[row_index, :]
        return np.var(row)

    def std(self, row_index: int = 0):
        """Calculate standard deviation of a row."""
        row = self.matrix[row_index, :]
        return np.std(row)

    def correlation(self, row1_index: int, row2_index: int):
        """
        Calculate correlation coefficient between two rows.
        
        Args:
            row1_index (int): Index of first row
            row2_index (int): Index of second row
        
        Returns:
            float: Correlation coefficient rounded to 2 decimal places
        """
        row1 = self.matrix[row1_index, :]
        row2 = self.matrix[row2_index, :]
        
        stacked = np.vstack([row1, row2])
        corr_matrix = np.corrcoef(stacked)
        corr_coef = corr_matrix[0, 1]
        
        # Handle NaN cases (when row has constant values)
        if np.isnan(corr_coef):
            return 0.0
        
        return round(corr_coef, 2)

    def get_row_stats(self, row_index: int = 0):
        """Get all statistical measures for a row."""
        return {
            'mean': round(self.mean(row_index), 4),
            'median_builtin': round(self.median_builtin(row_index), 4),
            'median_manual': round(self.median_manual(row_index), 4),
            'variance': round(self.variance(row_index), 4),
            'std': round(self.std(row_index), 4)
        }