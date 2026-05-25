"""
Module: input_handlers.py
Purpose: Functions to obtain text input.
Lab: 3
Version: 1.0
Developer: Rodion Shcherbak
"""

def predefined_text() -> str:
    """Return the predefined text from the assignment."""
    return ("So she was considering in her own mind, as well as she could, for the hot day "
            "made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain "
            "would be worth the trouble of getting up and picking the daisies, when suddenly "
            "a White Rabbit with pink eyes ran close by her.")

def user_input_text() -> str:
    """Read a line of text from the user."""
    return input("Enter your own string: ")