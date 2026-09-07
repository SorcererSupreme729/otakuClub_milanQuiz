"""
components.py
-------------
Reusable UI components: the HP bar, the question dialog, and the
credentials file generator.
"""

import streamlit as st

from quiz.config import MAX_HP, ADMIN_PASSWORD, TEAM_PASSWORDS, TEAMS
from quiz.state import save_state


def hp_bar_html(team: str, hp: int, color: str) -> str:
    """
    Returns an HTML string that renders a labelled, coloured HP progress bar
    for a single team.

    Args:
        team:  Team display name.
        hp:    Current hit-point value.
        color: CSS colour string (hex / rgb) used for the bar and label.

    Returns:
        Raw HTML string ready for ``st.markdown(..., unsafe_allow_html=True)``.
    """
    pct = max(0, min(100, (hp / MAX_HP) * 100))
    return f"""
    <div style="margin: 10px 0px 4px 0px;">
        <div style="display:flex; justify-content:space-between; font-family:'Rajdhani',sans-serif;
                    font-weight:700; color:{color}; font-size:0.95rem; margin-bottom: 4px;">
            <span>{team}</span><span>{hp} HP</span>
        </div>
        <div style="background:rgba(255,255,255,0.08); border-radius:4px; height:8px; overflow:hidden;
                    border:1px solid rgba(255,255,255,0.15);">
            <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, {color}, #ffffff22);
                        box-shadow:0 0 8px {color}; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """


@st.dialog("Question")
def show_question(category: str, tier: int) -> None:
    """
    Streamlit dialog that displays a question tile.

    - Team views : shows the question and waits for the host.
    - Admin / Hoster views: adds Reveal Answer and Mark as Done controls.

    Args:
        category: The category column label.
        tier:     The point/HP value for this tile.
    """
    mode = st.session_state.mode
    can_control = mode in ("admin", "hoster")  # both roles host questions

    # Large header showing category and tier
    st.markdown(
        f"<div style='font-size: 2.2rem; font-family: Cinzel, serif; color: #b7202e; "
        f"border-bottom: 2px solid #8B0000; padding-bottom: 10px; margin-bottom: 20px;'>"
        f"{category} — {tier} HP</div>",
        unsafe_allow_html=True,
    )

    # Placeholder question text (replace with actual question data later)
    st.markdown(
        "<div style='font-size: 1.8rem; font-family: Rajdhani, sans-serif; line-height: 1.4; "
        "color: #d8c9c0; margin-bottom: 30px;'>Insert your question text here...</div>",
        unsafe_allow_html=True,
    )

    if can_control:
        if st.button("🔍 Reveal Answer", use_container_width=True):
            st.markdown(
                "<div style='font-size: 1.8rem; font-family: Rajdhani, sans-serif; "
                "color: #4CAF50; font-weight: bold; margin-bottom: 20px;'>"
                "Insert your answer text here...</div>",
                unsafe_allow_html=True,
            )

        if st.button("✅ Mark as Done & Close", use_container_width=True):
            st.session_state.board[category][tier] = False
            save_state()  # Persist board state — triggers sync on other tabs
            st.rerun()
    else:
        st.info("Waiting for the host to reveal the answer...")


def generate_credentials_file() -> str:
    """
    Builds and returns a plain-text string listing all login credentials.
    Suitable for use as a download button payload.

    Returns:
        Formatted credential document as a string.
    """
    lines = [
        "========================================",
        "⚔️ MILAN QUIZ: CULLING GAME CREDENTIALS ⚔️",
        "========================================",
        "",
        "⛩️ COLONY OVERSEER (ADMIN) PASSWORD:",
        ADMIN_PASSWORD,
        "",
        "----------------------------------------",
        "🩸 TEAM PASSWORDS:",
    ]
    for team, pw in TEAM_PASSWORDS.items():
        lines.append(f"{team}:  {pw}")
    lines += [
        "----------------------------------------",
        "Keep this document secure. Let the Culling Game begin.",
    ]
    return "\n".join(lines)
