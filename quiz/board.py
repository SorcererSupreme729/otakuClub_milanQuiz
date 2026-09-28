"""
board.py
--------
Renders the main Jeopardy-style game board grid.

Each category gets a column; each tier gets a button row inside that column.
Active tiles show the point value; completed tiles show a disabled ✖ marker.
"""

import base64
import streamlit as st

from quiz.config import CATEGORIES, TIERS
from quiz.components import show_question


def render_board() -> None:
    """Renders the page title, subtitle, and the full category/tier grid."""
    _render_header()
    _render_grid()


# ── Private helpers ───────────────────────────────────────────────────────────

def _render_header() -> None:
    """Renders the stylised game title and tagline perfectly centred."""
    st.markdown(
        """
        <div style="margin-top: 15px; margin-bottom: 35px; display: flex; flex-direction: column; align-items: center; text-align: center;">
            <p style="
                color: #8f789e; 
                font-size: 11px; 
                font-weight: 500; 
                letter-spacing: 0.22em; 
                text-transform: uppercase; 
                margin: 0 0 10px 0; 
                font-family: 'Oswald', sans-serif;
            ">
                Tokyo No. 1 Colony
            </p>
            <h1 style="
                font-size: 3.5rem !important;
                color: #d8d3c7;
                font-family: 'Cinzel', serif;
                font-weight: 600;
                letter-spacing: 0.11em;
                text-shadow: 0 4px 30px rgba(216, 211, 199, 0.08);
                margin: 0 0 13px 0;
                padding: 0;
                line-height: 1.08;
                text-transform: uppercase;
            ">
                <span style="color: #5a3e6b; font-size: 0.6em; vertical-align: 0.13em;">死</span> CULLING GAME <span style="color: #5a3e6b; font-size: 0.6em; vertical-align: 0.13em;">滅</span>
            </h1>
            <p style="
                font-size: 11px;
                color: #77716b;
                font-family: 'Oswald', sans-serif;
                letter-spacing: 0.3em;
                text-transform: uppercase;
                margin: 0 0 18px 0;
                padding: 0;
            ">
                SURVIVE THE ROUNDS · MILAN QUIZ EDITION
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_grid() -> None:
    """Renders one Streamlit column per category, each containing tier buttons."""
    cols = st.columns(len(CATEGORIES))

    for i, category in enumerate(CATEGORIES):
        with cols[i]:
            _render_category_header(category, i)
            _render_tier_buttons(category)


def _render_category_header(category: str, index: int = 0) -> None:
    """Renders the centred category name banner above its tile column."""

    accents = [
        "#B5542A", "#4B7F52", "#3E5468", "#5A3E6B",
        "#8A5A2E", "#B5542A", "#4B7F52", "#3E5468", "#B5542A"
    ]
    accent = accents[index % len(accents)]

    if "CHIKA" in category.upper():
        try:
            with open("chikaFujiwaraTitle.jpg", "rb") as img_file:
                b64_img = base64.b64encode(img_file.read()).decode()

            # Flattened single-line HTML to bypass Markdown parser injections.
            # Same 100px frame + number badge + border treatment as the text
            # headers, just with the image as a background instead of the
            # gradient fill, so this column no longer breaks the row's rhythm.
            img_html = f"""<div style="height: 100px; width: 100%; overflow: hidden; margin-bottom: 5px;"><div style="position: relative; height: 100%; width: 100%; margin: 0; padding: 0; box-sizing: border-box; border-top: 2px solid {accent}; border-right: 1px solid {accent}55; border-bottom: 1px solid {accent}85; background-image: linear-gradient(180deg, rgba(10,8,11,0.15) 0%, rgba(10,8,11,0.0) 35%), url('data:image/jpeg;base64,{b64_img}'); background-size: cover; background-position: center 20%;"><span style="position: absolute; top: 6px; left: 6px; color: #f2ece1; font-family: 'Oswald', sans-serif; font-weight: 600; font-size: 0.75rem; letter-spacing: 0.12em; line-height: 1; background: {accent}; padding: 3px 7px; border-radius: 2px; box-shadow: 0 1px 4px rgba(0,0,0,0.6);">0{index + 1}</span></div></div>"""
            st.markdown(img_html, unsafe_allow_html=True)
        except Exception:
            st.markdown(f"### {category}")
        return

    # Flattened single-line HTML with a strict 100px outer wrapper.
    # The number sits in its own fixed-height row; the name lives in a
    # flex:1 row that centers it vertically in whatever space is left,
    # so 1-line and 2-line category names land at the same visual
    # position instead of one hugging the bottom edge.
    header_html = f"""<div style="height: 100px; width: 100%; overflow: hidden; margin-bottom: 5px;"><div style="display: flex; flex-direction: column; background: linear-gradient(145deg, {accent}2b, rgba(17, 15, 19, 0.9)); border-top: 2px solid {accent}; border-right: 1px solid {accent}55; border-bottom: 1px solid {accent}85; height: 100%; width: 100%; margin: 0; padding: 10px 8px; box-sizing: border-box;"><span style="color: {accent}; font-family: 'Oswald', sans-serif; font-size: 0.75rem; letter-spacing: 0.12em; opacity: 0.8; line-height: 1; flex: 0 0 auto;">0{index + 1}</span><div style="flex: 1 1 auto; display: flex; align-items: center; justify-content: center; width: 100%;"><span style="font-family: 'Cinzel', serif; font-weight: 500; color: #c2bbb1; text-transform: uppercase; font-size: 0.72rem; line-height: 1.25; display: block; width: 100%; word-break: break-word; text-align: center;">{category}</span></div></div></div>"""

    st.markdown(header_html, unsafe_allow_html=True)

def _render_tier_buttons(category: str) -> None:
    """Renders active or disabled buttons for every tier in a category column."""
    for tier in TIERS:
        is_active = st.session_state.board[category][tier]
        if is_active:
            if st.button(
                f"{tier} CE",
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