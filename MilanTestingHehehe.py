import streamlit as st
import pandas as pd
import json
import os

# 1. Setup Page Layout
st.set_page_config(page_title="Milan Quiz: Anime Jeopardy", layout="wide", page_icon="⚔️")

CATEGORIES = [
    "Quotes", "Pee Pee poo poo hard", "I can't read",
    "Where is Zoro?", "Where are the pixels?????",
    "Truck Kun's hitlist", "Inumaki's Spotify playlist",
    "Chika Fujiwara photo", "Japanese Culture"
]
TIERS = [200, 400, 600, 800, 1000, 1500]
TEAMS = ["Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6", "Team 7", "Team 8"]
MAX_CE = 4000

TEAM_COLORS = [
    "#8B0000", "#4A0E0E", "#B7202E", "#6E1414",
    "#9E1B1B", "#701212", "#A62639", "#5C0F0F"
]

# --- LOGIN CREDENTIALS ---
ADMIN_PASSWORD = "goatakuclub@milan2026"  

TEAM_PASSWORDS = {
    "Team 1": "hollow@purple2026",
    "Team 2": "black@flash2026",
    "Team 3": "ten@shadows2026",
    "Team 4": "infinite@void2026",
    "Team 5": "malevolent@shrine26",
    "Team 6": "idle@death2026",
    "Team 7": "heavenly@pact2026",
    "Team 8": "cursed@speech2026",
}

# --- BACKEND SAVING SYSTEM ---
STATE_FILE = "/Users/illen/Documents/MilanYareYare/milan_quiz_state.json"

def load_state():
    """Reads the saved game state from the JSON file if it exists."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            # JSON converts integer keys to strings. We must convert the tier keys back to ints!
            fixed_board = {cat: {int(tier): val for tier, val in tiers.items()} for cat, tiers in data["board"].items()}
            return {"ce": data["ce"], "board": fixed_board}
    return None

def save_state():
    """Saves the current session state to a neatly formatted JSON file."""
    state = {
        "ce": st.session_state.ce,
        "board": st.session_state.board
    }
    with open(STATE_FILE, "w") as f:
        # Added indent=4 here! This makes the file perfectly readable for humans.
        json.dump(state, f, indent=4)

# 2. Session State Init (With Backend Memory)
loaded_state = load_state()

if "ce" not in st.session_state:
    if loaded_state:
        st.session_state.ce = loaded_state["ce"]
    else:
        st.session_state.ce = {team: MAX_CE for team in TEAMS}

if "board" not in st.session_state:
    if loaded_state:
        st.session_state.board = loaded_state["board"]
    else:
        st.session_state.board = {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}

if "mode" not in st.session_state:
    st.session_state.mode = None  


# 3. Global Theme CSS
st.markdown("""
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
/* MAIN BOARD BUTTONS                        */
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
    height: 7.5vh !important;    
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
[data-testid="stMain"] div[data-testid="stColumn"] > div > div > div > div {
    gap: 0 !important;
}

/* Eliminating Streamlit's stubborn padding on markdown blocks */
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

/* Target and destroy the orange focus ring in the number input artifact */
div[data-baseweb="input"]:focus-within {
    box-shadow: none !important;
    border-color: rgba(183, 32, 46, 0.5) !important;
}

/* Kills the hidden label from pushing down the number input */
section[data-testid="stSidebar"] div[data-testid="stNumberInput"] label {
    display: none !important;
    height: 0 !important;
}

/* Ensure the Apply button aligns naturally without weird height overrides */
section[data-testid="stSidebar"] .stButton > button {
    margin-top: -1px !important;
}

hr, div[data-testid="stMarkdownContainer"] hr {
    border-color: rgba(183, 32, 46, 0.2) !important;
}

/* Dialog box */
div[role="dialog"] {
    background: linear-gradient(160deg, #120a0a, #050303) !important;
    border: 1px solid rgba(183, 32, 46, 0.4);
    box-shadow: 0 0 50px rgba(139, 0, 0, 0.35);
}
</style>
""", unsafe_allow_html=True)


# 3.5 MULTI-ACCOUNT LOGIN GATE
if st.session_state.mode is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='font-size:2.2rem !important; font-family: Cinzel, serif; color: #b7202e; text-align: center; margin-bottom: 20px;'>Select Your Identity</h1>",
        unsafe_allow_html=True
    )
    
    left, mid, right = st.columns([1, 1.5, 1])
    with mid:
        try:
            st.image("/Users/illen/Documents/MilanYareYare/Theme.png", use_container_width=True)
        except Exception:
            st.markdown(
                "<div style='text-align: center; color: #8a4a4a; padding: 20px; border: 1px dashed #8a4a4a; margin-bottom: 15px;'>"
                "[ Culling Game Image Not Found - Place Theme.png in the folder ]"
                "</div>", 
                unsafe_allow_html=True
            )

        roles = ["Audience (View Only)", "Colony Overseer (Admin)"] + TEAMS
        choice = st.selectbox("Who are you?", roles, label_visibility="collapsed")
        
        if choice == "Audience (View Only)":
            if st.button("Enter the Culling Game", use_container_width=True):
                st.session_state.mode = "audience"
                st.rerun()
        else:
            pw = st.text_input("Enter Password", type="password")
            if st.button("Authenticate", use_container_width=True):
                if choice == "Colony Overseer (Admin)" and pw == ADMIN_PASSWORD:
                    st.session_state.mode = "admin"
                    st.rerun()
                elif choice in TEAMS:
                    if pw == TEAM_PASSWORDS.get(choice):
                        st.session_state.mode = choice
                        st.rerun()
                    else:
                        st.error("Incorrect Cursed Energy Signature (Wrong Password).")
                else:
                    st.error("Incorrect Cursed Energy Signature (Wrong Password).")
    st.stop()


def ce_bar_html(team, ce, color):
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


IS_ADMIN = st.session_state.mode == "admin"
LOGGED_IN_TEAM = st.session_state.mode if st.session_state.mode in TEAMS else None

# --- CREDENTIALS DOCUMENT GENERATOR ---
def generate_credentials_file():
    doc = "========================================\n"
    doc += "⚔️ MILAN QUIZ: CULLING GAME CREDENTIALS ⚔️\n"
    doc += "========================================\n\n"
    doc += "⛩️ COLONY OVERSEER (ADMIN) PASSWORD:\n"
    doc += f"{ADMIN_PASSWORD}\n\n"
    doc += "----------------------------------------\n"
    doc += "🩸 TEAM PASSWORDS:\n"
    for team, pw in TEAM_PASSWORDS.items():
        doc += f"{team}:  {pw}\n"
    doc += "----------------------------------------\n"
    doc += "Keep this document secure. Let the Culling Game begin."
    return doc


# 4. Question Dialog - UPDATED FOR PROJECTOR VISIBILITY
@st.dialog("Question")
def show_question(category, tier):
    
    # Huge Header for the Category and CE
    st.markdown(
        f"<div style='font-size: 2.2rem; font-family: Cinzel, serif; color: #b7202e; border-bottom: 2px solid #8B0000; padding-bottom: 10px; margin-bottom: 20px;'>{category} — {tier} CE</div>",
        unsafe_allow_html=True
    )
    
    # Massive text for the actual question
    st.markdown(
        "<div style='font-size: 1.8rem; font-family: Rajdhani, sans-serif; line-height: 1.4; color: #d8c9c0; margin-bottom: 30px;'>Insert your question text here...</div>", 
        unsafe_allow_html=True
    )

    if IS_ADMIN:
        if st.button("Reveal Answer", use_container_width=True):
            # Beautiful, bright text for the answer so it stands out
            st.markdown(
                "<div style='font-size: 1.8rem; font-family: Rajdhani, sans-serif; color: #4CAF50; font-weight: bold; margin-bottom: 20px;'>Insert your answer text here...</div>", 
                unsafe_allow_html=True
            )

        if st.button("Mark as Done & Close", use_container_width=True):
            st.session_state.board[category][tier] = False
            save_state()  # Instantly saves the board state to the backend!
            st.rerun()
    else:
        st.info("Waiting for the mediator to reveal the answer...")


# 5. Sidebar: Dashboard
with st.sidebar:
    if IS_ADMIN:
        st.header("⛩️ Colony Overseer")
        st.caption("Manage cursed energy (CE), damage, and healing here.")
        
        st.download_button(
            label="📄 Download Passwords",
            data=generate_credentials_file(),
            file_name="Culling_Game_Passwords.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.divider()

        for team, color in zip(TEAMS, TEAM_COLORS):
            st.markdown(ce_bar_html(team, st.session_state.ce[team], color), unsafe_allow_html=True)
            
            col1, col2 = st.columns([1.5, 1], gap="small")
            with col1:
                adj_val = st.number_input(f"Adjust {team}", value=0, step=100, key=f"adj_{team}",
                                           label_visibility="collapsed")
            with col2:
                if st.button("Apply", key=f"btn_{team}", use_container_width=True):
                    st.session_state.ce[team] = max(0, st.session_state.ce[team] + adj_val)
                    save_state() # Instantly saves the new CE to the backend!
                    st.rerun()

        st.divider()
        if st.button("🚨 Reset Entire Game", use_container_width=True):
            st.session_state.ce = {team: MAX_CE for team in TEAMS}
            st.session_state.board = {cat: {tier: True for tier in TIERS} for cat in CATEGORIES}
            save_state() # Overwrites the backend with a fresh game
            st.rerun()
            
    else:
        if LOGGED_IN_TEAM:
            st.header(f"🗡️ {LOGGED_IN_TEAM} Terminal")
            st.caption("Your team is active. Awaiting your turn.")
        else:
            st.header("🩸 Audience View")
            st.caption("Live cursed energy — read only")
            
        st.divider()
        for team, color in zip(TEAMS, TEAM_COLORS):
            st.markdown(ce_bar_html(team, st.session_state.ce[team], color), unsafe_allow_html=True)

    st.divider()
    if st.button("🔁 Switch Mode / Log Out", use_container_width=True):
        st.session_state.mode = None
        st.rerun()

# 6. Main Board UI
st.markdown(
    "<h1 style='font-size: 2.8rem !important; text-align: center; color: #b7202e; font-family: Cinzel, serif; letter-spacing: 4px; text-shadow: 0 0 25px rgba(183, 32, 46, 0.55); margin-bottom: 0px;'>殺戮 CULLING GAME 殺戮</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#8a4a4a; font-family:Rajdhani, sans-serif; "
    "font-weight:600; letter-spacing:3px; margin-top:2px; margin-bottom:12px;'>SURVIVE THE ROUNDS — MILAN QUIZ EDITION</p>",
    unsafe_allow_html=True
)

cols = st.columns(len(CATEGORIES))

for i, category in enumerate(CATEGORIES):
    with cols[i]:
        # INLINE HTML: This absolutely forces the header text to perfectly center and prevents spilling!
        header_html = f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: rgba(183, 32, 46, 0.08);
            border-bottom: 2px solid rgba(183, 32, 46, 0.5);
            height: 5.5vh;
            width: 100%;
            margin: 0;
            padding: 0 2px;
            overflow: hidden;
        ">
            <span style="
                font-family: 'Rajdhani', sans-serif;
                font-weight: 700;
                color: #c9a0a0;
                text-transform: uppercase;
                font-size: 0.78rem;
                line-height: 1.1;
                display: block;
                width: 100%;
                word-wrap: break-word;
            ">{category}</span>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        
        for tier in TIERS:
            is_active = st.session_state.board[category][tier]
            if is_active:
                if st.button(f"{tier} CE", key=f"{category}_{tier}", use_container_width=True):
                    show_question(category, tier)
            else:
                st.button("✖", key=f"{category}_{tier}_done", disabled=True, use_container_width=True)