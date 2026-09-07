"""
app.py
------
Entry point for the Milan Quiz: Culling Game Streamlit application.

Run with:
    streamlit run app.py

This file is intentionally thin — it only wires together the modules
from the quiz/ package. All business logic lives in those modules.
"""

import streamlit as st

# ── Must be the very first Streamlit call ─────────────────────────────────────
st.set_page_config(
    page_title="Milan Quiz: Anime Jeopardy",
    layout="wide",
    page_icon="⚔️",
)

# ── Internal imports (after page config) ─────────────────────────────────────
from quiz.config import (
    TEAMS,
    ADMIN_PASSWORD,
    TEAM_PASSWORDS,
    THEME_IMAGE,
)
from quiz.state import init_session_state, check_for_external_updates
from quiz.styles import inject_css
from quiz.sidebar import render_sidebar
from quiz.board import render_board

# ── 1. Inject CSS ─────────────────────────────────────────────────────────────
inject_css()

# ── 2. Initialise session state (loads saved game from disk if available) ─────
init_session_state()

# ── 3. Login Gate ─────────────────────────────────────────────────────────────
if st.session_state.mode is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:2.2rem !important; font-family: Cinzel, serif; "
        "color: #b7202e; text-align: center; margin-bottom: 20px;'>"
        "Select Your Identity</h1>",
        unsafe_allow_html=True,
    )

    _left, mid, _right = st.columns([1, 1.5, 1])
    with mid:
        try:
            st.image(THEME_IMAGE, use_container_width=True)
        except Exception:
            st.markdown(
                "<div style='text-align: center; color: #8a4a4a; padding: 20px; "
                "border: 1px dashed #8a4a4a; margin-bottom: 15px;'>"
                "[ Culling Game Image Not Found — Place Theme.png in the project folder ]"
                "</div>",
                unsafe_allow_html=True,
            )

        roles = ["Hoster", "Colony Overseer (Admin)"] + TEAMS
        choice = st.selectbox("Who are you?", roles, label_visibility="collapsed")

        if choice == "Hoster":
            if st.button("Enter the Culling Game", use_container_width=True):
                st.session_state.mode = "hoster"
                st.rerun()
        else:
            pw = st.text_input("Enter Password", type="password")
            if st.button("Authenticate", use_container_width=True):
                if choice == "Colony Overseer (Admin)" and pw == ADMIN_PASSWORD:
                    st.session_state.mode = "admin"
                    st.rerun()
                elif choice in TEAMS and pw == TEAM_PASSWORDS.get(choice):
                    st.session_state.mode = choice
                    st.rerun()
                else:
                    st.error("Incorrect Cursed Energy Signature (Wrong Password).")

    st.stop()

# ── 4. Real-time sync: detect changes saved by other sessions ─────────────────
# Runs on every page interaction. For fully automatic polling use the
# auto-refresh fragment below (fires every 3 s in non-admin sessions).
check_for_external_updates()

# ── 5. Auto-refresh fragment — keeps non-admin tabs in sync automatically ─────
@st.fragment(run_every=3)
def _sync_watcher() -> None:
    """
    Lightweight fragment that polls the state file every 3 seconds.
    If the mtime changed (another session saved), it reloads session state
    and triggers a full page rerun so every open tab stays live.
    """
    import os
    from quiz.config import STATE_FILE
    from quiz.state import load_state

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

# Only run the auto-poller for non-admin sessions to avoid fighting with
# the admin's own saves triggering double reruns.
if st.session_state.mode != "admin":
    _sync_watcher()

# ── 6. Main App (post-login) ──────────────────────────────────────────────────
render_sidebar()
render_board()
