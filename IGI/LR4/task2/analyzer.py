# ---------------------------------------------------------
# Lab Work №4 - Task 2 (Variant 9)
# Module: analyzer.py
# Purpose: Text analysis using regular expressions
# Version: 1.0
# Developer: Vodnev Kirill
# Date of Development: 2026-03-01
# ---------------------------------------------------------

import re

class BaseAnalyzer:
    """Baseclass for all text processors."""

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
                - avg_sentence_length: average sentence length in words
                - avg_sentence_chars: average sentence length in characters (words only)
        """
        sentences = re.findall(r'[^.!?]+[.!?]', self.text)

        declarative = len(re.findall(r'[^.!?]+\.', self.text))
        interrogative = len(re.findall(r'[^.!?]+\?', self.text))
        imperative = len(re.findall(r'[^.!?]+!', self.text))

        if sentences:
            total_words = sum(len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences)
            avg_sentence_len = total_words / len(sentences)

            total_chars = sum(
                len(''.join(re.findall(r'\b\w+\b', sentence)))
                for sentence in sentences
            )
            avg_sentence_chars = total_chars / len(sentences)
        else:
            avg_sentence_len = 0
            avg_sentence_chars = 0

        return {
            "total": len(sentences),
            "declarative": declarative,
            "interrogative": interrogative,
            "imperative": imperative,
            "avg_sentence_length": round(avg_sentence_len, 2),
            "avg_sentence_chars": round(avg_sentence_chars, 2)
        }


class WordAnalyzer(BaseAnalyzer):
    """Analyzes word statistics from text."""

    def process(self) -> dict:
        """
        Process word statistics and variant-specific analysis.

        Returns:
            dict: Word analysis results
                - word_count: total number of words
                - avg_word_length: average word length in characters
                - words_vowel_ending_consonant_penultimate: words ending with vowel,
                  penultimate letter is consonant
                - lowercase_count: total lowercase letters in entire text
                - last_word_with_i: last word containing 'i' and its position
                - text_without_i_words: text with words starting with 'i' removed
                - dates: list of dates in format DD-MM-YYYY
        """
        words = re.findall(r'\b\w+\b', self.text)

        avg_word_len = sum(len(word) for word in words) / len(words) if words else 0

        vowel_cons_words = [
            word for word in words
            if len(word) >= 2 and
               word[-1].lower() in 'aeiou' and
               word[-2].lower() not in 'aeiou' and
               word[-2].isalpha()
        ]
        lowercase_count = sum(1 for char in self.text if char.islower())

        last_i_word = None
        last_i_index = None
        for idx, word in enumerate(words, 1):
            if 'i' in word.lower():
                last_i_word = word
                last_i_index = idx

        text_without_i = re.sub(r'\b[iI]\w*\b', '', self.text)
        text_without_i = re.sub(r'\s+', ' ', text_without_i).strip()

        dates = re.findall(r'\b(\d{2}-\d{2}-\d{4})\b', self.text)

        return {
            "word_count": len(words),
            "avg_word_length": round(avg_word_len, 2),
            "words_vowel_ending_consonant_penultimate": vowel_cons_words,
            "lowercase_count": lowercase_count,
            "last_word_with_i": last_i_word,
            "last_word_with_i_index": last_i_index,
            "text_without_i_words": text_without_i,
            "dates": dates
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
        Process smileys according to rules:
        - First character: ':' or ';' (exactly one)
        - Middle: '-' (zero or more times)
        - End: one or more identical brackets from set: ( ) [ ]

        Returns:
            dict: Smiley analysis results
                - smiley_count: total number of valid smileys
                - smileys: list of found valid smileys
                - invalid_candidates: sequences that look like smileys but are invalid
        """

        full_smileys = re.findall(r'[:;]-*[()[\]]+', self.text)

        valid_smileys = []
        for smiley in full_smileys:
            if len(smiley) >= 2:
                dash_end = smiley.find('-')
                if dash_end == -1:
                    bracket_part = smiley[1:]
                else:
                    dash_end = smiley.rfind('-') + 1
                    bracket_part = smiley[dash_end:]

                if bracket_part and all(b == bracket_part[0] for b in bracket_part):
                    valid_smileys.append(smiley)

        return {
            "smiley_count": len(valid_smileys),
            "smileys": valid_smileys
        }


class DateAnalyzer(BaseAnalyzer):
    """Extracts dates from text in format DD-MM-YYYY."""

    def process(self) -> dict:
        """
        Extract all dates in format DD-MM-YYYY.

        Returns:
            dict: Date analysis results
                - date_count: total number of dates
                - dates: list of extracted dates
        """
        dates = re.findall(r'\b(\d{2}-\d{2}-\d{4})\b', self.text)

        return {
            "date_count": len(dates),
            "dates": dates
        }