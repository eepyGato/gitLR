# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 26)
# Module: storage_pickle.py
# Purpose: Handle saving and loading rational numbers using pickle
# Version: 1.0
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------

import os
import pickle
from task1.rational import RationalNumber


def save_to_pickle():
    """Save all rational numbers to pickle file."""
    file_path = get_path_to_file()

    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as pickle_file_out:
            pickle.dump(obj=RationalNumber.all_numbers, file=pickle_file_out)

        print(f"✓ Successfully saved {len(RationalNumber.all_numbers)} rational numbers to Pickle")

    except IOError as e:
        print(f"✗ Error saving to Pickle: {e}")


def load_from_pickle():
    """Load rational numbers from pickle file."""
    file_path = get_path_to_file()

    try:
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            return

        RationalNumber.all_numbers.clear()

        with open(file_path, "rb") as pickle_file_in:
            loaded = pickle.load(pickle_file_in)
            RationalNumber.all_numbers.extend(loaded)

        print(f"✓ Successfully loaded {len(RationalNumber.all_numbers)} rational numbers from Pickle")

    except (IOError, pickle.PickleError) as e:
        print(f"✗ Error loading from Pickle: {e}")


def get_path_to_file() -> str:
    """Get path to pickle file."""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'rationals.pkl')