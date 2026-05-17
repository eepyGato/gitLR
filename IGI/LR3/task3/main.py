"""
Module: main.py
Purpose: Count lowercase-starting words with generator.
Lab: 3
Version: 1.0 (with generator)
Developer: Ivan Petrov
Date: 2026-04-07
"""

from text_analysis import count_lowercase_words, EmptyStringError
from input_handlers import manual_text_input, demo_text, file_line_generator

def log_call(func):
    def wrapper(text):
        print(f"[LOG] Analysing: '{text[:50]}...'")
        res = func(text)
        print(f"[LOG] Result: {res}")
        return res
    return wrapper

count_lowercase_words = log_call(count_lowercase_words)

def print_result(text, count):
    print("\n" + "=" * 60)
    print(f"Text: {text}")
    print(f"Lowercase-starting words count: {count}")
    print("=" * 60)

def main():
    print("*** Count words starting with lowercase letter ***\n")
    while True:
        print("Choose input method:")
        print("1 - Manual entry")
        print("2 - Demo text")
        print("3 - File line generator (reads sample.txt line by line)")
        choice = input("Your choice (1/2/3): ").strip()
        if choice == '3':
            gen = file_line_generator()
            # Combine all lines into one string for analysis
            lines = list(gen)
            text = " ".join(lines)
            if not text:
                print("No text from generator.")
                continue
        elif choice == '2':
            text = demo_text()
        else:
            text = manual_text_input()
        
        try:
            count = count_lowercase_words(text)
            print_result(text, count)
        except EmptyStringError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            break
    print("Goodbye!")

if __name__ == "__main__":
    main()