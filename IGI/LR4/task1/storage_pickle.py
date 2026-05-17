# ---------------------------------------------------------
# Lab Work №4 - Task 1 (Variant 9)
# Module: storage_pickle.py
# Purpose: Handle saving and loading persons using pickle serialization
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import os
import pickle
from task1.person import Person


def save_to_pickle():
    file_path = get_path_to_file()

    try:
        with open(file_path, "wb") as pickle_file_out:
            pickle.dump(obj=Person.all_persons, file=pickle_file_out)

        print(f"✓ Successfully saved {len(Person.all_persons)} persons to Pickle")

    except IOError as e:
        print(f"✗ Error saving to Pickle: {e}")


def load_from_pickle():
    file_path = get_path_to_file()

    try:
        if not os.path.exists(file_path):
            print(f"✗ File not found: {file_path}")
            return

        Person.all_persons.clear()

        with open(file_path, "rb") as pickle_file_in:
            loaded = pickle.load(pickle_file_in)
            Person.all_persons.extend(loaded)

        print(f"✓ Successfully loaded {len(Person.all_persons)} persons from Pickle")

    except (IOError, pickle.PickleError) as e:
        print(f"✗ Error loading from Pickle: {e}")


def get_path_to_file() -> str:
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', 'persons.pkl')

