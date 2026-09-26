"""
styles.py
---------
Injects the global dark-theme CSS into the Streamlit app.
"""

import streamlit as st

def inject_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Noto+Serif+JP:wght@600;700&family=Rajdhani:wght@500;600;700&family=Oswald:wght@300;400;500;600&display=swap');

footer {visibility: hidden !important;}
#MainMenu {visibility: hidden !important;}

html, body, .stApp {
    overflow: hidden !important;
}

/* 🔥 ENHANCED JJK CURSED ENERGY BACKGROUND */
.stApp {
    background:
        radial-gradient(ellipse at 50% -20%, rgba(155, 122, 171, 0.25) 0%, rgba(90, 62, 107, 0.15) 40%, transparent 75%),
        linear-gradient(180deg, #09050c 0%, #040205 60%, #000000 100%);
    color: #d8c9c0;
}

.block-container {
    padding-top: 4.5rem !important;
    padding-bottom: 0 !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
}

/* =====================================================================
   MAIN BOARD BUTTONS (THE SEALS) & GRID
   ===================================================================== */

[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="stButton"] button {
    background-color: #141416 !important;
    border: 1px solid rgba(58, 46, 66, 0.4) !important;
    color: #d8d3c7 !important;
    border-radius: 0px !important;
    height: 53px !important; 
    min-height: 53px !important;
    max-height: 53px !important;
    margin-top: 4px !important;
    margin-bottom: 4px !important;
    box-sizing: border-box !important;
    transition: filter 150ms ease, border-color 150ms ease, box-shadow 150ms ease !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="stButton"] button p {
    font-family: 'Oswald', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    margin: 0 !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="stButton"] button:disabled {
    background-color: rgba(216, 211, 199, 0.035) !important;
    color: #6d6862 !important;
    border-color: rgba(58, 46, 66, 0.4) !important;
    border-bottom: 1px solid rgba(58, 46, 66, 0.4) !important; 
    box-shadow: none !important;
}
[data-testid="stMain"] div[data-testid="stColumn"] [data-testid="stButton"] button:disabled p {
    color: #6d6862 !important;
}

/* Col 1, 6, 9: Orange (#B5542A) */
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(1) [data-testid="stButton"] button:not(:disabled),
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(6) [data-testid="stButton"] button:not(:disabled),
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(9) [data-testid="stButton"] button:not(:disabled) {
    border-bottom-color: color-mix(in srgb, #B5542A 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #B5542A 58%, transparent) !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(1) [data-testid="stButton"] button:not(:disabled):hover,
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(6) [data-testid="stButton"] button:not(:disabled):hover,
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(9) [data-testid="stButton"] button:not(:disabled):hover {
    border-color: #B5542A !important;
    box-shadow: inset 0 -2px 0 #B5542A, 0 0 9px color-mix(in srgb, #B5542A 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

/* Col 2 & 7: Green (#4B7F52) */
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(2) [data-testid="stButton"] button:not(:disabled),
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(7) [data-testid="stButton"] button:not(:disabled) {
    border-bottom-color: color-mix(in srgb, #4B7F52 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #4B7F52 58%, transparent) !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(2) [data-testid="stButton"] button:not(:disabled):hover,
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(7) [data-testid="stButton"] button:not(:disabled):hover {
    border-color: #4B7F52 !important;
    box-shadow: inset 0 -2px 0 #4B7F52, 0 0 9px color-mix(in srgb, #4B7F52 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

/* Col 3 & 8: Blue (#3E5468) */
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(3) [data-testid="stButton"] button:not(:disabled),
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(8) [data-testid="stButton"] button:not(:disabled) {
    border-bottom-color: color-mix(in srgb, #3E5468 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #3E5468 58%, transparent) !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(3) [data-testid="stButton"] button:not(:disabled):hover,
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(8) [data-testid="stButton"] button:not(:disabled):hover {
    border-color: #3E5468 !important;
    box-shadow: inset 0 -2px 0 #3E5468, 0 0 9px color-mix(in srgb, #3E5468 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

/* Col 4: Purple (#5A3E6B) */
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(4) [data-testid="stButton"] button:not(:disabled) {
    border-bottom-color: color-mix(in srgb, #5A3E6B 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #5A3E6B 58%, transparent) !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(4) [data-testid="stButton"] button:not(:disabled):hover {
    border-color: #5A3E6B !important;
    box-shadow: inset 0 -2px 0 #5A3E6B, 0 0 9px color-mix(in srgb, #5A3E6B 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

/* Col 5: Brown/Yellow (#8A5A2E) */
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(5) [data-testid="stButton"] button:not(:disabled) {
    border-bottom-color: color-mix(in srgb, #8A5A2E 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #8A5A2E 58%, transparent) !important;
}
[data-testid="stMain"] div[data-testid="stColumn"]:nth-child(5) [data-testid="stButton"] button:not(:disabled):hover {
    border-color: #8A5A2E !important;
    box-shadow: inset 0 -2px 0 #8A5A2E, 0 0 9px color-mix(in srgb, #8A5A2E 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

[data-testid="stMain"] div[data-testid="stColumn"] {
    padding: 0 !important;
}
[data-testid="stMain"] div[data-testid="stHorizontalBlock"] {
    gap: 8px !important;
}

/* =====================================================================
   LOGIN PAGE INPUTS & ALIGNMENT
   ===================================================================== */

[data-testid="stMain"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
[data-testid="stMain"] [data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #141416 !important;
    border: 1px solid rgba(58, 46, 66, 0.4) !important;
    border-radius: 0px !important;
    min-height: 53px !important;
    border-bottom-color: color-mix(in srgb, #4B7F52 58%, #141416) !important;
    box-shadow: inset 0 -2px 0 color-mix(in srgb, #4B7F52 58%, transparent) !important;
    transition: filter 150ms ease, border-color 150ms ease, box-shadow 150ms ease !important;
}

[data-testid="stMain"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
[data-testid="stMain"] [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: #4B7F52 !important;
    box-shadow: inset 0 -2px 0 #4B7F52, 0 0 9px color-mix(in srgb, #4B7F52 45%, transparent) !important;
    filter: brightness(1.12) !important;
}

[data-testid="stMain"] [data-testid="stSelectbox"] *, 
[data-testid="stMain"] [data-testid="stTextInput"] input {
    color: #d8d3c7 !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 15px !important;
    letter-spacing: 0.06em !important;
    background-color: transparent !important;
}

[data-testid="stMain"] [data-testid="stSelectbox"] label p,
[data-testid="stMain"] [data-testid="stTextInput"] label p {
    color: #a1a1aa !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    margin-bottom: 5px !important;
}

[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(img),
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(input) {
    border: none !important;
}

[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(img) div[data-testid="stColumn"],
[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:has(input) div[data-testid="stColumn"] {
    border: none !important;
}

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

/* =====================================================================
   TOP NAVIGATION TABS (Typography Only)
   ===================================================================== */
div[data-testid="stTabs"] {
    border-bottom: 1px solid rgba(58, 46, 66, 0.4) !important;
}

body div[id*="-tab-"],
body div[id*="-tab-"] * {
    font-family: 'Oswald', sans-serif !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #8a8580 !important;
    cursor: pointer;
}

body div[id*="-tab-"]:hover,
body div[id*="-tab-"]:hover * {
    color: #d8d3c7 !important;
}

body div[id*="-tab-"][data-selected] *,
body button[role="tab"][aria-selected="true"] * {
    color: #d8d3c7 !important;
}

/* ========================================= */
/* SIDEBAR TWEAKS (Overseer Panel)           */
/* ========================================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070508 0%, #030203 100%);
    border-right: 1px solid rgba(90, 62, 107, 0.25) !important; 
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *[style*="color:"] {
    color: #9b7aab !important;
    font-family: 'Oswald', sans-serif !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h1 {
    font-family: 'Cinzel', serif !important;
    color: #9b7aab !important; 
    font-size: 1.4rem !important;
    text-shadow: 0 0 12px rgba(90, 62, 107, 0.4) !important;
}

section[data-testid="stSidebar"] p {
    font-family: 'Rajdhani', sans-serif !important;
    color: #a1a1aa !important;
    font-size: 1.05rem !important;
}

section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background-color: #141416 !important;
    border: 1px solid rgba(90, 62, 107, 0.3) !important;
    border-radius: 4px !important;
    height: auto !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
    box-shadow: none !important;
    border-color: #5A3E6B !important;
}
section[data-testid="stSidebar"] div[data-baseweb="input"] input {
    color: #d8d3c7 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

section[data-testid="stSidebar"] div[data-testid="stNumberInput"] label {
    display: none !important;
    height: 0 !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background-color: #141416 !important;
    border: 1px solid rgba(90, 62, 107, 0.4) !important;
    color: #d8d3c7 !important;
    border-radius: 4px !important;
    transition: all 0.2s ease;
    margin-top: -1px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #5A3E6B !important;
    box-shadow: 0 0 10px rgba(90, 62, 107, 0.4) !important;
    color: #fff !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background-color: #0b070d !important;
    border: 1px solid rgba(90, 62, 107, 0.3) !important;
    border-radius: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    font-family: 'Rajdhani', sans-serif !important;
    color: #d8d3c7 !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    color: #9b7aab !important;
}

section[data-testid="stSidebar"] [data-testid="stProgress"] > div > div {
    background-color: #5A3E6B !important;
}

hr, div[data-testid="stMarkdownContainer"] hr {
    border-color: rgba(90, 62, 107, 0.2) !important;
}

/* ========================================= */
/* DIALOG / MODAL BOX TWEAKS                 */
/* ========================================= */
dialog, 
[data-testid="stDialog"], 
.stDialog {
    width: 95vw !important;
    max-width: 95vw !important;
    min-width: 95vw !important;
    background: transparent !important;
    position: fixed !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    margin: 0 !important;
}

dialog > div,
[data-testid="stDialog"] > div,
div[role="dialog"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
    min-height: 85vh !important;
    background: linear-gradient(160deg, #0b070d, #050305) !important;
    border: 1px solid rgba(90, 62, 107, 0.4) !important;
    box-shadow: 0 0 50px rgba(90, 62, 107, 0.35) !important;
}

dialog .block-container,
dialog [data-testid="stVerticalBlock"],
[data-testid="stDialog"] .block-container,
[data-testid="stDialog"] [data-testid="stVerticalBlock"],
[data-testid="stDialog"] [data-testid="stVerticalBlock"] > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 100% !important;
}

div[role="dialog"] header h2,
div[role="dialog"] div[data-testid="stDialogHeader"] h2,
div[role="dialog"] div[role="heading"] {
    font-family: 'Cinzel', serif !important;
    color: #9b7aab !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-size: 1.4rem !important;
}

/* 🔥 UNIVERSAL INLINE-RED OVERRIDE FOR ALL QUESTION HEADINGS INSIDE MODALS */
div[role="dialog"] div[data-testid="stMarkdownContainer"] h1,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h2,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h3,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h4,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h1 *,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h2 *,
div[role="dialog"] div[data-testid="stMarkdownContainer"] h3 *,
div[role="dialog"] div[data-testid="stMarkdownContainer"] div[style*="color:"],
div[role="dialog"] div[data-testid="stMarkdownContainer"] span[style*="color:"],
div[role="dialog"] div[data-testid="stMarkdownContainer"] font[color] {
    color: #9b7aab !important; 
    font-family: 'Cinzel', serif !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    text-align: center !important;
    font-size: 2.3rem !important; 
    text-shadow: 0 0 20px rgba(155, 122, 171, 0.45) !important;
    border: none !important;
    background: transparent !important;
}

/* Transform the red divider line under question headings into a muted purple glow line */
div[role="dialog"] div[data-testid="stMarkdownContainer"] hr {
    border-color: rgba(90, 62, 107, 0.6) !important;
    border-bottom: 2px solid rgba(155, 122, 171, 0.4) !important;
    border-top: none !important;
    background-color: transparent !important;
    box-shadow: 0 0 10px rgba(90, 62, 107, 0.3) !important;
    margin-top: 15px !important;
    margin-bottom: 25px !important;
}

/* SAFEGUARD: Keep the actual question body text untouched (Rajdhani beige) */
div[role="dialog"] div[data-testid="stMarkdownContainer"] p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.4rem !important;
    color: #d8d3c7 !important; 
    text-align: center !important;
    line-height: 1.6 !important;
}

div[role="dialog"] button[kind="header"] {
    color: #9b7aab !important;
    transition: color 0.2s ease;
}
div[role="dialog"] button[kind="header"]:hover {
    color: #d8c9c0 !important;
    background: transparent !important;
}

div[role="dialog"] .stButton > button {
    background-color: #0b070d !important;
    border: 1px solid rgba(90, 62, 107, 0.6) !important;
    color: #d8c9c0 !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.08em !important;
    border-radius: 4px !important;
    text-transform: uppercase !important;
    padding: 15px !important;
    margin-top: 20px !important;
    transition: all 0.2s ease !important;
}
div[role="dialog"] .stButton > button:hover {
    border-color: #9b7aab !important;
    background-color: #141416 !important;
    box-shadow: 0 0 20px rgba(90, 62, 107, 0.4) !important;
    color: #ffffff !important;
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

/* =====================================================================
   RULES & ITEMS SAFE STYLING 
   ===================================================================== */
div[data-testid="stTabs"] .stMarkdown h3 {
    font-family: 'Oswald', sans-serif !important;
    color: #9b7aab !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-size: 1.4rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

div[data-testid="stTabs"] .stMarkdown ul,
div[data-testid="stTabs"] .stMarkdown ol,
div[data-testid="stTabs"] .stMarkdown li {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.15rem !important;
    color: #a1a1aa !important;
    line-height: 1.6 !important;
    letter-spacing: 0.03em !important;
}

div[data-testid="stTabs"] .stMarkdown strong {
    color: #d8d3c7 !important;
    font-weight: 700 !important;
}

div[data-testid="stTabs"] .stMarkdown table {
    border-collapse: collapse !important;
    width: 100% !important;
    margin-top: 15px !important;
}
div[data-testid="stTabs"] .stMarkdown th {
    font-family: 'Oswald', sans-serif !important;
    color: #9b7aab !important;
    text-transform: uppercase !important;
    font-size: 1.1rem !important;
    border-bottom: 2px solid rgba(90, 62, 107, 0.5) !important;
    padding: 12px 8px !important;
    text-align: left !important;
}
div[data-testid="stTabs"] .stMarkdown td {
    font-family: 'Rajdhani', sans-serif !important;
    color: #a1a1aa !important;
    border-bottom: 1px solid rgba(90, 62, 107, 0.2) !important;
    padding: 12px 8px !important;
}
</style>
""",
        unsafe_allow_html=True,
    )