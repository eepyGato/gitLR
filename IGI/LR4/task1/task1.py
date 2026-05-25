# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 26)
# Module: task1.py
# Purpose: Main interface for rational number management
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

from task1.rational import RationalNumber
from task1.storage_csv import save_to_csv, load_from_csv
from task1.storage_pickle import save_to_pickle, load_from_pickle

DESCRIPTION = """
╔══════════════════════════════════════════════════════════════════════╗
║                 Rational Number Management System                     ║
║                                                                       ║
║  This program manages rational numbers in the form: numerator/denominator ║
║                                                                       ║
║  Capabilities:                                                        ║
║  ✓ Add new rational number                                            ║
║  ✓ Check for equal rational numbers (even if not reduced)             ║
║  ✓ Find the maximum rational number                                   ║
║  ✓ Search for a specific rational number                              ║
║  ✓ Display information about a number entered from keyboard           ║
║  ✓ Save/Load data from CSV and Pickle formats                         ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def display_menu():
    """Display main menu with all available options."""
    print("\n" + "=" * 60)
    print("Rational Number Management Menu")
    print("=" * 60)
    print("1.  Add new rational number")
    print("2.  Find equal rational numbers")
    print("3.  Find maximum rational number")
    print("4.  Search for specific rational number")
    print("5.  Display number info (from keyboard input)")
    print("6.  Show all rational numbers")
    print("7.  Save to CSV")
    print("8.  Load from CSV")
    print("9.  Save to Pickle")
    print("10. Load from Pickle")
    print("0.  Exit\n")


def input_rational_number(prompt: str):
    """
    Input a rational number from user.

    Args:
        prompt (str): Prompt message

    Returns:
        tuple: (numerator, denominator) or (None, None) on error
    """
    print(prompt)
    try:
        numerator = int(input("  Enter numerator: "))
        denominator = int(input("  Enter denominator (non-zero): "))

        if denominator == 0:
            print("✗ Denominator cannot be zero!")
            return None, None

        return numerator, denominator
    except ValueError:
        print("✗ Invalid input. Please enter integers.")
        return None, None


def add_number():
    """Add a new rational number."""
    print("\n" + "-" * 40)
    print("Add New Rational Number")
    print("-" * 40)

    numerator, denominator = input_rational_number("Enter rational number:")

    if numerator is not None:
        try:
            RationalNumber(numerator, denominator)
            print(f"✓ Added: {numerator}/{denominator}\n")
        except ValueError as e:
            print(f"✗ {e}\n")


def find_equal_numbers():
    """Find and display equal rational numbers."""
    print("\n" + "-" * 40)
    print("Find Equal Rational Numbers")
    print("-" * 40)

    if len(RationalNumber.all_numbers) < 2:
        print("\n✗ Need at least 2 numbers to check for equality\n")
        return

    equal_groups = RationalNumber.find_equal_numbers()

    if equal_groups:
        print("\n✓ Found equal rational numbers:\n")
        for group in equal_groups:
            print(f"  Numbers at positions {group} are equal:")
            for idx in group:
                num = RationalNumber.all_numbers[idx - 1]
                print(f"    • Position {idx}: {num}")
            print()
    else:
        print("\n✗ No equal rational numbers found\n")


def find_maximum():
    """Find and display the maximum rational number."""
    print("\n" + "-" * 40)
    print("Find Maximum Rational Number")
    print("-" * 40)

    if not RationalNumber.all_numbers:
        print("\n✗ No numbers in the list\n")
        return

    maximum = RationalNumber.find_maximum()

    if maximum:
        print(f"\n✓ Maximum rational number: {maximum}")
        print(f"  Decimal value: {maximum.to_float():.6f}\n")


def search_number():
    """Search for a specific rational number."""
    print("\n" + "-" * 40)
    print("Search for Rational Number")
    print("-" * 40)

    numerator, denominator = input_rational_number("Enter rational number to search:")

    if numerator is not None:
        found = RationalNumber.find_number_by_value(numerator, denominator)

        if found:
            print(f"\n✓ Found: {found}")
            # Find all positions
            positions = []
            for i, num in enumerate(RationalNumber.all_numbers, 1):
                if num == found:
                    positions.append(i)
            print(f"  Found at position(s): {positions}\n")
        else:
            print(f"\n✗ {numerator}/{denominator} not found in the list\n")


def display_number_info():
    """Display information about a number entered from keyboard."""
    print("\n" + "-" * 40)
    print("Display Number Information")
    print("-" * 40)

    numerator, denominator = input_rational_number("Enter rational number to analyze:")

    if numerator is not None:
        try:
            num = RationalNumber(numerator, denominator)

            print("\n" + "=" * 50)
            print("Rational Number Information")
            print("=" * 50)
            print(f"Fraction form:     {num}")
            print(f"Decimal value:     {num.to_float():.10f}")
            print(f"Numerator:         {num.numerator}")
            print(f"Denominator:       {num.denominator}")

            # Check if in list
            if num in RationalNumber.all_numbers:
                positions = [i for i, n in enumerate(RationalNumber.all_numbers, 1) if n == num]
                print(f"In current list:   Yes (at position(s): {positions})")
            else:
                print("In current list:   No")

            # Check if reduced
            from math import gcd
            g = gcd(abs(num.numerator), abs(num.denominator))
            if g > 1:
                reduced = f"{num.numerator // g}/{num.denominator // g}"
                print(f"Reduced form:      {reduced}")

            print("=" * 50 + "\n")
        except ValueError as e:
            print(f"✗ {e}\n")


def show_all_numbers():
    """Display all rational numbers."""
    RationalNumber.print_all(RationalNumber.all_numbers)


def print_description():
    """Print program description."""
    print(DESCRIPTION)


def task1():
    """Main program loop."""
    print_description()

    while True:
        display_menu()

        try:
            choice = input("Choose an option (0-10): ").strip()

            if not choice:
                continue

            choice = int(choice)

            if choice == 0:
                print("\n✓ Exiting program...\n")
                break
            elif choice == 1:
                add_number()
            elif choice == 2:
                find_equal_numbers()
            elif choice == 3:
                find_maximum()
            elif choice == 4:
                search_number()
            elif choice == 5:
                display_number_info()
            elif choice == 6:
                show_all_numbers()
            elif choice == 7:
                save_to_csv()
            elif choice == 8:
                load_from_csv()
            elif choice == 9:
                save_to_pickle()
            elif choice == 10:
                load_from_pickle()
            else:
                print("✗ Invalid choice. Please enter 0-10\n")

        except ValueError:
            print("✗ Please enter a valid number\n")
        except KeyboardInterrupt:
            print("\n\n✓ Program interrupted by user")
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}\n")


if __name__ == "__main__":
    task1()