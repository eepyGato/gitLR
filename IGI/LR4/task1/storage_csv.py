# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 26)
# Module: storage_csv.py
# Purpose: Handle saving and loading rational numbers from CSV files
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

import csv
import os
from task1.rational import RationalNumber


def save_to_csv():
    """Save all rational numbers to CSV file."""
    file_path = get_path_to_file()

    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", newline='', encoding='utf-8') as file_csv_out:
            writer = csv.writer(file_csv_out)
            writer.writerow(["Numerator", "Denominator"])  # header

            for num in RationalNumber.all_numbers:
                writer.writerow([num.numerator, num.denominator])

        print(f"✓ Successfully saved {len(RationalNumber.all_numbers)} rational numbers to CSV")

    except IOError as e:
        print(f"✗ Error saving to CSV: {e}")


def load_from_csv():
    """Load rational numbers from CSV file."""
    file_path = get_path_to_file()

    try:
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            return

        RationalNumber.all_numbers.clear()

        with open(file_path, newline='', encoding='utf-8') as file_csv_in:
            reader_csv = csv.reader(file_csv_in)
            next(reader_csv)  # skip header

            loaded_count = 0
            for row in reader_csv:
                if row and len(row) >= 2:
                    try:
                        numerator = int(row[0])
                        denominator = int(row[1])
                        RationalNumber(numerator, denominator)
                        loaded_count += 1
                    except (ValueError, ZeroDivisionError) as e:
                        print(f"✗ Invalid data format in row {row}: {e}")

        print(f"✓ Successfully loaded {loaded_count} rational numbers from CSV")

    except IOError as e:
        print(f"✗ Error loading from CSV: {e}")


def get_path_to_file() -> str:
    """Get path to CSV file."""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'rationals.csv')