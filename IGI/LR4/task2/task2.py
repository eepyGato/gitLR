# ---------------------------------------------------------
# Lab Work №4 - Task 2 (Variant 9)
# Module: task2.py
# Purpose: Main interface for text analysis system
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import os

from task2.analyzer import (
    SentenceAnalyzer,
    WordAnalyzer,
    SmileyAnalyzer,
    DateAnalyzer
)

from task2.archiver import archive_file, save_results_to_file
from utils.inputValidator import input_data

DESCRIPTION = """
╔═══════════════════════════════════════════════════════════╗
║                   Text Analysis System                    ║
║                                                           ║
║  This program analyzes text using regular expressions:    ║
║  ✓ Extract dates in format DD-MM-YYYY                     ║
║  ✓ Find words ending with vowel (penultimate consonant)   ║
║  ✓ Count lowercase letters                                ║
║  ✓ Find last word containing 'i'                          ║
║  ✓ Remove words starting with 'i'                         ║
║  ✓ Analyze sentence structure (all types)                 ║
║  ✓ Calculate average lengths                              ║
║  ✓ Count valid smileys                                    ║
║  ✓ Archive results in ZIP                                 ║
╚═══════════════════════════════════════════════════════════╝
"""


def display_menu():
    """Display main analysis menu."""
    print("\n" + "=" * 60)
    print("Text Analyzer Menu")
    print("=" * 60)
    print("1.  Analyze sentences")
    print("2.  Analyze words (Variant 9 specific)")
    print("3.  Count smileys")
    print("4.  Extract dates (DD-MM-YYYY)")
    print("5.  Archive and compress results")
    print("6.  Show all analysis results")
    print("0.  Exit\n")


def get_path_to_file(file: str) -> str:
    """
    Get absolute path to file in task2/files directory.

    Args:
        file (str): Filename

    Returns:
        str: Absolute path
    """
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_file_dir, 'files', file)


def get_text() -> str:
    """
    Read text from file.txt in task2/files directory.

    Returns:
        str: Text content or None if file not found
    """
    try:
        with open(get_path_to_file("file.txt"), "r", encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("✗ Text file not found: task2/files/file.txt")
        return None


def analyze_sentences():
    """Analyze sentence statistics from text."""
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Sentence Analysis")
    print("-" * 60)

    result = SentenceAnalyzer(text).process()

    print(f"\n Total sentences:              {result['total']}")
    print(f"\n Sentence types:")
    print(f"   • Declarative (.) :           {result['declarative']}")
    print(f"   • Interrogative (?):          {result['interrogative']}")
    print(f"   • Imperative (!):             {result['imperative']}")

    print(f"\n Lengths:")
    print(f"   • Avg sentence (words):       {result['avg_sentence_length']} words")
    print(f"   • Avg sentence (chars):       {result['avg_sentence_chars']} characters\n")


def analyze_words():
    """
    Analyze words with variant 9 specific.

    Tasks:
    1. Extract dates in format DD-MM-YYYY
    2. Find words ending with vowel AND penultimate letter is consonant
    3. Count lowercase letters
    4. Find last word containing 'i' and its position
    5. Output text with words starting with 'i' removed
    """
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Word Analysis")
    print("-" * 60)

    result = WordAnalyzer(text).process()

    print(f"\n General statistics:")
    print(f"   • Total words:                {result['word_count']}")
    print(f"   • Average word length:        {result['avg_word_length']} characters")

    print(f"\n Lowercase letters in text:   {result['lowercase_count']}")

    print(f"\n Extracted dates (DD-MM-YYYY):")
    if result['word_count'] > 0 and result['dates']:
        for date in result['dates']:
            print(f"   • {date}")
    else:
        print("   (no dates found)")

    print(f"\n Words ending with vowel (penultimate is consonant):")
    if result['words_vowel_ending_consonant_penultimate']:
        words_list = result['words_vowel_ending_consonant_penultimate']
        print(f"   Count: {len(words_list)}")
        print(f"   Words: {', '.join(words_list[:10])}")
        if len(words_list) > 10:
            print(f"   ... and {len(words_list) - 10} more")
    else:
        print("   (no words found)")

    print(f"\n Last word containing 'i':")
    if result['last_word_with_i']:
        print(f"   Word: {result['last_word_with_i']}")
        print(f"   Position: #{result['last_word_with_i_index']}")
    else:
        print("   (no word with 'i' found)")

    print(f"\n Text without words starting with 'i':")
    if result['text_without_i_words']:
        text_preview = result['text_without_i_words'][:100]
        print(f"   {text_preview}...")
    else:
        print("   (no text after filtering)")
    print()


def analyze_smileys():
    """Analyze and count valid smileys in text."""
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Smiley Analysis")
    print("-" * 60)

    result = SmileyAnalyzer(text).process()

    print(f"\n Total valid smileys:         {result['smiley_count']}")

    if result['smileys']:
        print(f"\nValid smileys found:")
        for smiley in result['smileys']:
            print(f"   • {smiley}")
    else:
        print("\n(no valid smileys found)")


def extract_dates():
    """Extract and display dates from text."""
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Date Extraction (DD-MM-YYYY)")
    print("-" * 60)

    result = DateAnalyzer(text).process()

    print(f"\n Total dates found:           {result['date_count']}")

    if result['dates']:
        print(f"\nDates:")
        for date in result['dates']:
            print(f"   • {date}")
    else:
        print("\n(no dates found)")

    print()


def archive_results():
    """Perform complete analysis and archive results."""
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Archiving Analysis Results")
    print("-" * 60 + "\n")

    sentence_result = SentenceAnalyzer(text).process()
    word_result = WordAnalyzer(text).process()
    smiley_result = SmileyAnalyzer(text).process()
    date_result = DateAnalyzer(text).process()

    results = [
        "=" * 70,
        "TEXT ANALYSIS RESULTS (Variant 9)".center(70),
        "=" * 70,
        "",
        "1. SENTENCE ANALYSIS",
        "-" * 70,
        f"   Total sentences:                           {sentence_result['total']}",
        f"   Declarative sentences (.):                 {sentence_result['declarative']}",
        f"   Interrogative sentences (?):               {sentence_result['interrogative']}",
        f"   Imperative sentences (!):                  {sentence_result['imperative']}",
        f"   Average sentence length (words):           {sentence_result['avg_sentence_length']} words",
        f"   Average sentence length (characters):      {sentence_result['avg_sentence_chars']} chars",
        "",
        "2. WORD ANALYSIS",
        "-" * 70,
        f"   Total words:                               {word_result['word_count']}",
        f"   Average word length:                       {word_result['avg_word_length']} characters",
        f"   Total lowercase letters:                   {word_result['lowercase_count']}",
        f"   Words (vowel ending, consonant penultimate): {len(word_result['words_vowel_ending_consonant_penultimate'])}",
        f"   Last word with 'i':                        {word_result['last_word_with_i']} (position: {word_result['last_word_with_i_index']})",
        f"   Total dates found (DD-MM-YYYY):            {date_result['date_count']}",
        "",
        "3. SMILEY ANALYSIS",
        "-" * 70,
        f"   Total valid smileys:                       {smiley_result['smiley_count']}",
        "",
    ]

    if word_result['words_vowel_ending_consonant_penultimate']:
        results.append("   Words (vowel ending, consonant penultimate):")
        words_list = word_result['words_vowel_ending_consonant_penultimate']
        results.append(f"      {', '.join(words_list[:20])}")
        if len(words_list) > 20:
            results.append(f"      ... and {len(words_list) - 20} more")
        results.append("")

    if date_result['dates']:
        results.append("   Dates found:")
        for date in date_result['dates']:
            results.append(f"      • {date}")
        results.append("")

    if smiley_result['smileys']:
        results.append("   Valid smileys found:")
        for smiley in smiley_result['smileys']:
            results.append(f"      • {smiley}")
        results.append("")

    results.append("4. TEXT WITHOUT WORDS STARTING WITH 'I'")
    results.append("-" * 70)
    if word_result['text_without_i_words']:
        results.append(f"   {word_result['text_without_i_words'][:300]}")
    else:
        results.append("   (no text after filtering)")

    results.append("")
    results.append("=" * 70)
    results.append("End of Analysis Report")
    results.append("=" * 70)

    result_file = get_path_to_file("result.txt")
    save_results_to_file(result_file, results)

    try:
        archive_info = archive_file(result_file)
        if archive_info:
            print("✓ Archive created successfully")
            print(f"  Filename: {archive_info['filename']}")
            print(f"  Original size: {archive_info['size']} bytes")
            print(f"  Compressed size: {archive_info['compress_size']} bytes")
            print(f"  Compression ratio: {archive_info['compression_ratio']}%\n")
    except Exception as e:
        print(f"✗ Error archiving file: {e}\n")


def show_all_results():
    """Display all analysis results."""
    text = get_text()
    if text is None:
        return

    print("\n" + "=" * 60)
    print("COMPLETE TEXT ANALYSIS (Variant 9)")
    print("=" * 60)

    print("\n" + "▶ " + "SENTENCE ANALYSIS".center(56))
    analyze_sentences()

    print("\n" + "▶ " + "WORD ANALYSIS".center(56))
    analyze_words()

    print("\n" + "▶ " + "DATE EXTRACTION".center(56))
    extract_dates()

    print("\n" + "▶ " + "SMILEY ANALYSIS".center(56))
    analyze_smileys()


def print_description():
    """Display program description."""
    print(DESCRIPTION)


def task2():
    """
    Main function to start Task 2.
    Runs text analysis interactive menu.
    """
    print_description()

    while True:
        display_menu()

        try:
            choice = input_data("Choose an option: ", int, 0, 6)

            match choice:
                case 1:
                    analyze_sentences()
                case 2:
                    analyze_words()
                case 3:
                    analyze_smileys()
                case 4:
                    extract_dates()
                case 5:
                    archive_results()
                case 6:
                    show_all_results()
                case 0:
                    print("\n✓ Returning to main menu...\n")
                    break

        except KeyboardInterrupt:
            print("\n\n✓ Program interrupted by user")
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}")
