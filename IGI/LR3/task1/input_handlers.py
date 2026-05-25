"""
Module: input_handlers.py
Purpose: Input methods including a generator with yield.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

def manual_sequence():
    """Read list of x values from user input."""
    while True:
        raw = input("Enter x values separated by space or comma: ").strip()
        if not raw:
            print("Input cannot be empty.")
            continue
        parts = raw.replace(',', ' ').split()
        try:
            return [float(p) for p in parts]
        except ValueError:
            print("Invalid number. Use only numeric values.")

def arithmetic_progression_generator():
    """
    Generator (yield) that produces x values as an arithmetic progression.
    User provides start, step, and count. Yields one x at a time.
    """
    while True:
        try:
            start = float(input("Start value: "))
            step = float(input("Step: "))
            count = int(input("Number of values: "))
            if count <= 0:
                print("Count must be positive.")
                continue
            for i in range(count):
                yield start + i * step
            break
        except ValueError:
            print("Invalid input. Use numbers only.")

def get_epsilon():
    while True:
        try:
            eps = float(input("Enter accuracy eps (positive, e.g., 1e-6): "))
            if eps <= 0:
                print("Epsilon must be positive.")
                continue
            return eps
        except ValueError:
            print("Invalid number.")

def get_max_iterations():
    while True:
        try:
            s = input("Maximum iterations (default 500): ").strip()
            return 500 if s == "" else int(s)
        except ValueError:
            print("Invalid integer.")