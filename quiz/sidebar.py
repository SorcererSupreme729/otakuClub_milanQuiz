"""
sidebar.py
----------
Renders the entire sidebar panel.

- Admin view  : HP bars + per-team adjust controls + reset + password download.
- Hoster view : HP bars ranked by HP (highest first), with rank badges.
- Team view   : Read-only HP bars with a team-name header.
- All views   : Log-out / switch-mode button at the bottom.
"""

import streamlit as st

from quiz.config import TEAMS, TEAM_COLORS
from quiz.components import hp_bar_html, generate_credentials_file
from quiz.state import save_state


def render_sidebar() -> None:
    """Renders the full sidebar based on the current session mode."""
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


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_admin_sidebar() -> None:
    """Admin panel: HP management, password download, and game reset."""
    st.header("⛩️ Colony Overseer")
    st.caption("Manage cursed energy (HP), damage, and healing here.")

    st.download_button(
        label="📄 Download Passwords",
        data=generate_credentials_file(),
        file_name="Culling_Game_Passwords.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    for team, color in zip(TEAMS, TEAM_COLORS):
        # HP bar display
        st.markdown(
            hp_bar_html(team, st.session_state.hp[team], color),
            unsafe_allow_html=True,
        )

        # Inline number input + apply button
        col1, col2 = st.columns([1.5, 1], gap="small")
        with col1:
            adj_val = st.number_input(
                f"Adjust {team}",
                value=0,
                step=100,
                key=f"adj_{team}",
                label_visibility="collapsed",
            )
        with col2:
            if st.button("Apply", key=f"btn_{team}", use_container_width=True):
                st.session_state.hp[team] = max(
                    0, st.session_state.hp[team] + adj_val
                )
                save_state()
                st.rerun()

    st.divider()
    if st.button("🚨 Reset Entire Game", use_container_width=True):
        from quiz.config import MAX_HP, TIERS, CATEGORIES

        st.session_state.hp = {team: MAX_HP for team in TEAMS}
        st.session_state.board = {
            cat: {tier: True for tier in TIERS} for cat in CATEGORIES
        }
        save_state()
        st.rerun()


def _render_hoster_sidebar() -> None:
    """
    Hoster panel: teams listed in descending HP order with rank badges.
    🥇 / 🥈 / 🥉 for the podium, then #4 … #8 below.
    """
    st.header("🎬 Hoster Panel")
    st.caption("Live standings — click questions on the board to host.")

    st.divider()

    # Build a colour lookup so we can match the original TEAM_COLORS after sorting
    color_map = dict(zip(TEAMS, TEAM_COLORS))

    # Sort teams high → low HP (highest HP = currently winning)
    ranked = sorted(
        TEAMS,
        key=lambda t: st.session_state.hp[t],
        reverse=True,
    )

    # Rank badges: medals for top 3, plain numbers after
    badges = ["🥇", "🥈", "🥉"] + [f"**#{i}**" for i in range(4, len(TEAMS) + 1)]

    for badge, team in zip(badges, ranked):
        hp = st.session_state.hp[team]
        color = color_map[team]

        # Rank label + team name inline
        st.markdown(
            f"<div style='font-family: Rajdhani, sans-serif; font-size: 0.8rem; "
            f"color: #8a4a4a; margin-top: 10px; margin-bottom: -6px;'>"
            f"{badge}&nbsp;&nbsp;<span style='color:{color}; font-weight:700;'>{team}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown(hp_bar_html(team, hp, color), unsafe_allow_html=True)


def _render_team_sidebar(logged_in_team: str | None) -> None:
    """Team view: read-only HP bars."""
    if logged_in_team:
        st.header(f"🗡️ {logged_in_team} Terminal")
        st.caption("Your team is active. Awaiting your turn.")
    else:
        st.header("🩸 Viewer")
        st.caption("Live cursed energy — read only")

    st.divider()
    for team, color in zip(TEAMS, TEAM_COLORS):
        st.markdown(
            hp_bar_html(team, st.session_state.hp[team], color),
            unsafe_allow_html=True,
        )
