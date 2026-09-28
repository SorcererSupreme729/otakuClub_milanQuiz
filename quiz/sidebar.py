import streamlit as st
from quiz.config import TEAMS, TEAM_COLORS
from quiz.components import ce_bar_html, generate_credentials_file
from quiz.state import get_ranked_teams, save_state, update_team_ce

# ── Item catalogue ────────────────────────────────────────────────────────────
# Items are grouped by the wheel they come from. The Items Guide tab renders
# NORMAL_WHEEL_ITEMS in green and HELL_WHEEL_ITEMS in red.

NORMAL_WHEEL_ITEMS = {
    "Revival Blessing": "Revives a dead teammate.",
    "Heal 400": "Restores 400 CE.",
    "Poison": "Poisons another team; they take an extra 6.25% CE for every wrong answer. It is removed if they answer any question correctly.",
    "Barrier": "Nullifies any explicit damage dealt (1 time use only).",
    "Rocky helmet": "The team that deals damage to the team with a rocky helmet will take half the damage. Breaks after 2 uses.",
    "Landmine": "Allows a team to place a landmine on one question. If any team chooses that question, they take 400 CE worth of damage.",
    "Black Flash": "Activate after buzzing correctly, before dealing damage. Flip a coin: Win = 1.2x damage, Lose = 0.8x damage.",
    "Leech Seed": "Target team loses 100 CE for 4 turns, and your team heals that amount.",
    "Domain": "The team that set up a domain on the question is immune to any damage from the question. (Only 3 exist).",
    "Focus Sash": "If an attack would reduce you to 0 CE, you survive at 1 CE. One use only.",
    "Life Drain": "Every team except you loses 10% of their current CE. If they have less than 200CE, they lose 200CE instead.",
    "Kazuma’s hand": "Steal another team's item.",
    "Truck-kun’s insurance payout": "When receiving lethal damage, Isekai one teammate to survive with 1000 CE. The teammate can never be revived.",
    "Shinigami Eyes": "Sacrifice 50% of your current CE to 'write down' a team's name. Their next incorrect answer penalty is multiplied by 2.5x.",
    "Uno Reverse": "Reflect all damage.",
}

HELL_WHEEL_ITEMS = {
    "Excalibur": "Forces another team to press the buzzer first. Will overlook any other buzzers. If they get the correct answer, they get to deal 25% more damage.",
    "Heal 1CE": "Heals exactly 1 CE.",
    "Swap CE": "Swap CE with any team of your choice (to be used immediately).",
    "Critical hit": "Lose 10% CE.",
    "Stub your toe": "Lose exactly 1 CE.",
    "Mahoraga’s Wheel": "A player activates this right when a category is selected. For the rest of the game, that player has \"adapted\" to that specific category; they take half damage from any attacks originating from that column. (Only 1 exists).",
    "Freeze": "Team cannot buzz on the next question.",
    "Gambler’s Domain": "Flip a coin: heads = +50% damage, tails = −50% damage on your next attack.",
    "Explosion": "Deal 50% of your current CE as damage to another team. You also lose that amount. FORCED INSTANT USE.",
    "Chaos": "A die is rolled; each roll has some effect:<br>• 1: All damage is reduced by 50% for the entire game for that team. Explicit damage.<br>• 2: All items disappear.<br>• 3: All damage is increased by 50% for the entire game except for the team that got the item.<br>• 4: The team loses 3 players immediately.<br>• 5: Normal Wheel disappears from the game.<br>• 6: Every team has their CE averaged.",
    "Idle Death Gamble": "Flip three coins. 3 Heads → +1500 CE, 2 Heads → +500 CE, 1 Head → −500 CE, 0 Heads → −1500 CE.",
    "Rumbling": "Can only be activated if your team drops below 1,000 CE. Deal 400 flat damage to every other team on the board. One-time use only.",
}

# Combined lookup (Normal Wheel first, then Hell Wheel) — used by the admin
# item dropdown so every item can be assigned to a team.
ITEM_DESCRIPTIONS = {**NORMAL_WHEEL_ITEMS, **HELL_WHEEL_ITEMS}

PREMADE_ITEMS = list(ITEM_DESCRIPTIONS.keys())

def render_sidebar() -> None:
    mode = st.session_state.mode
    is_admin = mode == "admin"
    is_hoster = mode == "hoster"
    logged_in_team = mode if mode in TEAMS else None

    with st.sidebar:
        if is_admin:
            _render_admin_sidebar()
        elif is_hoster:
            _render_hoster_sidebar()
        else:
            _render_team_sidebar(logged_in_team)

        st.divider()
        if st.button("🔁 Switch Mode / Log Out", use_container_width=True):
            st.session_state.mode = None
            st.rerun()

def _render_admin_sidebar() -> None:
    st.header("⛩️ Colony Overseer")
    st.caption("Manage cursed energy (CE), items, and healing here.")

    st.download_button(
        label="📄 Download Passwords",
        data=generate_credentials_file(),
        file_name="Culling_Game_Passwords.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    for team, color in zip(TEAMS, TEAM_COLORS):
        username = st.session_state["usernames"].get(team, "")
        display_name = f"{team} — {username}" if username else team
        st.markdown(
            ce_bar_html(display_name, st.session_state.ce[team], color),
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([1.5, 1], gap="small")
        with col1:
            adj_val = st.number_input(
                f"Adjust {team}", value=0, step=100, key=f"adj_{team}", label_visibility="collapsed"
            )
        with col2:
            if st.button("Apply", key=f"btn_{team}", use_container_width=True):
                update_team_ce(team, st.session_state.ce[team] + adj_val)
                save_state()
                st.rerun()
                
        # Items Management Expander with Premade Selection & Custom Input
        with st.expander(f"🎒 Manage {team} Items"):
            current_items = st.session_state["items"].get(team, [])
            for i, item in enumerate(current_items):
                c1, c2 = st.columns([4, 1])
                c1.write(f"• {item}")
                if c2.button("✖", key=f"del_item_{team}_{i}"):
                    st.session_state["items"][team].pop(i)
                    save_state()
                    st.rerun()
            
            item_source = st.radio(
                "Source", 
                ["Select an item", "Add item (Custom)"], 
                horizontal=True, 
                key=f"source_{team}", 
                label_visibility="collapsed"
            )
            
            item_to_add = ""
            if item_source == "Select an item":
                options_with_prompt = ["-- Select an item --"] + PREMADE_ITEMS
                chosen_premade = st.selectbox(
                    "Select an item", 
                    options_with_prompt, 
                    key=f"premade_{team}", 
                    label_visibility="collapsed"
                )
                if chosen_premade != "-- Select an item --":
                    item_to_add = chosen_premade
            else:
                item_to_add = st.text_input(
                    "Add item", 
                    key=f"custom_{team}", 
                    label_visibility="collapsed", 
                    placeholder="Type custom item..."
                )
            
            if st.button("➕ Add", key=f"add_item_btn_{team}", use_container_width=True):
                if item_to_add and item_to_add.strip():
                    st.session_state["items"][team].append(item_to_add.strip())
                    save_state()
                    st.rerun()
                else:
                    st.warning("Please select or type a valid item.")

    st.divider()
    if st.button("🚨 Reset Entire Game", use_container_width=True):
        from quiz.config import MAX_CE, TIERS, CATEGORIES

        st.session_state.ce = {team: MAX_CE for team in TEAMS}
        st.session_state.board = {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}
        st.session_state["items"] = {team: [] for team in TEAMS}
        st.session_state["death_order"] = []
        save_state()
        st.rerun()


def _render_hoster_sidebar() -> None:
    st.header("🎬 Hoster Panel")
    st.caption("Live standings — click questions on the board to host.")
    st.divider()

    color_map = dict(zip(TEAMS, TEAM_COLORS))
    ranked = get_ranked_teams()
    badges = ["🥇", "🥈", "🥉"] + [f"#{i}" for i in range(4, len(TEAMS) + 1)]

    defeated_teams = [
        st.session_state["usernames"].get(team) or team
        for team in TEAMS
        if st.session_state.ce[team] <= 0
    ]
    if defeated_teams:
        st.warning(f"Eliminated: {', '.join(defeated_teams)}")

    for badge, team in zip(badges, ranked):
        ce = st.session_state.ce[team]
        color = color_map[team]
        username = st.session_state["usernames"].get(team, "")
        display_name = f"{team} — {username}" if username else team
        st.markdown(
            f"<div style='font-family: Rajdhani, sans-serif; font-size: 0.8rem; "
            f"color: #8a4a4a; margin-top: 10px; margin-bottom: -6px;'>"
            f"{badge}&nbsp;&nbsp;<span style='color:{color}; font-weight:700;'>{display_name}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(ce_bar_html(display_name, ce, color), unsafe_allow_html=True)


def _render_team_sidebar(logged_in_team: str | None) -> None:
    if logged_in_team:
        username = st.session_state["usernames"].get(logged_in_team, "")
        identity = f"{logged_in_team} — {username}" if username else logged_in_team
        st.header(f"{identity} Terminal")
        st.caption("Your team is alive. Awaiting your turn.")
    else:
        st.header("🩸 Viewer")
        st.caption("Live cursed energy — read only")

    st.caption("Live standings")
    st.divider()

    color_map = dict(zip(TEAMS, TEAM_COLORS))
    ranked = get_ranked_teams()
    badges = ["🥇", "🥈", "🥉"] + [f"#{i}" for i in range(4, len(TEAMS) + 1)]

    for badge, team in zip(badges, ranked):
        color = color_map[team]
        username = st.session_state["usernames"].get(team, "")
        display_name = f"{team} — {username}" if username else team
        st.markdown(
            f"<div style='font-family: Rajdhani, sans-serif; font-size: 0.8rem; "
            f"color: #8a4a4a; margin-top: 10px; margin-bottom: -6px;'>"
            f"{badge}&nbsp;&nbsp;<span style='color:{color}; font-weight:700;'>{display_name}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            ce_bar_html(display_name, st.session_state.ce[team], color),
            unsafe_allow_html=True,
        )