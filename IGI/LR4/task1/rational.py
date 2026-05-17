# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 26)
# Module: rational.py
# Purpose: Define rational number class for fraction storage
# Version: 1.1 (Fixed - search doesn't add to list)
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------


class PrintableMixin:
    """Mixin to print all rational numbers passed as an argument."""

    @staticmethod
    def print_all(numbers):
        """
        Print all rational numbers passed as a list.

        Args:
            numbers: List of rational number objects to display
        """
        if not numbers:
            print("No data available.")
            return

        print("\n" + "=" * 60)
        print("All Rational Numbers:")
        print("=" * 60)

        for index, num in enumerate(numbers, 1):
            print(f"{index}. {num}")

        print("=" * 60 + "\n")


class RationalNumber(PrintableMixin):
    """Class for rational number with numerator and denominator."""

    all_numbers = []  # static list to store all rational numbers

    def __init__(self, numerator: int, denominator: int, add_to_list: bool = True):
        """
        Initialize a rational number object.

        Args:
            numerator (int): Numerator of the fraction
            denominator (int): Denominator of the fraction (cannot be zero)
            add_to_list (bool): Whether to add this number to all_numbers list
                               (default True, set False for temporary search objects)
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")

        self.numerator = numerator
        self.denominator = denominator
        
        # Only add to static list if specified
        if add_to_list:
            RationalNumber.all_numbers.append(self)

    def __str__(self) -> str:
        """
        String representation of rational number.

        Returns:
            str: Formatted rational number as numerator/denominator
        """
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other) -> bool:
        """
        Check equality of two rational numbers.
        Compares cross-multiplication to handle non-reduced fractions.

        Args:
            other: Another RationalNumber object

        Returns:
            bool: True if numbers are equal, False otherwise
        """
        if not isinstance(other, RationalNumber):
            return False
        # a/b == c/d  <=>  a*d == b*c
        return self.numerator * other.denominator == self.denominator * other.numerator

    def __lt__(self, other) -> bool:
        """
        Check if this rational number is less than another.
        Compares cross-multiplication.

        Args:
            other: Another RationalNumber object

        Returns:
            bool: True if self < other, False otherwise
        """
        if not isinstance(other, RationalNumber):
            return NotImplemented
        # a/b < c/d  <=>  a*d < b*c
        return self.numerator * other.denominator < self.denominator * other.numerator

    def __gt__(self, other) -> bool:
        """
        Check if this rational number is greater than another.

        Args:
            other: Another RationalNumber object

        Returns:
            bool: True if self > other, False otherwise
        """
        if not isinstance(other, RationalNumber):
            return NotImplemented
        return self.numerator * other.denominator > self.denominator * other.numerator

    def to_float(self) -> float:
        """
        Convert rational number to float.

        Returns:
            float: Decimal representation of the fraction
        """
        return self.numerator / self.denominator

    @classmethod
    def find_equal_numbers(cls) -> list:
        """
        Find groups of equal rational numbers.

        Returns:
            list: List of lists, each containing indices of equal numbers
        """
        if len(cls.all_numbers) < 2:
            return []

        equal_groups = []
        used_indices = set()

        for i, num1 in enumerate(cls.all_numbers):
            if i in used_indices:
                continue

            group = [i + 1]  # 1-based index for display
            for j, num2 in enumerate(cls.all_numbers):
                if i != j and j not in used_indices and num1 == num2:
                    group.append(j + 1)
                    used_indices.add(j)

            if len(group) > 1:
                equal_groups.append(group)
            used_indices.add(i)

        return equal_groups

    @classmethod
    def find_maximum(cls):
        """
        Find the maximum rational number.

        Returns:
            RationalNumber: Largest rational number or None if list is empty
        """
        if not cls.all_numbers:
            return None
        return max(cls.all_numbers)

    @classmethod
    def find_number_by_value(cls, numerator: int, denominator: int):
        """
        Find a rational number by its value (can be non-reduced).
        This method does NOT add the search number to the list.

        Args:
            numerator (int): Numerator to search for
            denominator (int): Denominator to search for

        Returns:
            RationalNumber: Matching number or None
        """
        # Create temporary number WITHOUT adding to list
        search_num = RationalNumber(numerator, denominator, add_to_list=False)
        
        for num in cls.all_numbers:
            if num == search_num:
                return num
        return None

    @classmethod
    def reset(cls):
        """Clear all stored numbers (useful for loading from file)."""
        cls.all_numbers.clear()