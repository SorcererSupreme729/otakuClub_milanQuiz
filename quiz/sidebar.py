import streamlit as st
from quiz.config import TEAMS, TEAM_COLORS
from quiz.components import hp_bar_html, generate_credentials_file
from quiz.state import save_state

ITEM_DESCRIPTIONS = {
    "Revival Blessing": "Revives a dead teammate.",
    "Heal 400": "Restores 400 HP.",
    "Poison": "Poisons another team; they take an extra 6.25% HP for every wrong answer. It is removed if they answer any question correctly.",
    "Barrier": "Nullifies any explicit damage dealt (1 time use only).",
    "Rocky helmet": "The team that deals damage to the team with a rocky helmet will take half the damage. Breaks after 2 uses.",
    "Landmine": "Allows a team to place a landmine on one question. If any team chooses that question, they take 400 HP worth of damage.",
    "Black Flash": "Activate after buzzing correctly, before dealing damage. Flip a coin: Win = 1.2x damage, Lose = 0.8x damage.",
    "Leech Seed": "Target team loses 100 HP for 4 turns, and your team heals that amount.",
    "Domain": "The team that set up a domain on the question is immune to any damage from the question. (Only 3 exist).",
    "Focus Sash": "If an attack would reduce you to 0 HP, you survive at 1 HP. One use only.",
    "Life Drain": "Every team except you loses 10% of their current HP. If they have less than 200HP, they lose 200HP instead.",
    "Kazuma’s hand": "Steal another team's item.",
    "Truck-kun’s insurance payout": "When receiving lethal damage, Isekai one teammate to survive with 1000 HP. The teammate can never be revived.",
    "Shinigami Eyes": "Sacrifice 50% of your current HP to 'write down' a team's name. Their next incorrect answer penalty is multiplied by 2.5x.",
    "Uno Reverse": "Reflect all items.",
}

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
    st.caption("Manage cursed energy (HP), items, and healing here.")

    st.download_button(
        label="📄 Download Passwords",
        data=generate_credentials_file(),
        file_name="Culling_Game_Passwords.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    for team, color in zip(TEAMS, TEAM_COLORS):
        st.markdown(
            hp_bar_html(team, st.session_state.hp[team], color),
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([1.5, 1], gap="small")
        with col1:
            adj_val = st.number_input(
                f"Adjust {team}", value=0, step=100, key=f"adj_{team}", label_visibility="collapsed"
            )
        with col2:
            if st.button("Apply", key=f"btn_{team}", use_container_width=True):
                st.session_state.hp[team] = max(0, st.session_state.hp[team] + adj_val)
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
        from quiz.config import MAX_HP, TIERS, CATEGORIES

        st.session_state.hp = {team: MAX_HP for team in TEAMS}
        st.session_state.board = {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}
        st.session_state["items"] = {team: [] for team in TEAMS}
        save_state()
        st.rerun()


def _render_hoster_sidebar() -> None:
    st.header("🎬 Hoster Panel")
    st.caption("Live standings — click questions on the board to host.")
    st.divider()

    color_map = dict(zip(TEAMS, TEAM_COLORS))
    ranked = sorted(TEAMS, key=lambda t: st.session_state.hp[t], reverse=True)
    badges = ["🥇", "🥈", "🥉"] + [f"**#{i}**" for i in range(4, len(TEAMS) + 1)]

    for badge, team in zip(badges, ranked):
        hp = st.session_state.hp[team]
        color = color_map[team]
        st.markdown(
            f"<div style='font-family: Rajdhani, sans-serif; font-size: 0.8rem; "
            f"color: #8a4a4a; margin-top: 10px; margin-bottom: -6px;'>"
            f"{badge}&nbsp;&nbsp;<span style='color:{color}; font-weight:700;'>{team}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(hp_bar_html(team, hp, color), unsafe_allow_html=True)


def _render_team_sidebar(logged_in_team: str | None) -> None:
    if logged_in_team:
        st.header(f"🗡️ {logged_in_team} Terminal")
        st.caption("Your team is active. Awaiting your turn.")
    else:
        st.header("🩸 Viewer")
        st.caption("Live cursed energy — read only")

    st.caption("Live standings")
    st.divider()

    color_map = dict(zip(TEAMS, TEAM_COLORS))
    ranked = sorted(TEAMS, key=lambda team: st.session_state.hp[team], reverse=True)
    badges = ["🥇", "🥈", "🥉"] + [f"**#{i}**" for i in range(4, len(TEAMS) + 1)]

    for badge, team in zip(badges, ranked):
        color = color_map[team]
        st.markdown(
            f"<div style='font-family: Rajdhani, sans-serif; font-size: 0.8rem; "
            f"color: #8a4a4a; margin-top: 10px; margin-bottom: -6px;'>"
            f"{badge}&nbsp;&nbsp;<span style='color:{color}; font-weight:700;'>{team}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            hp_bar_html(team, st.session_state.hp[team], color),
            unsafe_allow_html=True,
        )