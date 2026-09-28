"""
components.py
-------------
Reusable UI components: the CE bar, the question dialog, and the
credentials file generator.
"""

import streamlit as st
import os
import base64

from quiz.config import MAX_CE, ADMIN_PASSWORD, HOSTER_PASSWORD, TEAM_PASSWORDS, TEAMS
from quiz.state import save_state
from quiz.questions import load_questions, get_question


def ce_bar_html(team: str, ce: int, color: str) -> str:
    """
    Returns an HTML string that renders a labelled, coloured CE progress bar
    for a single team.

    Args:
        team:  Team display name.
        ce:    Current hit-point value.
        color: CSS colour string (hex / rgb) used for the bar and label.

    Returns:
        Raw HTML string ready for ``st.markdown(..., unsafe_allow_html=True)``.
    """
    pct = max(0, min(100, (ce / MAX_CE) * 100))
    return f"""
    <div style="margin: 10px 0px 4px 0px;">
        <div style="display:flex; justify-content:space-between; font-family:'Rajdhani',sans-serif;
                    font-weight:700; color:{color}; font-size:0.95rem; margin-bottom: 4px;">
            <span>{team}</span><span>{ce} CE</span>
        </div>
        <div style="background:rgba(255,255,255,0.08); border-radius:4px; height:8px; overflow:hidden;
                    border:1px solid rgba(255,255,255,0.15);">
            <div style="width:{pct}%; height:100%; background:linear-gradient(90deg, {color}, #ffffff22);
                        box-shadow:0 0 8px {color}; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """

def _render_media(media_type: str, media_url: str) -> None:
    if not media_type or not media_url:
        return

    # Paragraph has no separate media
    if media_type == "paragraph":
        return

    # If the media is a local file, convert it to an absolute path
    if not media_url.startswith(("http://", "https://")):
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        media_url = os.path.join(project_root, media_url)

    # Debugging information
    if not media_url.startswith(("http://", "https://")):
        if not os.path.exists(media_url):
            st.error(f"Media file not found: {media_url}")
            return

    if media_type == "photo":
        st.image(media_url)

    elif media_type == "audio":
        st.audio(media_url)

    elif media_type == "video":
        st.video(media_url)


@st.dialog("Question", width="large")
def show_question(category: str, tier: int) -> None:
    """
    Streamlit dialog that displays a question tile.

    - Team views: shows the question and waits for the host.
    - Admin / Hoster views: adds Reveal Answer and Mark as Done controls.
    """

    mode = st.session_state.mode
    can_control = mode in ("admin", "hoster")

    data = load_questions()
    q = get_question(data, category, tier)

    # Header: Compact centered image banner for Chika, purple text for everything else
    if "CHIKA" in category.upper():
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(project_root, "chikaFujiwaraTitle.jpg")
            
            # Narrower column ratio to make the image ~2x smaller
            _, img_col, _ = st.columns([1, 0.6, 1])
            with img_col:
                st.image(img_path, use_container_width=True)
                st.markdown(
                    f"<div style='text-align: center; font-family: Cinzel, serif; color: #9b7aab; "
                    f"font-size: 1.1rem; font-weight: 600; margin-top: 5px; margin-bottom: 20px; "
                    f"letter-spacing: 0.08em; border-bottom: 2px solid rgba(90, 62, 107, 0.6); padding-bottom: 8px;'>"
                    f"{tier} CE</div>",
                    unsafe_allow_html=True,
                )
        except Exception:
            st.markdown(
                f"<div style='font-size: 2.2rem; font-family: Cinzel, serif; "
                f"color: #9b7aab; border-bottom: 2px solid rgba(90, 62, 107, 0.6); "
                f"padding-bottom: 10px; margin-bottom: 20px; "
                f"text-shadow: 0 0 15px rgba(90, 62, 107, 0.4);'>"
                f"{category} — {tier} CE</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            f"<div style='font-size: 2.2rem; font-family: Cinzel, serif; "
            f"color: #9b7aab; border-bottom: 2px solid rgba(90, 62, 107, 0.6); "
            f"padding-bottom: 10px; margin-bottom: 20px; "
            f"text-shadow: 0 0 15px rgba(90, 62, 107, 0.4);'>"
            f"{category} — {tier} CE</div>",
            unsafe_allow_html=True,
        )

    # If question doesn't exist
    if q is None:
        st.warning("No question found for this tile.")

        if can_control:
            if st.button("✅ Mark as Done & Close", use_container_width=True):
                st.session_state.board[category][tier] = False
                save_state()
                st.rerun()

        return

    # --------------------------------------------------
    # QUESTION DATA
    # --------------------------------------------------

    question_text = q.get("question_text") or "Insert your question text here..."

    question_media_type = q.get("question_media_type", "")
    question_media_url = q.get("question_media_url", "")

    # --------------------------------------------------
    # ANSWER DATA
    # --------------------------------------------------

    answer_text = q.get("answer") or "Insert your answer text here..."

    answer_media_type = q.get("answer_media_type", "")
    answer_media_url = q.get("answer_media_url", "")

    # --------------------------------------------------
    # QUESTION SECTION
    # --------------------------------------------------

    st.markdown(
        f"<div style='font-size: 1.8rem; "
        f"font-family: Rajdhani, sans-serif; "
        f"line-height: 1.4; color: #d8c9c0; "
        f"margin-bottom: 20px;'>"
        f"{question_text}</div>",
        unsafe_allow_html=True,
    )

    # Show question media
    _render_media(
        question_media_type,
        question_media_url
    )

    # --------------------------------------------------
    # ANSWER SECTION
    # --------------------------------------------------

    if can_control:

        if st.button("Reveal Answer", use_container_width=True):

            # Answer text
            st.markdown(
                f"<div style='font-size: 1.8rem; "
                f"font-family: Rajdhani, sans-serif; "
                f"color: #4CAF50; font-weight: bold; "
                f"margin-bottom: 20px;'>"
                f"{answer_text}</div>",
                unsafe_allow_html=True,
            )

            # Show answer image/audio/video
            _render_media(
                answer_media_type,
                answer_media_url
            )

        if st.button("Mark as Done & Close", use_container_width=True):
            st.session_state.board[category][tier] = False
            save_state()
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
        "🗝️ HOSTER PASSWORD:",
        HOSTER_PASSWORD,
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