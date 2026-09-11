"""
styles.py
---------
Injects the global dark-theme CSS into the Streamlit app.
Keeping all CSS in one place makes it easy to tweak the look without
hunting through business-logic files.
"""

import streamlit as st


def inject_css() -> None:
    """Renders the global CSS stylesheet into the page."""
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Noto+Serif+JP:wght@600;700&family=Rajdhani:wght@500;600;700&display=swap');

/* Hide only the footer and main menu, keep the header for the sidebar toggle! */
footer {visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}

/* Lock the app from scrolling */
html, body, .stApp {
    overflow: hidden !important;
}

.stApp {
    background:
        radial-gradient(circle at 50% 0%, rgba(139,0,0,0.12) 0%, transparent 55%),
        linear-gradient(180deg, #050405 0%, #0a0606 50%, #030202 100%);
    color: #d8c9c0;
}

/* Pushed the top padding down safely */
.block-container {
    padding-top: 4.5rem !important;
    padding-bottom: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}

/* ========================================= */
/* MAIN BOARD BUTTONS & GRID                 */
/* ========================================= */

/* Point tile buttons - Equal spacing and identical sizes */
[data-testid="stMain"] div[data-testid="stColumn"] .stButton > button {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
    letter-spacing: 1px;
    background: linear-gradient(160deg, #140909, #0a0505) !important;
    color: #b7202e !important;
    border: none !important;
    border-top: 1px solid rgba(183, 32, 46, 0.35) !important;
    border-radius: 0 !important;
    height: 8vh !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] .stButton > button:hover {
    background: linear-gradient(160deg, #1e0f0f, #100808) !important;
    color: #f2c9c9 !important;
    box-shadow: inset 0 0 18px rgba(224, 48, 74, 0.35) !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] .stButton > button:disabled {
    background: rgba(10, 5, 5, 0.6) !important;
    color: rgba(183, 32, 46, 0.15) !important;
    box-shadow: none !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] .stButton > button:disabled:hover {
    background: rgba(10, 5, 5, 0.6) !important;
    color: rgba(183, 32, 46, 0.15) !important;
    border: none !important;
    border-top: 1px solid rgba(183, 32, 46, 0.35) !important;
    box-shadow: none !important;
    transform: none !important;
    transition: none !important;
}

/* Grid columns layout */
[data-testid="stMain"] div[data-testid="stColumn"] {
    border-right: 1px solid rgba(183, 32, 46, 0.35);
    border-bottom: 1px solid rgba(183, 32, 46, 0.35);
    padding: 0 !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:first-child {
    border-left: 1px solid rgba(183, 32, 46, 0.35);
}
[data-testid="stMain"] div[data-testid="stHorizontalBlock"] {
    border-top: 1px solid rgba(183, 32, 46, 0.35);
    gap: 0 !important;
}

/* ========================================= */
/* LOGIN PAGE BORDER OVERRIDE (COVER PAGE)   */
/* ========================================= */
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(img),
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(input) {
    border: none !important;
}

[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(img) div[data-testid="stColumn"],
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(input) div[data-testid="stColumn"] {
    border: none !important;
}

/* ── Button hover alignment fix ──────────────────────────────────────────── */
[data-testid="stMain"] div[data-testid="stColumn"] > div,
[data-testid="stMain"] div[data-testid="stColumn"] > div > div,
[data-testid="stMain"] div[data-testid="stColumn"] > div > div > div {
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="stVerticalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="element-container"] {
    padding: 0 !important;
    margin: 0 !important;
    line-height: 0 !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] .stButton {
    display: block !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    line-height: 0 !important;
}

[data-testid="stMain"] .stMarkdown {
    width: 100% !important;
}
[data-testid="stMain"] .stMarkdown p {
    margin-bottom: 0 !important;
}

/* ========================================= */
/* SIDEBAR TWEAKS                            */
/* ========================================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0606 0%, #030202 100%);
    border-right: 1px solid rgba(183, 32, 46, 0.25);
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h1 {
    font-family: 'Cinzel', serif !important;
    color: #b7202e !important;
    font-size: 1.4rem !important;
    text-shadow: 0 0 12px rgba(183, 32, 46, 0.4);
}

div[data-baseweb="input"]:focus-within {
    box-shadow: none !important;
    border-color: rgba(183, 32, 46, 0.5) !important;
}

section[data-testid="stSidebar"] div[data-testid="stNumberInput"] label {
    display: none !important;
    height: 0 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    margin-top: -1px !important;
}

hr, div[data-testid="stMarkdownContainer"] hr {
    border-color: rgba(183, 32, 46, 0.2) !important;
}

/* ========================================= */
/* DIALOG / MODAL BOX TWEAKS                 */
/* ========================================= */

/* 1. Target the absolute outermost dialog tag and wrapper */
dialog, 
[data-testid="stDialog"], 
.stDialog {
    width: 95vw !important;
    max-width: 95vw !important;
    min-width: 95vw !important;
    background: transparent !important;
    /* 🎯 FORCE TRUE GEOMETRIC CENTERING 🎯 */
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 !important;
}

/* 2. Target the immediate inner wrapper that actually holds the content */
dialog > div,
[data-testid="stDialog"] > div,
div[role="dialog"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    min-height: 85vh !important;
    background: linear-gradient(160deg, #120a0a, #050303) !important;
    border: 1px solid rgba(183, 32, 46, 0.4) !important;
    box-shadow: 0 0 50px rgba(139, 0, 0, 0.35) !important;
}

/* 3. The true culprit: Streamlit's deeply hidden content blocks */
dialog .block-container,
dialog [data-testid="stVerticalBlock"],
[data-testid="stDialog"] .block-container,
[data-testid="stDialog"] [data-testid="stVerticalBlock"],
[data-testid="stDialog"] [data-testid="stVerticalBlock"] > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

/* ========================================= */
/* HEADER TEXT FIXES                         */
/* ========================================= */
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type {
    align-items: stretch !important;
}

[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"] {
    height: auto !important;
    min-height: 90px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    padding: 6px !important;
}

[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"] p,
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="stColumn"] span {
    font-size: 0.85rem !important;
    line-height: 1.2 !important;
    text-align: center !important;
    white-space: normal !important;
    word-break: break-word !important;
}

</style>
""",
        unsafe_allow_html=True,
    )