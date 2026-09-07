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
    if not os.path.exists(STATE_FILE):
        return None

    with open(STATE_FILE, "r") as f:
        data = json.load(f)

    fixed_board = {
        cat: {int(tier): val for tier, val in tiers.items()}
        for cat, tiers in data["board"].items()
    }
    
    items_data = data.get("items", {team: [] for team in TEAMS})
    return {"hp": data["hp"], "board": fixed_board, "items": items_data}


def save_state() -> None:
    state = {
        "hp": st.session_state.hp,
        "board": st.session_state.board,
        "items": st.session_state["items"], # FIXED bracket notation!
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def init_session_state() -> None:
    loaded = load_state()

    if "hp" not in st.session_state:
        st.session_state.hp = loaded["hp"] if loaded else {team: MAX_HP for team in TEAMS}

    if "board" not in st.session_state:
        st.session_state.board = (
            loaded["board"]
            if loaded
            else {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}
        )
        
    if "items" not in st.session_state:
        st.session_state["items"] = ( # FIXED bracket notation!
            loaded["items"] 
            if loaded 
            else {team: [] for team in TEAMS}
        )

    if "mode" not in st.session_state:
        st.session_state.mode = None

    if "state_mtime" not in st.session_state:
        st.session_state.state_mtime = (
            os.path.getmtime(STATE_FILE) if os.path.exists(STATE_FILE) else 0.0
        )


def check_for_external_updates() -> None:
    if not os.path.exists(STATE_FILE):
        return

    current_mtime = os.path.getmtime(STATE_FILE)
    if current_mtime != st.session_state.get("state_mtime", 0.0):
        st.session_state.state_mtime = current_mtime
        loaded = load_state()
        if loaded:
            st.session_state.hp = loaded["hp"]
            st.session_state.board = loaded["board"]
            st.session_state["items"] = loaded["items"] # FIXED bracket notation!
        st.rerun()