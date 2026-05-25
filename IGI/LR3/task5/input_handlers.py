"""
Module: input_handlers.py
Purpose: Input methods including a random float generator.
Lab: 5
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

import random

def manual_input_list():
    while True:
        raw = input("Enter numbers separated by space: ").strip()
        if not raw:
            print("Empty input.")
            continue
        parts = raw.split()
        numbers = []
        ok = True
        for p in parts:
            try:
                numbers.append(float(p))
            except ValueError:
                print(f"Invalid: '{p}'")
                ok = False
                break
        if ok and numbers:
            return numbers

def random_float_generator():
    """
    Generator that yields random floats one by one.
    User specifies count, min, max.
    """
    while True:
        try:
            count = int(input("How many numbers? "))
            if count <= 0:
                print("Positive count.")
                continue
            low = float(input("Min: "))
            high = float(input("Max: "))
            if low > high:
                print("Min <= max.")
                continue
            for _ in range(count):
                yield random.uniform(low, high)
            break
        except ValueError:
            print("Invalid number.")