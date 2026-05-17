# ---------------------------------------------------------
# Lab Work №4 - Task 4 (Variant 9)
# Module: shapes.py
# Purpose: Base classes and polygon implementation
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

from abc import ABC, abstractmethod
import math
from matplotlib.colors import is_color_like


class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""

    @abstractmethod
    def area(self) -> float:
        """Calculate area."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return figure name."""
        pass


class FigureColor:
    """Validates and stores figure color."""

    def __init__(self, color: str):
        self._color = self._validate_color(color)

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, new_color: str):
        self._color = self._validate_color(new_color)

    @staticmethod
    def _validate_color(color: str) -> str:
        if is_color_like(color):
            return color
        print(f"⚠️  Warning: '{color}' is not valid. Using 'black'\n")
        return "black"


class RegularPolygon(GeometricFigure):
    """Regular polygon with n equal sides and angles."""

    def __init__(self, n_sides: int, side_length: float, color: str, label: str = ""):
        """
        Initialize regular polygon.

        Args:
            n_sides: Number of sides (n >= 3)
            side_length: Length of each side (> 0)
            color: Color name or hex code
            label: Optional description
        """
        if n_sides < 3:
            raise ValueError("Number of sides must be >= 3")
        if side_length <= 0:
            raise ValueError("Side length must be > 0")

        self.n_sides = n_sides
        self.side_length = side_length
        self._color = FigureColor(color)
        self.label = label

    def area(self) -> float:
        """Area = (n * a^2) / (4 * tan(pi/n))"""
        cot = 1 / math.tan(math.pi / self.n_sides)
        return (self.n_sides * self.side_length ** 2 * cot) / 4

    def get_name(self) -> str:
        return f"Regular {self.n_sides}-gon"

    def get_perimeter(self) -> float:
        """Perimeter = n * a"""
        return self.n_sides * self.side_length

    def get_apothem(self) -> float:
        """Apothem = a / (2 * tan(pi/n))"""
        return self.side_length / (2 * math.tan(math.pi / self.n_sides))

    def get_circumradius(self) -> float:
        """Circumradius = a / (2 * sin(pi/n))"""
        return self.side_length / (2 * math.sin(math.pi / self.n_sides))

    def describe(self) -> str:
        """Return polygon description."""
        return (
                "\n" + "=" * 60 + "\n"
                                  f"Figure: {self.get_name()}\n"
                                  f"Color: {self._color.color}\n"
                                  f"Number of sides: {self.n_sides}\n"
                                  f"Side length: {self.side_length:.4f}\n"
                                  f"Perimeter: {self.get_perimeter():.4f}\n"
                                  f"Apothem: {self.get_apothem():.4f}\n"
                                  f"Circumradius: {self.get_circumradius():.4f}\n"
                                  f"Area: {self.area():.4f}\n"
                                  f"Label: {self.label if self.label else 'N/A'}\n"
                + "=" * 60 + "\n"
        )

    @property
    def color(self) -> str:
        return self._color.color

    @color.setter
    def color(self, new_color: str):
        self._color.color = new_color


class Rectangle(GeometricFigure):
    """Rectangle with width and height."""

    def __init__(self, width: float, height: float, color: str, label: str = ""):
        """
        Initialize rectangle.

        Args:
            width: Rectangle width (> 0)
            height: Rectangle height (> 0)
            color: Color name or hex code
            label: Optional description
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be > 0")

        self.width = width
        self.height = height
        self._color = FigureColor(color)
        self.label = label

    def area(self) -> float:
        """Area = width * height"""
        return self.width * self.height

    def get_name(self) -> str:
        return "Rectangle"

    def get_perimeter(self) -> float:
        """Perimeter = 2 * (width + height)"""
        return 2 * (self.width + self.height)

    def get_diagonal(self) -> float:
        """Diagonal = sqrt(width^2 + height^2)"""
        return math.sqrt(self.width ** 2 + self.height ** 2)

    def describe(self) -> str:
        """Return rectangle description."""
        return (
                "\n" + "=" * 60 + "\n"
                                  f"Figure: {self.get_name()}\n"
                                  f"Color: {self._color.color}\n"
                                  f"Width: {self.width:.4f}\n"
                                  f"Height: {self.height:.4f}\n"
                                  f"Perimeter: {self.get_perimeter():.4f}\n"
                                  f"Diagonal: {self.get_diagonal():.4f}\n"
                                  f"Area: {self.area():.4f}\n"
                                  f"Label: {self.label if self.label else 'N/A'}\n"
                + "=" * 60 + "\n"
        )

    @property
    def color(self) -> str:
        return self._color.color

    @color.setter
    def color(self, new_color: str):
        self._color.color = new_color
