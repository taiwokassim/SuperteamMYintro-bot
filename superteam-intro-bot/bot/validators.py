"""
validators.py

Contains validation logic for intro submissions.
Ensures:
- Minimum line count
- Minimum character count
- Minimum word count
- Prevents spammy repeated characters
"""

import re


def is_valid_intro(text: str) -> bool:
    """
    Validates whether a user's intro meets minimum quality requirements.

    Requirements:
    - At least 3 non-empty lines
    - At least 150 characters
    - At least 25 words
    - No excessive repeated characters
    """

    if not text:
        return False

    stripped = text.strip()

    # Minimum character requirement
    if len(stripped) < 150:
        return False

    # Minimum non-empty lines
    lines = [line for line in stripped.split("\n") if line.strip()]
    if len(lines) < 3:
        return False

    # Minimum word count
    words = stripped.split()
    if len(words) < 25:
        return False

    # Prevent repeated character spam (e.g., "aaaaaaa")
    if re.search(r"(.)\1{9,}", stripped):
        return False

    return True

    