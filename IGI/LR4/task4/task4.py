# ---------------------------------------------------------
# Lab Work №4 - Task 4 (Variant 9)
# Module: task4.py
# Purpose: Main task logic for polygon construction
# Version: 1.1
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

from task4.shapes import RegularPolygon, Rectangle
from task4.plot import draw_polygon, draw_rectangle
from utils.inputValidator import input_data

DESCRIPTION = r"""
╔═══════════════════════════════════════════════════════════╗
║                Regular Polygon Constructor                ║
║                                                           ║
║  Task: Build a regular n-gon with side length a           ║
║                                                           ║
║  A regular polygon has:                                   ║
║  • All sides of equal length                              ║
║  • All angles equal                                       ║
║  • n ≥ 3 (triangle minimum)                               ║
║                                                           ║
║  Key Formulas:                                            ║
║  • Area = (n * a²) / (4 * tan(π / n))                     ║
║  • Perimeter = n * a                                      ║
║  • Apothem = a / (2 * tan(π / n))                         ║
║  • Circumradius = a / (2 * sin(π / n))                    ║
║                                                           ║
║  This program:                                            ║
║  • Creates regular polygons with user-defined parameters  ║
║  • Calculates area, perimeter, and radii                  ║
║  • Visualizes the polygon                                 ║
║  • Saves visualization to file                            ║
╚═══════════════════════════════════════════════════════════╝
"""


def print_description():
    """Print task description."""
    print(DESCRIPTION)


def task4() -> bool:
    """
    Main function for polygon constructor program.

    Allows user to:
    1. Input polygon parameters (number of sides, side length, color, label)
    2. Validate input data
    3. Create RegularPolygon object
    4. Display polygon properties (EXACTLY ONCE)
    5. Visualize polygon with matplotlib
    6. Save visualization to file
    7. Repeat or return to menu

    Returns:
        bool: Always True to return to menu
    """
    print_description()

    while True:
        print("\n" + "=" * 70)
        print("POLYGON PARAMETERS".center(70))
        print("=" * 70)

        try:
            n_sides = input_data("\nEnter number of sides (n >= 3): ", int, min_value=3)
            side_length = input_data("Enter side length (a > 0): ", float, min_value=0)
            color = input_data("Enter color (e.g., 'blue', 'red', 'green', 'purple', '#FF5733'): ", str)
            label = input_data("Enter label for polygon (or press Enter to skip): ", str)

            print(f"\n Creating regular {n_sides}-gon...")
            polygon = RegularPolygon(n_sides, side_length, color, label)

            print(polygon.describe())

            visualize = input("Visualize polygon? (y/n): ").strip().lower()
            if visualize == 'y':
                print("\nGenerating visualization...")
                draw_polygon(polygon)

        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")

        print("-" * 70)
        again = input("Create another polygon? (1=yes, other=no): ").strip()

        if again != '1':
            print("\n✓ Returning to main menu...\n")
            return True


def task4_bonus() -> bool:
    """
    Bonus: Rectangle constructor for comparison with polygon.

    Rectangle properties:
    • Area = width * height
    • Perimeter = 2 * (width + height)
    • Diagonal = sqrt(width² + height²)

    Returns:
        bool: Always True to return to menu
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║  Rectangle Constructor (Bonus)".ljust(69) + "║")
    print("╚" + "═" * 68 + "╝\n")

    while True:
        print("\n" + "=" * 70)
        print("RECTANGLE PARAMETERS".center(70))
        print("=" * 70)

        try:
            width = input_data("\nEnter width (w > 0): ", float, min_value=0)
            height = input_data("Enter height (h > 0): ", float, min_value=0)
            color = input_data("Enter color (e.g., 'blue', 'red', 'green'): ", str)
            label = input_data("Enter label for rectangle: ", str)

            print(f"\nCreating rectangle {width} x {height}...")
            rectangle = Rectangle(width, height, color, label)

            print(rectangle.describe())

            visualize = input("Visualize rectangle? (y/n): ").strip().lower()
            if visualize == 'y':
                print("\nGenerating visualization...")
                draw_rectangle(rectangle)

        except ValueError as e:
            print(f"\n✗ Invalid input: {e}")
        except Exception as e:
            print(f"\n✗ Error: {e}")

        print("-" * 70)
        again = input("Create another rectangle? (1=yes, other=no): ").strip()
        if again != '1':
            print("\n✓ Returning to main menu...\n")
            return True
