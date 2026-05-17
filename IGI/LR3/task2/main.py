"""
Module: main.py
Purpose: Average of even numbers with generator.
Lab: 2
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

from stats_core import average_even, NoEvenNumbersError
from input_handlers import manual_input_until_one, random_int_generator

def validate_and_log(func):
    def wrapper(numbers):
        print(f"[LOG] Computing average for {numbers}")
        try:
            res = func(numbers)
            print(f"[LOG] Result = {res}")
            return res
        except NoEvenNumbersError as e:
            print(f"[LOG] {e}")
            return None
    return wrapper

average_even = validate_and_log(average_even)

def print_result(numbers, avg):
    print("\n" + "=" * 50)
    print(f"Numbers: {numbers}")
    print(f"Evens: {[n for n in numbers if n % 2 == 0]}")
    print(f"Average of evens: {avg:.4f}" if avg is not None else "No even numbers")
    print("=" * 50)

def main():
    print("*** Average of even numbers ***\n")
    while True:
        print("Choose input method:")
        print("1 - Manual entry (until 1)")
        print("2 - Random number generator (yield)")
        choice = input("Your choice (1/2): ").strip()
        if choice == '2':
            gen = random_int_generator()
            numbers = list(gen)
        else:
            numbers = manual_input_until_one()
        avg = average_even(numbers)
        print_result(numbers, avg)
        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            break
    print("Goodbye!")

if __name__ == "__main__":
    main()