"""
Module: input_handlers.py
Purpose: Input methods with yield generator.
Lab: 2
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

import random

def manual_input_until_one():
    numbers = []
    print("Enter integers (finish with 1):")
    while True:
        try:
            val = input("> ").strip()
            if not val:
                continue
            num = int(val)
            if num == 1:
                break
            numbers.append(num)
        except ValueError:
            print("Invalid integer.")
    return numbers

def random_int_generator():
    """
    Generator that yields random integers one by one.
    User specifies count, min, max.
    """
    while True:
        try:
            count = int(input("How many random numbers? "))
            if count <= 0:
                print("Positive count required.")
                continue
            low = int(input("Minimum: "))
            high = int(input("Maximum: "))
            if low > high:
                print("Min <= max required.")
                continue
            for _ in range(count):
                yield random.randint(low, high)
            break
        except ValueError:
            print("Invalid integer.")