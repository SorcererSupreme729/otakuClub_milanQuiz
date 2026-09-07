"""
state.py
--------
Handles all persistence: reading from and writing the JSON state file.
"""

import json
import os

import streamlit as st

from quiz.config import STATE_FILE, TEAMS, TIERS, CATEGORIES, MAX_HP


def load_state() -> dict | None:
    """
    Reads the saved game state from the JSON file if it exists.

    JSON stores all keys as strings, so integer tier keys need to be
    converted back to ints on load.

    Returns:
        A dict with "hp" and "board" keys, or None if no save file exists.
    """
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    # JSON converts integer keys to strings — restore them as ints.
    fixed_board = {
        cat: {int(tier): val for tier, val in tiers.items()}
        for cat, tiers in data["board"].items()
    }
    return {"hp": data["hp"], "board": fixed_board}


def save_state() -> None:
    """
    Saves the current session state (HP and board) to the JSON file.
    Uses indent=4 for human-readable output.
    """
    state = {
        "hp": st.session_state.hp,
        "board": st.session_state.board,
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def init_session_state() -> None:
    """
    Initialises all required session_state keys on first run.
    Loads persisted state from disk if available; otherwise uses fresh defaults.
    """
    loaded = load_state()

    if "hp" not in st.session_state:
        st.session_state.hp = loaded["hp"] if loaded else {team: MAX_HP for team in TEAMS}

    if "board" not in st.session_state:
        st.session_state.board = (
            loaded["board"]
            if loaded
            else {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}
        )

    # mode: None = login screen, "admin", "hoster", or a team name
    if "mode" not in st.session_state:
        st.session_state.mode = None

    # Seed the mtime tracker on first load
    if "state_mtime" not in st.session_state:
        st.session_state.state_mtime = (
            os.path.getmtime(STATE_FILE) if os.path.exists(STATE_FILE) else 0.0
        )


def check_for_external_updates() -> None:
    """
    Detects whether the state file was saved by another browser session
    (e.g. admin marking a tile done or adjusting HP) and, if so, reloads
    the state and triggers a full page rerun so every tab stays in sync.

    Call this once per page render, before drawing any UI.
    """
    if not os.path.exists(STATE_FILE):
        return

    current_mtime = os.path.getmtime(STATE_FILE)
    if current_mtime != st.session_state.get("state_mtime", 0.0):
        st.session_state.state_mtime = current_mtime
        loaded = load_state()
        if loaded:
            st.session_state.hp = loaded["hp"]
            st.session_state.board = loaded["board"]
        st.rerun()

