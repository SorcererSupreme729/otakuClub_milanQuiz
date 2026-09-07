"""
questions.py
------------
Loads the question/answer content database and provides lookup helpers.
"""

import json
import os
import streamlit as st

QUESTIONS_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "culling_game_questions.json")
)


# @st.cache_data
def load_questions(path: str = QUESTIONS_PATH) -> dict:
    """
    Loads the quiz content database from disk once per session.

    Args:
        path: Path to the questions JSON file.

    Returns:
        Parsed JSON as a dict.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_question(data: dict, category: str, tier: int) -> dict | None:
    """
    Finds the question dict matching a category name and HP tier.
    Matching is case-insensitive and whitespace-tolerant on the category
    name, and tolerant of int/str mismatches on the tier value.

    Args:
        data:     The loaded questions database (from load_questions).
        category: Category column label, e.g. "QUOTES".
        tier:     HP value for the tile, e.g. 200.

    Returns:
        The matching question dict, or None if not found.
    """
    cat_target = str(category).strip().casefold()

    for cat in data.get("categories", []):
        cat_name = str(cat.get("name", "")).strip().casefold()
        if cat_name != cat_target:
            continue

        for q in cat.get("questions", []):
            hp = q.get("hp_value")
            try:
                if int(hp) == int(tier):
                    return q
            except (TypeError, ValueError):
                if str(hp).strip() == str(tier).strip():
                    return q

    return None