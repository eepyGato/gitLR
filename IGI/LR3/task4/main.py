"""
Module: main.py
Purpose: Main program for Lab 4 – string analysis.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

from string_analysis import split_words, count_words, find_longest_word, get_odd_words, EmptyTextError
from input_handlers import predefined_text, user_input_text

# ---------- Decorator: logging ----------
def log_analysis(func):
    """Decorator to log the analysis step."""
    def wrapper(text):
        print(f"[LOG] Analysing text (first 60 chars): {text[:60]}...")
        result = func(text)
        print(f"[LOG] Analysis complete.")
        return result
    return wrapper

# Apply decorator to a wrapper function that performs all tasks
@log_analysis
def analyze_text(text):
    """Perform all three tasks on the text."""
    words = split_words(text)
    if not words:
        raise EmptyTextError("No words found after splitting.")
    
    total = count_words(words)
    longest, idx = find_longest_word(words)
    odd_words = get_odd_words(words)
    
    return {
        'words': words,
        'total': total,
        'longest': longest,
        'longest_index': idx,
        'odd_words': odd_words
    }

# ---------- Result printer ----------
def print_results(results):
    """Print the results in a formatted way."""
    print("\n" + "=" * 70)
    print(f"Total number of words: {results['total']}")
    print(f"Longest word: '{results['longest']}' (position {results['longest_index']})")
    print("\nOdd-positioned words (1st, 3rd, 5th, ...):")
    for i, w in enumerate(results['odd_words'], start=1):
        print(f"  {2*i-1}: {w}")
    print("=" * 70)

# ---------- Main program ----------
def main():
    print("*** String Analysis: Count words, longest word, odd words ***\n")

    while True:
        print("Choose input method:")
        print("1 - Use predefined text from the assignment")
        print("2 - Enter your own text")
        choice = input("Your choice (1/2): ").strip()

        if choice == '1':
            text = predefined_text()
            print("\n[Using predefined text]")
        elif choice == '2':
            text = user_input_text()
        else:
            print("Invalid choice. Defaulting to predefined text.")
            text = predefined_text()

        try:
            results = analyze_text(text)
            print_results(results)
        except EmptyTextError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        again = input("\nRun again? (y/n): ").lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()