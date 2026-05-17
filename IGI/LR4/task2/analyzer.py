# ---------------------------------------------------------
# Lab Work №4 - Task 2 (Variant 26)
# Module: analyzer.py
# Purpose: Text analysis using regular expressions
# Version: 1.0
# Developer: Student
# Date of Development: 2026-05-17
# ---------------------------------------------------------

import re


class BaseAnalyzer:
    """Base class for all text processors."""

    def __init__(self, text: str):
        """
        Initialize analyzer with text.

        Args:
            text (str): The text to be analyzed.
        """
        self.text = text

    def process(self):
        """
        Process the text. Must be overridden in subclass.

        Raises:
            NotImplementedError: If not overridden.
        """
        raise NotImplementedError("Must be overridden in subclass.")


class SentenceAnalyzer(BaseAnalyzer):
    """Analyzes sentence statistics from text."""

    def process(self) -> dict:
        """
        Process sentence statistics.

        Returns:
            dict: Sentence analysis results
                - total: total number of sentences
                - declarative: sentences ending with '.'
                - interrogative: sentences ending with '?'
                - imperative: sentences ending with '!'
                - avg_sentence_length: average sentence length in characters (words only)
                - avg_word_length: average word length in characters
        """
        # Split text into sentences
        sentences = re.findall(r'[^.!?]+[.!?]', self.text)

        # Count sentence types
        declarative = len(re.findall(r'[^.!?]+\.', self.text))
        interrogative = len(re.findall(r'[^.!?]+\?', self.text))
        imperative = len(re.findall(r'[^.!?]+!', self.text))

        # Extract all words
        words = re.findall(r'\b\w+\b', self.text)

        # Calculate average sentence length in characters (words only, no spaces/punctuation)
        if sentences:
            total_chars = sum(
                len(''.join(re.findall(r'\b\w+\b', sentence)))
                for sentence in sentences
            )
            avg_sentence_chars = total_chars / len(sentences)
        else:
            avg_sentence_chars = 0

        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0

        return {
            "total": len(sentences),
            "declarative": declarative,
            "interrogative": interrogative,
            "imperative": imperative,
            "avg_sentence_chars": round(avg_sentence_chars, 2),
            "avg_word_length": round(avg_word_length, 2)
        }


class WordAnalyzer(BaseAnalyzer):
    """Analyzes word statistics from text for variant 26."""

    def process(self) -> dict:
        """
        Process word statistics and variant-specific analysis.

        Tasks:
        1. Count uppercase English letters
        2. Replace pattern "р...рb...bc...c" with "ddd"
        3. Count words with length < 5
        4. Find shortest word ending with 'd'
        5. Sort all words by length descending

        Returns:
            dict: Word analysis results
        """
        # Extract all words
        words = re.findall(r'\b\w+\b', self.text)

        # 1. Find all uppercase English letters (A-Z)
        uppercase_letters = re.findall(r'[A-Z]', self.text)
        unique_uppercase = sorted(set(uppercase_letters))

        # 2. Replace pattern "р...рb...bc...c" with "ddd"
        # Pattern: р (one or more), then b (two or more), then c (one or more)
        # Note: Using Cyrillic 'р' as specified in the task
        pattern = r'р+b{2,}c+'
        text_after_replacement = re.sub(pattern, 'ddd', self.text)

        # 3. Count words with length < 5
        short_words = [word for word in words if len(word) < 5]
        short_words_count = len(short_words)

        # 4. Find shortest word ending with 'd'
        words_ending_with_d = [word for word in words if word.endswith('d')]
        shortest_word_d = min(words_ending_with_d, key=len) if words_ending_with_d else None

        # 5. Sort all words by length descending
        words_by_length_desc = sorted(words, key=len, reverse=True)

        return {
            "word_count": len(words),
            "uppercase_letters": unique_uppercase,
            "uppercase_count": len(uppercase_letters),
            "text_after_replacement": text_after_replacement,
            "short_words_count": short_words_count,
            "short_words": short_words[:20],  # first 20 for display
            "shortest_word_d": shortest_word_d,
            "words_by_length_desc": words_by_length_desc[:30]  # first 30 for display
        }


class SmileyAnalyzer(BaseAnalyzer):
    """
    Finds all valid smileys in the text.

    Smiley rules:
    - First character: ':' or ';' (exactly one)
    - Middle: '-' (zero or more times)
    - End: one or more identical brackets from set: ( ) [ ]
    - No other characters inside
    """

    def process(self) -> dict:
        """
        Process smileys according to rules.

        Returns:
            dict: Smiley analysis results
                - smiley_count: total number of valid smileys
                - smileys: list of found valid smileys
        """
        # Find all potential smileys
        full_smileys = re.findall(r'[:;]-*[()\[\]]+', self.text)

        valid_smileys = []
        for smiley in full_smileys:
            if len(smiley) >= 2:
                # Find where brackets start
                bracket_start = 1
                for i in range(1, len(smiley)):
                    if smiley[i] == '-':
                        continue
                    bracket_start = i
                    break

                bracket_part = smiley[bracket_start:]

                # Check if all brackets are identical
                if bracket_part and all(b == bracket_part[0] for b in bracket_part):
                    valid_smileys.append(smiley)

        return {
            "smiley_count": len(valid_smileys),
            "smileys": valid_smileys
        }