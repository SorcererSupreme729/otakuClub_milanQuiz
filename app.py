"""
app.py
------
Entry point for the Milan Quiz: Culling Game Streamlit application.
"""

import re

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
    HOSTER_PASSWORD,
    TEAM_PASSWORDS,
    THEME_IMAGE,
)
from quiz.state import (
    check_for_external_updates,
    get_ranked_teams,
    init_session_state,
    save_state,
)
from quiz.styles import inject_css
from quiz.sidebar import render_sidebar, NORMAL_WHEEL_ITEMS, HELL_WHEEL_ITEMS
from quiz.board import render_board

# ── 1. Inject CSS ─────────────────────────────────────────────────────────────
inject_css()

# ── 2. Initialise session state (loads saved game from disk if available) ─────
init_session_state()

# ── 3. Login Gate ─────────────────────────────────────────────────────────────
if st.session_state.mode is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Changed color to #d8d3c7 (beige) to match the main board, kept size at 2.2rem
    st.markdown(
        "<h1 style='font-size:2.2rem !important; font-family: Cinzel, serif; "
        "color: #d8d3c7; text-align: center; margin-bottom: 20px;'>"
        "SELECT YOUR IDENTITY</h1>",
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
            pw = st.text_input("Enter Hoster Password", type="password")
            if st.button("Enter the Culling Game", use_container_width=True):
                if pw == HOSTER_PASSWORD:
                    st.session_state.mode = "hoster"
                    st.rerun()
                else:
                    st.error("Incorrect Cursed Energy Signature (Wrong Hoster Password).")
        else:
            username = ""
            if choice in TEAMS:
                saved_username = st.session_state["usernames"].get(choice, "")
                username = st.text_input(
                    "Enter Username",
                    value=saved_username,
                    max_chars=15,
                )

            pw = st.text_input("Enter Password", type="password")
            if st.button("Authenticate", use_container_width=True):
                if choice == "Colony Overseer (Admin)" and pw == ADMIN_PASSWORD:
                    st.session_state.mode = "admin"
                    st.rerun()
                elif choice in TEAMS and pw == TEAM_PASSWORDS.get(choice):
                    username = username.strip()
                    saved_username = st.session_state["usernames"].get(choice, "")
                    if not username:
                        username = saved_username

                    if not username:
                        st.error("Enter a username before authenticating.")
                    elif not re.fullmatch(r"[A-Za-z0-9]{1,10}", username):
                        st.error("Username must be 1-10 alphanumeric characters.")
                    elif any(
                        username.casefold() == other.casefold()
                        for team, other in st.session_state["usernames"].items()
                        if team != choice and other
                    ):
                        st.error("That username is already in use.")
                    else:
                        st.session_state["usernames"][choice] = username
                        save_state()
                        st.session_state.mode = choice
                        st.rerun()
                else:
                    st.error("Incorrect Cursed Energy Signature (Wrong Password).")

    st.stop()

# ── 4. Auto-refresh fragment — keeps all sessions in sync automatically ───────
@st.fragment(run_every=3)
def _sync_watcher() -> None:
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
            st.session_state.ce = loaded["ce"]
            st.session_state.board = loaded["board"]
            st.session_state["items"] = loaded["items"]
            st.session_state["usernames"] = loaded["usernames"]
            st.session_state["death_order"] = loaded["death_order"]
        st.rerun()

_sync_watcher()

# ── 5. Real-time sync: detect changes saved by other sessions ─────────────────
check_for_external_updates()

if st.session_state.mode in TEAMS:
    logged_in_team = st.session_state.mode
    if st.session_state.ce[logged_in_team] <= 0:
        st.markdown(
            """
            <div style="
                position: fixed; inset: 0; width: 100vw; height: 100vh;
                background: #000; z-index: 9999; pointer-events: all;
                display: flex; align-items: center; justify-content: center;
            ">
                <span style="
                    color: #ff2222; font-family: 'Cinzel', serif;
                    font-size: clamp(3rem, 10vw, 6rem); font-weight: 700;
                    letter-spacing: 0.1em; text-transform: uppercase;
                    text-shadow: 0 0 40px rgba(255, 0, 0, 0.6);
                    text-align: center;
                ">
                    YOU HAVE DIED
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

# ── 6. Main App (post-login) ──────────────────────────────────────────────────
render_sidebar()

def render_rules():
    st.markdown(
        "<h1 style='color: #d8c9c0; font-family: Cinzel, serif; text-align: center; font-size: 3.2rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 30px;'>Rules of Engagement</h1>", 
        unsafe_allow_html=True
    )
    
    st.markdown("""
    ### General Rules

    1. **Buzz-In:** Teams buzz in to answer. If the first team to buzz answers incorrectly, the right to answer passes to the next team in buzz order, and so on.
    2. **If No Team Answers:** If the entire buzz queue is exhausted with no correct answer (or no team buzzes at all), the answer is revealed and no team scores. The next question is picked by the team immediately following the question-selecting team in the MILAN/Menti ranking.
    3. **Correct Answers:** You deal damage equal to the question's point value to *any* opposing team's Cursed Energy. The team that answered correctly picks the next question.
    4. **Incorrect Answers:** You lose Cursed Energy equal to the question's point value.
    5. **Team Size:** Each team must have exactly 6 players. Teams cannot have fewer or more than 6 players.
    """)

    st.markdown("""
    ### Damage & Combat Mechanics

    6. **Consecutive Damage Multiplier:** If a team takes external damage on consecutive Questions, incoming damage reduces by 0.1x per turn (Min: 0.5x). Resets to 1.0x after one complete turn of no external damage taken. Applies *only* to damage a team takes from another team's correct answer it never applies to self-inflicted Cursed Energy loss or CE loss due to items. *(Exception: Does not apply to 1,500-point questions).*
    7. **Player Sacrifice:** Failing to get an answer chance for n−1 consecutive questions forces a team to sacrifice one player. Wrong answers do not count, and the counter resets to 0 after an eliminations. Sacrificed players cannot participate until revived and are not counted as active.
    8. **Team Elimination:** A team is eliminated if it has zero active (non-sacrificed) players, or if its Cursed Energy reaches zero.
    9. **Eliminating a Team (Bounty):** The attacking team immediately has all of its own sacrificed players revived (if any) **and** receives one free Normal Wheel spin.
    """)

    st.markdown("""
    ### Sacrifice Mechanics

    10. **Reviving a Player:** Cost = `min(25% of current Cursed Energy, 400)`. A team may never pay a cost that would bring its own Cursed Energy to 0 or below.
    11. **Buy a Wheel Spin:** Cost = `max(5% of current Cursed Energy, 100)`. Same restriction — cannot reduce your own Cursed Energy to 0 or below.
    12. **Item Limit:** A team can receive a maximum of 5 items obtained through spins bought via Rule 11. Items from any other source (streak spins, bounty spins, special-question spins) are uncapped.
    """)

    st.markdown("""
    ### Hints & Question Mechanics

    13. **Purchasing a Hint:** After buzzing in, a team may request a hint at a cost of 50% of the tier value.(Max 2 per team)
    14. **No Transfers:** Cursed Energy cannot be transferred between teams (except via specific items).
    """)

    st.markdown("""
    ### Streaks & Special Buffs

    15. **Three-Question Streak:** 3 consecutive questions answered correctly by the same team = 1 free Wheel Spin (Normal or Hell).
    16. **Last Stand Buff:** If only 1 player remains in a team, they gain **+500 Cursed Energy** for every correct answer (in addition to normal effects).
    """)

    st.markdown("""
    ### Items & Wheel Mechanics

    17. **Using Items:** Use immediately or store in inventory (except for some items).
    18. **Communication & Item Trades:** All inter-team communication, alliances, and item trades must be messaged to and approved by Kogane, who acts as mediator.
    19. **Bonus Questions:** Certain questions are marked as Bonus Questions. If the team answering a bonus question is correct, they receive a free Normal Wheel spin. If they are wrong, they are forced to take a Hell Wheel spin (in addition to the normal incorrect-answer penalty).
    """)

    st.markdown("""
    ### Leader & Comeback Mechanics

    20. **First-Place Penalty:** The 1st place team (per the live leaderboard) takes **10% increased damage** (1.1x) from external attacks.
    21. **Boss Bounty:** Eliminating the 1st place team awards **2 Normal Wheel spins** instead of 1, in addition to the player-revival from Rule 9.
    """)

def _render_item_cards(items: dict, accent: str) -> None:
    """Renders each item as a card with a coloured left border."""
    for item, desc in items.items():
        st.markdown(
            f"<div style='border-left: 4px solid {accent}; background: {accent}1a; "
            f"padding: 10px 14px; margin-bottom: 10px; border-radius: 0 4px 4px 0;'>"
            f"<div style='font-family: Rajdhani, sans-serif; font-weight: 700; font-size: 1.1rem; "
            f"color: #e6dfd6;'>{item}</div>"
            f"<div style='font-size: 0.95rem; color: #a1a1aa; margin-top: 3px; line-height: 1.45;'>{desc}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


def _render_wheel_header(title: str, subtitle: str, count: int, accent: str) -> None:
    """Renders a coloured banner above a wheel's item list."""
    st.markdown(
        f"<div style='border-bottom: 2px solid {accent}; padding-bottom: 8px; margin-bottom: 16px;'>"
        f"<div style='font-family: Cinzel, serif; font-size: 1.6rem; font-weight: 600; "
        f"letter-spacing: 0.08em; text-transform: uppercase; color: {accent};'>{title} "
        f"<span style='font-size: 0.9rem; opacity: 0.8;'>({count})</span></div>"
        f"<div style='font-size: 0.85rem; color: #a1a1aa; margin-top: 2px;'>{subtitle}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_items_guide():
    st.markdown(
        "<h1 style='color: #d8c9c0; font-family: Cinzel, serif; text-align: center; font-size: 3.2rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 30px;'> Culling Game Item Guide</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("A complete list of special items, abilities, and curses available in the Culling Games")
    st.divider()

    NORMAL_COLOR = "#4CAF50"  # green
    HELL_COLOR = "#E53935"    # red

    normal_col, hell_col = st.columns(2, gap="large")

    with normal_col:
        _render_wheel_header(
            "Normal Wheel", "Beneficial items", len(NORMAL_WHEEL_ITEMS), NORMAL_COLOR
        )
        _render_item_cards(NORMAL_WHEEL_ITEMS, NORMAL_COLOR)

    with hell_col:
        _render_wheel_header(
            "Hell Wheel", "Risky, chaotic, or harmful items", len(HELL_WHEEL_ITEMS), HELL_COLOR
        )
        _render_item_cards(HELL_WHEEL_ITEMS, HELL_COLOR)

def render_team_dashboard(team_name):
    st.markdown(
        f"<h1 style='color: #d8c9c0; font-family: Cinzel, serif; text-align: center; font-size: 3.2rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 30px;'>🗡️ {team_name} Terminal</h1>", 
        unsafe_allow_html=True
    )
    
    current_ce = st.session_state.ce[team_name]
    
    rank = get_ranked_teams().index(team_name) + 1
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3 style='color: #c9a0a0;'>🏆 Current Rank: #{rank}</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h3 style='color: #c9a0a0;'>🩸 Cursed Energy: {current_ce} CE</h3>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown("<h3 style='color: #9b7aab; font-family: Cinzel, serif;'>🎒 Cursed Inventory (Items)</h3>", unsafe_allow_html=True)
    
    items = st.session_state.get("items", {}).get(team_name, [])
    if not items:
        st.info("Your inventory is empty. Survive rounds to claim artifacts.")
    else:
        for item in items:
            st.markdown(f"- **{item}**")

# ── Role-Based Routing ──
if st.session_state.mode in ["admin", "hoster"]:
    tab1, tab2, tab3 = st.tabs(["Culling Game Board", "Rules of Engagement", "Items Guide"])
    with tab1:
        render_board()
    with tab2:
        render_rules()
    with tab3:
        render_items_guide()
        
elif st.session_state.mode in TEAMS:
    tab1, tab2, tab3 = st.tabs(["Team Dashboard", "Rules of Engagement", "Items Guide"])
    with tab1:
        render_team_dashboard(st.session_state.mode)
    with tab2:
        render_rules()
    with tab3:
        render_items_guide()