"""
Module: input_handlers.py
Purpose: Input methods including a line generator (yield).
Lab: 3
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

def manual_text_input():
    return input("Enter a string: ")

def demo_text():
    return "hello world! This is a Demo string. apple Banana cat."

def file_line_generator(filename="sample.txt"):
    """
    Generator that yields lines from a file one by one.
    For demonstration, we'll collect all lines into one string.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found. Yielding empty.")
        yield ""