"""
logic.py — Response engine for Nova Chatbot.

Flow:
  1. Normalise raw input (lowercase, strip punctuation, expand contractions)
  2. Walk COMPILED_RULES in priority order
  3. Return a random response from the first matching rule
  4. Resolve sentinel tokens (__TIME__, __DATE__)
  5. Fall back to a random FALLBACK_RESPONSES entry
"""

import random
import re
from datetime import datetime
from chatbot.patterns import COMPILED_RULES, FALLBACK_RESPONSES


def normalise(text: str) -> str:
    """Clean and standardise user input for reliable regex matching."""
    text = text.strip().lower()

    # Expand contractions with strict word boundaries
    contractions = {
        r"\bwhat's\b": "what is",
        r"\bwho're\b": "who are",
        r"\bhow're\b": "how are",
        r"\bi'm\b":    "i am",
        r"\bcan't\b":  "cannot",
        r"\bwon't\b":  "will not",
        r"\bdon't\b":  "do not",
        r"\bdidn't\b": "did not",
        r"\byou're\b": "you are",
    }
    for pat, rep in contractions.items():
        text = re.sub(pat, rep, text)

    # Strip everything except letters, digits, spaces
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def resolve(response: str) -> str:
    """Replace sentinel tokens with live values."""
    if response == "__TIME__":
        now = datetime.now()
        return f"🕐 The current time is {now.strftime('%I:%M %p')} (server time)."
    if response == "__DATE__":
        now = datetime.now()
        return f"📅 Today is {now.strftime('%A, %d %B %Y')}."
    return response


def generate_response(user_input: str) -> str:
    """Main entry point called by app.py /chat endpoint."""
    clean = normalise(user_input)
    for rule in COMPILED_RULES:
        for pattern in rule["patterns"]:
            if pattern.search(clean):
                return resolve(random.choice(rule["responses"]))
    return random.choice(FALLBACK_RESPONSES)