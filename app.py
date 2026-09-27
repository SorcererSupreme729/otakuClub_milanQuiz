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
from quiz.sidebar import render_sidebar, ITEM_DESCRIPTIONS
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
            st.session_state.hp = loaded["hp"]
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
    if st.session_state.hp[logged_in_team] <= 0:
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

    1. **Buzz-In:** The first team to buzz in gets the first opportunity to answer.
    2. **If No Team Answers:** The next question will be selected by the team immediately following the question-selecting team in the MILAN/Menti ranking.
    3. **Correct Answers:** You may deal damage equal to the question's point value to *any* opposing team.
    4. **Incorrect Answers:** You lose HP equal to the question's point value.
    """)

    st.markdown("""
    ### Damage & Combat Mechanics

    5. **Consecutive Damage Multiplier:** If a team takes damage on consecutive turns, incoming damage reduces by 0.1x per turn (Min: 0.5x). *(Progression: 1.0x → 0.9x → 0.8x → 0.7x → 0.6x → 0.5x)*. Resets to 1.0x after one complete turn of no damage. *(Exception: Does not apply to 1,500-point questions).*
    6. **Player Sacrifice (Inactivity):** If a team doesn't answer for *n−1* consecutive questions, they must sacrifice one player to remain in the game. Revived players cannot participate in team discussions.
    7. **Team Elimination:** If a team loses all of its players, they are eliminated.
    8. **Eliminating a Team (Bounty):**
       * If the attacking team *had* sacrificed players: All of those sacrificed players are immediately brought back.
       * If the attacking team *had no* sacrificed players: The attacking team receives one free spin of the Normal Wheel.
    """)

    st.markdown("""
    ### Sacrifice Mechanics

    9. **Reviving a Player:** Cost = `min(25% of current HP, 400 HP)`. Must have enough HP to pay the full cost.
    10. **Buy a Wheel Spin:** Cost = `max(5% of current HP, 100 HP)`. Must have enough HP to pay the full cost.
    11. **Item Limit:** A team can receive a maximum of 5 items through sacrifice mechanics.
    """)

    st.markdown("""
    ### Hints & Question Mechanics

    12. **Purchasing a Hint:** After buzzing in, sacrifice HP for a hint. Cost = **50% of the tier value** (e.g., 200pt → 100 HP).
    13. **No Point Transfers:** HP/points cannot be transferred between teams (except via specific items).
    """)

    st.markdown("""
    ### Streaks & Special Buffs

    14. **Three-Question Streak:** 3 correct answers in a row = 1 Free Wheel Spin (Normal or Hell).
    15. **Last Stand Buff:** If only 1 player remains in a team, they gain **+500 HP** for every correct answer (in addition to normal effects).
    """)

    st.markdown("""
    ### Items & Wheel Mechanics

    16. **Using Items:** Use immediately or store in inventory (unless restricted).
    17. **Item Trades:** All item trades must be discussed with and approved by Kogane.
    18. **Special Wheel Questions:** Certain questions award a Normal Wheel spin (if correct) or force a Hell Wheel spin (if incorrect).
    """)

    st.markdown("""
    ### Leader & Comeback Mechanics

    19. **First-Place Penalty:** The 1st place team takes **20% increased damage** (1.2x) from attacks. 
    20. **Boss Bounty:** Eliminating the 1st place team awards **2 Normal Wheel spins** instead of 1.
    """)

    st.markdown("""
    ### Quick Reference

    | Mechanic | Rule |
    | :--- | :--- |
    | **Starting / Max HP** | 4,000 HP |
    | **Question Tiers** | 200–1,500 |
    | **Correct Answer** | Deal tier damage to an opposing team |
    | **Wrong Answer** | Lose tier damage |
    | **Consecutive Damage** | Multiplier decreases by 0.1, min 0.5x (Resets after 1 safe turn) |
    | **3 Correct in a Row** | Free Normal Wheel spin |
    | **No Answer for n−1 Qs**| Sacrifice 1 player |
    | **Eliminate a Team** | Revive sacrificed players OR free Normal Wheel spin |
    | **Hint** | Costs 50% of question tier |
    | **Revive Player** | Costs min(25% HP, 400 HP) |
    | **Wheel Spin (Sacrifice)**| Costs max(5% HP, 100 HP) |
    | **Top HP Team** | Takes 20% increased damage |
    | **Eliminate Top Team** | 2 Normal Wheel spins |
    | **Last Stand** | +500 HP per correct answer (1 player remaining) |
    """)

def render_items_guide():
    st.markdown(
        "<h1 style='color: #d8c9c0; font-family: Cinzel, serif; text-align: center; font-size: 3.2rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 30px;'> Culling Game Item Guide</h1>", 
        unsafe_allow_html=True
    )
    st.markdown("A complete list of special items, abilities, and curses available in the Milan Culling Game:")
    st.divider()

    for item, desc in ITEM_DESCRIPTIONS.items():
        st.markdown(
            f"**{item}**<br><span style='font-size: 0.95rem; color: #a1a1aa;'>{desc}</span>", 
            unsafe_allow_html=True
        )
        st.write("")

def render_team_dashboard(team_name):
    st.markdown(
        f"<h1 style='color: #d8c9c0; font-family: Cinzel, serif; text-align: center; font-size: 3.2rem; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 30px;'>🗡️ {team_name} Terminal</h1>", 
        unsafe_allow_html=True
    )
    
    current_hp = st.session_state.hp[team_name]
    
    rank = get_ranked_teams().index(team_name) + 1
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h3 style='color: #c9a0a0;'>🏆 Current Rank: #{rank}</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h3 style='color: #c9a0a0;'>🩸 Cursed Energy: {current_hp} HP</h3>", unsafe_allow_html=True)
    
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