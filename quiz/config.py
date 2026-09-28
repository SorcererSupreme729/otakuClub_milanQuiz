"""
config.py
---------
All game constants and credentials in one place.
Changing a value here propagates everywhere automatically.
"""

from pathlib import Path

# ── File Paths ──────────────────────────────────────────────────────────────
# Resolved relative to the project root (parent of the quiz/ package dir).
# This fixes the hard-coded macOS path bug in the original script.
_PROJECT_ROOT = Path(__file__).parent.parent

STATE_FILE = str(_PROJECT_ROOT / "milan_quiz_state.json")
THEME_IMAGE = str(_PROJECT_ROOT / "Theme.png")

# ── Board Layout ─────────────────────────────────────────────────────────────
CATEGORIES = [
    "Quotes",
    "Pee Pee poo poo hard",
    "I can't read",
    "Where is Zoro?",
    "Where are the pixels?????",
    "Truck Kun's hitlist",
    "Inumaki's Spotify playlist",
    "Chika Fujiwara photo",
    "Japanese Culture",
]

TIERS = [200, 400, 600, 800, 1000, 1500]

# Edit only this list to choose which category/tier pairs are bonus questions.
BONUS_QUESTIONS = [
    ("Quotes", 400), ("Quotes", 800),
    ("I can't read", 400), ("I can't read", 800),
    ("Where is Zoro?", 600), ("Where is Zoro?", 1000),
    ("Where are the pixels?????", 400), ("Where are the pixels?????", 800),
    ("Inumaki's Spotify playlist", 600), ("Inumaki's Spotify playlist", 1000),
    ("Japanese Culture", 600), ("Japanese Culture", 1000),
    ("Pee Pee poo poo hard", 1000),
    ("Truck Kun's hitlist", 1000),
    ("Chika Fujiwara photo", 800),
]


def is_bonus(category: str, tier: int) -> bool:
    """Return whether a category/tier pair is configured as a bonus question."""
    category_target = str(category).strip().casefold()

    for bonus_category, bonus_tier in BONUS_QUESTIONS:
        if str(bonus_category).strip().casefold() != category_target:
            continue

        try:
            if int(bonus_tier) == int(tier):
                return True
        except (TypeError, ValueError):
            if str(bonus_tier).strip() == str(tier).strip():
                return True

    return False

# ── Teams ────────────────────────────────────────────────────────────────────
TEAMS = [
    "Team 1", "Team 2", "Team 3", "Team 4",
    "Team 5", "Team 6", "Team 7", "Team 8",
]

MAX_CE = 4000

TEAM_COLORS = [
    "#8B0000", "#4A0E0E", "#B7202E", "#6E1414",
    "#9E1B1B", "#701212", "#A62639", "#5C0F0F",
]

# ── Credentials ──────────────────────────────────────────────────────────────
ADMIN_PASSWORD = "goatakuclub@milan2026"
HOSTER_PASSWORD = "open@thegates2026"

TEAM_PASSWORDS = {
    "Team 1": "hollow@purple2026",
    "Team 2": "black@flash2026",
    "Team 3": "ten@shadows2026",
    "Team 4": "infinite@void2026",
    "Team 5": "malevolent@shrine26",
    "Team 6": "idle@death2026",
    "Team 7": "heavenly@pact2026",
    "Team 8": "cursed@speech2026",
}
