"""
board.py
--------
Renders the main Jeopardy-style game board grid.

Each category gets a column; each tier gets a button row inside that column.
Active tiles show the point value; completed tiles show a disabled ✖ marker.
"""

import streamlit as st

from quiz.config import CATEGORIES, TIERS
from quiz.components import show_question


def render_board() -> None:
    """Renders the page title, subtitle, and the full category/tier grid."""
    _render_header()
    _render_grid()


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_header() -> None:
    """Renders the stylised game title and tagline."""

    st.markdown(
        """
        <h1 style="
            font-size: 2.8rem !important;
            text-align: center;
            color: #b7202e;
            font-family: Cinzel, serif;
            letter-spacing: 4px;
            text-shadow: 0 0 25px rgba(183, 32, 46, 0.55);
            margin-top: 0px;
            margin-bottom: 10px;
            padding: 0;
        ">
            殺戮 CULLING GAME 殺戮
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            text-align: center;
            color: #8a4a4a;
            font-family: Rajdhani, sans-serif;
            font-weight: 600;
            letter-spacing: 3px;
            margin-top: 0px;
            margin-bottom: 32px;
            padding: 0;
        ">
            SURVIVE THE ROUNDS — MILAN QUIZ EDITION
        </p>
        """,
        unsafe_allow_html=True,
    )


def _render_grid() -> None:
    """Renders one Streamlit column per category, each containing tier buttons."""
    cols = st.columns(len(CATEGORIES))

    for i, category in enumerate(CATEGORIES):
        with cols[i]:
            _render_category_header(category)
            _render_tier_buttons(category)


def _render_category_header(category: str) -> None:
    """Renders the centred category name banner above its tile column."""

    header_html = f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: rgba(183, 32, 46, 0.08);
        border-bottom: 2px solid rgba(183, 32, 46, 0.5);
        min-height: 90px;
        height: auto;
        width: 100%;
        margin: 0;
        padding: 14px 6px;
        box-sizing: border-box;
    ">
        <span style="
            font-family: 'Rajdhani', sans-serif;
            font-weight: 700;
            color: #c9a0a0;
            text-transform: uppercase;
            font-size: 0.85rem;
            line-height: 1.2;
            display: block;
            width: 100%;
            word-break: break-word;
        ">{category}</span>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

def _render_tier_buttons(category: str) -> None:
    """Renders active or disabled buttons for every tier in a category column."""
    for tier in TIERS:
        is_active = st.session_state.board[category][tier]
        if is_active:
            if st.button(
                f"{tier} HP",
                key=f"{category}_{tier}",
                use_container_width=True,
            ):
                show_question(category, tier)
        else:
            st.button(
                "✖",
                key=f"{category}_{tier}_done",
                disabled=True,
                use_container_width=True,
            )
