# ---------------------------------------------------------
# Lab Work №4 - Task 2 (Variant 26)
# Module: task2.py
# Purpose: Main interface for text analysis system
# Version: 1.0
# Developer: Shcherbak Rodion
# Date of Development: 2026-04-29
# ---------------------------------------------------------

import os

from task2.analyzer import SentenceAnalyzer, WordAnalyzer, SmileyAnalyzer
from task2.archiver import archive_file, save_results_to_file

DESCRIPTION = """
╔══════════════════════════════════════════════════════════════════════╗
║                   Text Analysis System (Variant 26)                   ║
║                                                                       ║
║  This program analyzes text using regular expressions:                ║
║  ✓ Count sentences (total, declarative, interrogative, imperative)   ║
║  ✓ Calculate average sentence length (characters)                    ║
║  ✓ Calculate average word length                                     ║
║  ✓ Extract all uppercase English letters                             ║
║  ✓ Replace pattern "р...рb...bc...c" with "ddd"                      ║
║  ✓ Count words with length < 5                                       ║
║  ✓ Find shortest word ending with 'd'                                ║
║  ✓ Sort all words by length descending                               ║
║  ✓ Count valid smileys                                               ║
║  ✓ Archive results in ZIP                                            ║
╚══════════════════════════════════════════════════════════════════════╝
"""


def display_menu():
    """Display main analysis menu."""
    print("\n" + "=" * 60)
    print("Text Analyzer Menu (Variant 26)")
    print("=" * 60)
    print("1.  Analyze sentences")
    print("2.  Analyze words")
    print("3.  Count smileys")
    print("4.  Run complete analysis")
    print("5.  Archive and compress results")
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

    print(f"\n Total sentences:                 {result['total']}")
    print(f"\n Sentence types:")
    print(f"   • Declarative (.):              {result['declarative']}")
    print(f"   • Interrogative (?):            {result['interrogative']}")
    print(f"   • Imperative (!):               {result['imperative']}")
    print(f"\n Average sentence length:         {result['avg_sentence_chars']} characters")
    print(f" Average word length:              {result['avg_word_length']} characters\n")


def analyze_words():
    """Analyze words with variant 26 specific tasks."""
    text = get_text()
    if text is None:
        return

    print("\n" + "-" * 60)
    print("Word Analysis (Variant 26)")
    print("-" * 60)

    result = WordAnalyzer(text).process()

    print(f"\n Total words:                     {result['word_count']}")

    # 1. Uppercase English letters
    print(f"\n 1. Uppercase English letters found:")
    if result['uppercase_letters']:
        print(f"    Letters: {', '.join(result['uppercase_letters'])}")
        print(f"    Total count: {result['uppercase_count']}")
    else:
        print("    (no uppercase English letters found)")

    # 2. Pattern replacement preview
    print(f"\n 2. Pattern 'р...рb...bc...c' → 'ddd':")
    print(f"    Original text preview: {text[:100]}...")
    print(f"    After replacement: {result['text_after_replacement'][:100]}...")

    # 3. Words with length < 5
    print(f"\n 3. Words with length < 5:")
    print(f"    Count: {result['short_words_count']}")
    if result['short_words']:
        print(f"    Examples: {', '.join(result['short_words'][:10])}")

    # 4. Shortest word ending with 'd'
    print(f"\n 4. Shortest word ending with 'd':")
    if result['shortest_word_d']:
        print(f"    Word: '{result['shortest_word_d']}' (length: {len(result['shortest_word_d'])})")
    else:
        print("    (no words ending with 'd' found)")

    # 5. Words sorted by length descending
    print(f"\n 5. Words sorted by length descending:")
    if result['words_by_length_desc']:
        print(f"    First 15: {', '.join(result['words_by_length_desc'][:15])}")
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

    print(f"\n Total valid smileys:             {result['smiley_count']}")

    if result['smileys']:
        print(f"\n Valid smileys found:")
        for smiley in result['smileys'][:15]:
            print(f"   • {smiley}")
        if len(result['smileys']) > 15:
            print(f"   ... and {len(result['smileys']) - 15} more")
    else:
        print("\n (no valid smileys found)")


def run_complete_analysis():
    """Run all analyses and display complete results."""
    text = get_text()
    if text is None:
        return

    print("\n" + "=" * 60)
    print("COMPLETE TEXT ANALYSIS (Variant 26)")
    print("=" * 60)

    # Sentence analysis
    sentence_result = SentenceAnalyzer(text).process()
    print("\n▶ SENTENCE STATISTICS".center(58))
    print("-" * 60)
    print(f"  Total sentences:                    {sentence_result['total']}")
    print(f"  Declarative (.):                    {sentence_result['declarative']}")
    print(f"  Interrogative (?):                  {sentence_result['interrogative']}")
    print(f"  Imperative (!):                     {sentence_result['imperative']}")
    print(f"  Average sentence length (chars):    {sentence_result['avg_sentence_chars']}")
    print(f"  Average word length:                {sentence_result['avg_word_length']}")

    # Word analysis
    word_result = WordAnalyzer(text).process()
    print("\n▶ WORD ANALYSIS".center(58))
    print("-" * 60)
    print(f"  Total words:                        {word_result['word_count']}")
    print(f"  Uppercase English letters:          {', '.join(word_result['uppercase_letters']) if word_result['uppercase_letters'] else 'none'}")
    print(f"  Words with length < 5:              {word_result['short_words_count']}")
    print(f"  Shortest word ending with 'd':      '{word_result['shortest_word_d']}'" if word_result['shortest_word_d'] else "  Shortest word ending with 'd':      none")

    # Smiley analysis
    smiley_result = SmileyAnalyzer(text).process()
    print("\n▶ SMILEY STATISTICS".center(58))
    print("-" * 60)
    print(f"  Total valid smileys:                {smiley_result['smiley_count']}")
    if smiley_result['smileys'][:5]:
        print(f"  Examples:                          {', '.join(smiley_result['smileys'][:5])}")

    print("\n" + "=" * 60 + "\n")


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

    # Build results report
    results = []
    results.append("=" * 70)
    results.append("TEXT ANALYSIS RESULTS (Variant 26)".center(70))
    results.append("=" * 70)
    results.append("")
    results.append("1. SENTENCE ANALYSIS")
    results.append("-" * 70)
    results.append(f"   Total sentences:                           {sentence_result['total']}")
    results.append(f"   Declarative sentences (.):                 {sentence_result['declarative']}")
    results.append(f"   Interrogative sentences (?):               {sentence_result['interrogative']}")
    results.append(f"   Imperative sentences (!):                  {sentence_result['imperative']}")
    results.append(f"   Average sentence length (characters):      {sentence_result['avg_sentence_chars']}")
    results.append(f"   Average word length:                       {sentence_result['avg_word_length']}")
    results.append("")
    results.append("2. WORD ANALYSIS")
    results.append("-" * 70)
    results.append(f"   Total words:                               {word_result['word_count']}")
    results.append(f"   Uppercase English letters found:           {', '.join(word_result['uppercase_letters']) if word_result['uppercase_letters'] else 'none'}")
    results.append(f"   Uppercase letters total count:             {word_result['uppercase_count']}")
    results.append("")
    results.append("3. PATTERN REPLACEMENT")
    results.append("-" * 70)
    results.append(f"   Original text preview:")
    results.append(f"      {text[:200]}...")
    results.append(f"   After replacing 'р...рb...bc...c' with 'ddd':")
    results.append(f"      {word_result['text_after_replacement'][:200]}...")
    results.append("")
    results.append("4. WORD STATISTICS")
    results.append("-" * 70)
    results.append(f"   Words with length < 5:                    {word_result['short_words_count']}")
    if word_result['short_words']:
        results.append(f"   Examples: {', '.join(word_result['short_words'][:15])}")
    results.append(f"   Shortest word ending with 'd':            '{word_result['shortest_word_d']}'" if word_result['shortest_word_d'] else "   Shortest word ending with 'd':            none")
    results.append("")
    results.append("5. WORDS SORTED BY LENGTH (DESCENDING)")
    results.append("-" * 70)
    if word_result['words_by_length_desc']:
        results.append(f"   First 20: {', '.join(word_result['words_by_length_desc'][:20])}")
    results.append("")
    results.append("6. SMILEY ANALYSIS")
    results.append("-" * 70)
    results.append(f"   Total valid smileys:                       {smiley_result['smiley_count']}")
    if smiley_result['smileys']:
        results.append(f"   Smileys found: {', '.join(smiley_result['smileys'][:15])}")
    results.append("")
    results.append("=" * 70)
    results.append("End of Analysis Report")
    results.append("=" * 70)

    result_file = get_path_to_file("result.txt")
    save_results_to_file(result_file, results)

    try:
        archive_info = archive_file(result_file)
        if archive_info:
            print("\n✓ Archive created successfully")
            print(f"  Filename: {archive_info['filename']}")
            print(f"  Original size: {archive_info['size']} bytes")
            print(f"  Compressed size: {archive_info['compress_size']} bytes")
            print(f"  Compression ratio: {archive_info['compression_ratio']}%\n")
    except Exception as e:
        print(f"✗ Error archiving file: {e}\n")


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
            choice = input("Choose an option (0-5): ").strip()

            if not choice:
                continue

            choice = int(choice)

            if choice == 0:
                print("\n✓ Exiting program...\n")
                break
            elif choice == 1:
                analyze_sentences()
            elif choice == 2:
                analyze_words()
            elif choice == 3:
                analyze_smileys()
            elif choice == 4:
                run_complete_analysis()
            elif choice == 5:
                archive_results()
            else:
                print("✗ Invalid choice. Please enter 0-5\n")

        except ValueError:
            print("✗ Please enter a valid number\n")
        except KeyboardInterrupt:
            print("\n\n✓ Program interrupted by user")
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}")


if __name__ == "__main__":
    task2()