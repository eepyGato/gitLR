"""
Module: main.py
Purpose: List processing with generator.
Lab: 5
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

from list_processing import sum_negative, product_between_min_max, EmptyListError, SingleElementError
from input_handlers import manual_input_list, random_float_generator
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"[TIMER] {func.__name__} took {time.time()-start:.6f}s")
        return res
    return wrapper

@timer_decorator
def process_list(numbers):
    s_neg = sum_negative(numbers)
    prod = product_between_min_max(numbers)
    return s_neg, prod

def print_list(numbers):
    formatted = [f"{x:.2f}" for x in numbers]
    print("List:", ", ".join(formatted))

def main():
    print("*** Sum of negatives & product between min/max ***\n")
    while True:
        print("Choose input method:")
        print("1 - Manual entry")
        print("2 - Random float generator (yield)")
        choice = input("Your choice (1/2): ").strip()
        if choice == '2':
            gen = random_float_generator()
            numbers = list(gen)
        else:
            numbers = manual_input_list()
        print("\nYour list:")
        print_list(numbers)
        try:
            s_neg, prod = process_list(numbers)
            print(f"Sum of negatives: {s_neg:.4f}")
            print(f"Product between min and max (exclusive): {prod:.4f}")
        except (EmptyListError, SingleElementError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected: {e}")
        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            break
    print("Goodbye!")

if __name__ == "__main__":
    main()