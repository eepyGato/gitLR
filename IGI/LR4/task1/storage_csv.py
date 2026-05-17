# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 9)
# Module: storage_csv.py
# Purpose: Handle saving and loading persons from CSV files
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import csv
import os
from task1.person import Person


def save_to_csv():
    file_path = get_path_to_file()

    try:
        with open(file_path, "w", newline='', encoding='utf-8') as file_csv_out:
            writer = csv.writer(file_csv_out)
            writer.writerow(["Surname", "Gender", "Height"])  # header

            for person in Person.all_persons:
                writer.writerow([person.last_name, person.gender, person.height])

        print(f"✓ Successfully saved {len(Person.all_persons)} persons to CSV")

    except IOError as e:
        print(f"✗ Error saving to CSV: {e}")


def load_from_csv():
    file_path = get_path_to_file()

    try:
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            return

        Person.all_persons.clear()

        with open(file_path, newline='', encoding='utf-8') as file_csv_in:
            reader_csv = csv.reader(file_csv_in)
            next(reader_csv)  # skip header

            loaded_count = 0
            for row in reader_csv:
                if row and len(row) >= 3:
                    try:
                        surname, gender, height = row[0], row[1], float(row[2])
                        Person(surname, gender, height)
                        loaded_count += 1
                    except ValueError:
                        print(f"✗ Invalid data format in row: {row}")

        print(f"✓ Successfully loaded {loaded_count} persons from CSV")

    except IOError as e:
        print(f"✗ Error loading from CSV: {e}")


def get_path_to_file() -> str:
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'persons.csv')
