"""
state.py
--------
Handles all persistence: reading from and writing the JSON state file.
"""

import json
import os

import streamlit as st

from quiz.config import STATE_FILE, TEAMS, TIERS, CATEGORIES, MAX_CE


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
    usernames_data = data.get("usernames", {})
    usernames = {team: usernames_data.get(team, "") for team in TEAMS}
    death_order = []
    for team in data.get("death_order", []):
        if team in TEAMS and data["ce"].get(team, 0) <= 0 and team not in death_order:
            death_order.append(team)
    death_order.extend(
        team
        for team in TEAMS
        if data["ce"].get(team, 0) <= 0 and team not in death_order
    )
    return {
        "ce": data["ce"],
        "board": fixed_board,
        "items": items_data,
        "usernames": usernames,
        "death_order": death_order,
    }


def save_state() -> None:
    state = {
        "ce": st.session_state.ce,
        "board": st.session_state.board,
        "items": st.session_state["items"], # FIXED bracket notation!
        "usernames": st.session_state["usernames"],
        "death_order": st.session_state["death_order"],
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def init_session_state() -> None:
    loaded = load_state()

    if "ce" not in st.session_state:
        st.session_state.ce = loaded["ce"] if loaded else {team: MAX_CE for team in TEAMS}

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

    if "usernames" not in st.session_state:
        st.session_state["usernames"] = (
            loaded["usernames"]
            if loaded
            else {team: "" for team in TEAMS}
        )

    if "death_order" not in st.session_state:
        st.session_state["death_order"] = loaded["death_order"] if loaded else []

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
            st.session_state.ce = loaded["ce"]
            st.session_state.board = loaded["board"]
            st.session_state["items"] = loaded["items"] # FIXED bracket notation!
            st.session_state["usernames"] = loaded["usernames"]
            st.session_state["death_order"] = loaded["death_order"]
        st.rerun()


def update_team_ce(team: str, new_ce: int) -> None:
    new_ce = max(0, new_ce)
    was_alive = st.session_state.ce[team] > 0
    st.session_state.ce[team] = new_ce

    if was_alive and new_ce <= 0:
        if team not in st.session_state["death_order"]:
            st.session_state["death_order"].append(team)
    elif new_ce > 0 and team in st.session_state["death_order"]:
        st.session_state["death_order"].remove(team)


def get_ranked_teams() -> list[str]:
    alive = [team for team in TEAMS if st.session_state.ce[team] > 0]
    alive_sorted = sorted(
        alive,
        key=lambda team: st.session_state.ce[team],
        reverse=True,
    )
    dead_sorted = list(reversed(st.session_state["death_order"]))
    return alive_sorted + dead_sorted