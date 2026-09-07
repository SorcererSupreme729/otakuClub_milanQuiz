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

# ── Teams ────────────────────────────────────────────────────────────────────
TEAMS = [
    "Team 1", "Team 2", "Team 3", "Team 4",
    "Team 5", "Team 6", "Team 7", "Team 8",
]

MAX_HP = 4000

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
