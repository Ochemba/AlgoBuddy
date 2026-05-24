import streamlit as st
import time
import streamlit.components.v1 as _components

st.set_page_config(page_title="AlgoBuddy", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

# AUDIO EDIT 1: added generate_tts_audio to import
from tutor_engine import get_tutor_response, clear_conversation, set_conversation_history, generate_tts_audio
from course_registry import get_course, get_topic
from validators import validate_user_message, ValidationError
from auth import AuthManager
from chat_history import new_session_id, save_session, load_all_sessions, load_session, delete_session, format_session_date

# Import shared cache
from shared_cache import (
    get_courses, get_personas, get_course_list, get_course_labels,
    get_topics_for_course, get_topic_display, get_course_display,
    get_avatar_map, clear_all_caches
)

_auth = AuthManager()

# Use cached data
COURSES = get_courses()
PERSONAS = get_personas()
COURSE_KEYS = get_course_list()
COURSE_LABELS = get_course_labels()
AVATAR = get_avatar_map()

# ============================================
# COMPLETE CSS (YOUR ORIGINAL - KEPT INTACT)
# ============================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --navy: #060B2B;
    --n2: #0D1547;
    --n3: #1B2B6B;
    --teal: #06B6D4;
    --tg: rgba(6, 182, 212, 0.15);
    --tb: rgba(6, 182, 212, 0.3);
    --g1: rgba(255, 255, 255, 0.05);
    --g2: rgba(255, 255, 255, 0.09);
    --t1: #EEF2FF;
    --t2: #A8B4D8;
    --t3: #5A6A9A;
    --font: 'Plus Jakarta Sans', sans-serif;
    --mono: 'JetBrains Mono', monospace;
}

/* Base styles */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    color: var(--t1) !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none !important;
}

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #060B2B 0%, #0D1547 55%, #182060 100%) !important;
    min-height: 100vh;
}

/* Responsive container */
@media (max-width: 768px) {
    .block-container {
        padding: 0 !important;
    }
}

/* Auth inputs */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active,
[data-testid="stTextInput"] input:not([disabled]) {
    background: #0f1d5e !important;
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
    caret-color: #06B6D4 !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.15) !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: rgba(168, 180, 216, 0.5) !important;
    -webkit-text-fill-color: rgba(168, 180, 216, 0.5) !important;
}

[data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stTextInput"] div[style] {
    background: #0f1d5e !important;
}

[data-testid="stTextInput"] label {
    color: #A8B4D8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* Auth layout */
.auth-logo {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    justify-content: center;
    margin-bottom: 1.8rem;
}

.auth-logo-icon {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #1B2B6B, #06B6D4);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.auth-sub {
    font-size: 0.88rem;
    color: #A8B4D8;
    text-align: center;
    margin-bottom: 1.6rem;
}

.auth-tabs {
    display: flex;
    gap: 0;
    margin-bottom: 1.8rem;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.auth-tab {
    flex: 1;
    padding: 0.55rem 0;
    text-align: center;
    font-size: 0.88rem;
    font-weight: 600;
    color: #A8B4D8;
    background: rgba(255, 255, 255, 0.03);
}

.auth-tab.active {
    background: rgba(6, 182, 212, 0.18);
    color: #06B6D4;
    border-bottom: 2px solid #06B6D4;
}

/* Navbar - responsive */
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
    background: rgba(6, 11, 43, 0.95) !important;
    backdrop-filter: blur(18px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
    padding: 0.55rem 1rem !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 500 !important;
    margin-bottom: 0 !important;
    align-items: center !important;
    flex-wrap: wrap !important;
}

@media (max-width: 768px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
        padding: 0.55rem 0.75rem !important;
    }
}

section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
    display: flex !important;
    align-items: center !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    gap: 0 !important;
}

@media (max-width: 768px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        min-width: auto !important;
        width: auto !important;
    }
}

section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"] .element-container,
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .element-container {
    margin: 0 !important;
    width: 100%;
}

/* Pill buttons */
.ab-pill-btn .stButton>button,
.ab-pill-btn .stButton>button:focus {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 20px !important;
    font-family: var(--font) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--teal) !important;
    padding: 0.25rem 0.85rem !important;
    box-shadow: none !important;
    min-height: 0 !important;
    height: 28px !important;
    white-space: nowrap !important;
    transition: all 0.15s !important;
}

@media (max-width: 480px) {
    .ab-pill-btn .stButton>button,
    .ab-pill-btn .stButton>button:focus {
        font-size: 0.7rem !important;
        padding: 0.2rem 0.6rem !important;
        height: 24px !important;
    }
}

.ab-pill-btn .stButton>button:hover {
    background: rgba(6, 182, 212, 0.15) !important;
    border-color: var(--teal) !important;
    transform: none !important;
}

.ab-pill-btn {
    display: inline-flex;
    align-items: center;
}

/* Avatar */
.ab-avatar-circle {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1B2B6B, #06B6D4);
    border: 2px solid rgba(6, 182, 212, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    color: #fff;
}

@media (max-width: 480px) {
    .ab-avatar-circle {
        width: 26px;
        height: 26px;
        font-size: 0.65rem;
    }
}

/* Selectbox */
[data-testid="stSelectbox"] label,
[data-testid="stTextArea"] label {
    color: var(--t2) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

[data-testid="stToggle"] *,
[data-baseweb="checkbox"] * {
    color: var(--t2) !important;
    font-size: 0.85rem !important;
}

[data-testid="stExpander"] label,
[data-testid="stExpander"] p {
    color: var(--t2) !important;
}

[data-testid="stExpander"] [data-testid="stTextInput"] input {
    background: #0f1d5e !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: var(--t1) !important;
    -webkit-text-fill-color: var(--t1) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: var(--t2) !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
    background: #dbeafe !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 10px !important;
    color: #1e3a5f !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] svg {
    color: #1e3a5f !important;
    fill: #1e3a5f !important;
}

html body [role="option"],
html body [role="option"] * {
    color: #0f172a !important;
    background-color: #f8fafc !important;
    font-family: var(--font) !important;
    font-size: 0.88rem !important;
}

html body [role="option"]:hover {
    background-color: #e2e8f0 !important;
    color: #0f172a !important;
}

html body [role="option"][aria-selected="true"] {
    background-color: #bae6fd !important;
    color: #0c4a6e !important;
    font-weight: 600 !important;
    border-left: 3px solid #06B6D4 !important;
}

html body [role="option"][aria-selected="true"] * {
    color: #0c4a6e !important;
    background-color: transparent !important;
}

/* Home cards - responsive grid */
.ab-home {
    max-width: 100%;
    padding: 2rem 1rem 8rem;
}

@media (max-width: 768px) {
    .ab-home {
        padding: 1.5rem 0.75rem 8rem;
    }
}

@media (max-width: 480px) {
    .ab-home {
        padding: 1rem 0.5rem 8rem;
    }
}

.ab-hero {
    text-align: center;
    padding: 0.5rem 1rem 2rem;
}

@media (max-width: 768px) {
    .ab-hero {
        padding: 0.5rem 0.5rem 1.5rem;
    }
}

.ab-hero-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #1B2B6B, #06B6D4);
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin: 0 auto 1.1rem;
    box-shadow: 0 0 40px rgba(6, 182, 212, 0.28);
}

@media (max-width: 768px) {
    .ab-hero-icon {
        width: 56px;
        height: 56px;
        font-size: 1.6rem;
        margin-bottom: 0.8rem;
    }
}

@media (max-width: 480px) {
    .ab-hero-icon {
        width: 48px;
        height: 48px;
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }
}

.ab-hero-h {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #fff;
    margin-bottom: 0.4rem;
}

@media (max-width: 768px) {
    .ab-hero-h {
        font-size: 1.6rem;
    }
}

@media (max-width: 480px) {
    .ab-hero-h {
        font-size: 1.3rem;
    }
}

.hl {
    background: linear-gradient(90deg, #93C5FD, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.ab-hero-sub {
    font-size: 0.95rem;
    color: var(--t2);
}

@media (max-width: 768px) {
    .ab-hero-sub {
        font-size: 0.85rem;
    }
}

@media (max-width: 480px) {
    .ab-hero-sub {
        font-size: 0.8rem;
    }
}

/* Cards - responsive grid */
.ab-card-body {
    background: var(--g1);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: none;
    border-radius: 14px 14px 0 0;
    padding: 1.5rem 1.2rem 1rem;
    transition: background 0.2s, border-color 0.2s;
    flex: 1;
}

@media (max-width: 768px) {
    .ab-card-body {
        padding: 1.2rem 1rem 0.8rem;
    }
}

@media (max-width: 480px) {
    .ab-card-body {
        padding: 1rem 0.8rem 0.7rem;
    }
}

.ab-card-body:hover {
    background: var(--g2);
    border-color: rgba(6, 182, 212, 0.28);
}

.ab-card-ico {
    font-size: 1.5rem;
    margin-bottom: 0.65rem;
}

@media (max-width: 768px) {
    .ab-card-ico {
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }
}

.ab-card-t {
    font-size: 0.97rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.3rem;
}

@media (max-width: 768px) {
    .ab-card-t {
        font-size: 0.9rem;
    }
}

.ab-card-d {
    font-size: 0.81rem;
    color: var(--t2);
    line-height: 1.55;
    margin-bottom: 0.55rem;
}

@media (max-width: 768px) {
    .ab-card-d {
        font-size: 0.75rem;
        line-height: 1.45;
    }
}

.ab-card-hint {
    font-size: 0.71rem;
    color: var(--teal);
    font-weight: 500;
}

@media (max-width: 768px) {
    .ab-card-hint {
        font-size: 0.65rem;
    }
}

.ab-cu-btn .stButton>button {
    background: var(--g1) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    color: var(--teal) !important;
    font-family: var(--font) !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    box-shadow: none !important;
}

@media (max-width: 768px) {
    .ab-cu-btn .stButton>button {
        font-size: 0.75rem !important;
        padding: 0.5rem 0.8rem !important;
    }
}

.ab-cu-btn .stButton>button:hover {
    background: rgba(255, 255, 255, 0.09) !important;
    border-color: rgba(6, 182, 212, 0.3) !important;
    transform: none !important;
}

.ab-cu-btn,
.ab-cu-btn>div,
.ab-cu-btn .element-container,
.ab-cu-btn .stButton {
    margin: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
}

/* Responsive grid for cards */
@media (max-width: 992px) {
    .ab-home .stHorizontalBlock {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 1rem !important;
    }
    
    .ab-home .stHorizontalBlock [data-testid="stColumn"] {
        width: 100% !important;
        min-width: 0 !important;
        flex: none !important;
        margin-bottom: 0 !important;
    }
}

@media (max-width: 768px) {
    .ab-home .stHorizontalBlock {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 0.75rem !important;
        padding: 0 0.5rem !important;
    }
}

@media (max-width: 560px) {
    .ab-home .stHorizontalBlock {
        grid-template-columns: 1fr !important;
        gap: 0.75rem !important;
    }
    
    .ab-home .stHorizontalBlock [data-testid="stColumn"] {
        margin-bottom: 0 !important;
    }
}

.ab-home .stHorizontalBlock {
    margin: 0 !important;
}

.ab-home .stHorizontalBlock [data-testid="stColumn"] > div {
    height: 100% !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Chat */
.ab-ctx-tag {
    font-size: 0.73rem;
    color: var(--teal);
    background: var(--tg);
    border: 1px solid var(--tb);
    border-radius: 20px;
    padding: 0.15rem 0.7rem;
    font-weight: 500;
    white-space: nowrap;
}

@media (max-width: 768px) {
    .ab-ctx-tag {
        font-size: 0.65rem;
        padding: 0.1rem 0.5rem;
    }
}

@media (max-width: 480px) {
    .ab-ctx-tag {
        font-size: 0.6rem;
        padding: 0.08rem 0.45rem;
    }
}

.ab-chat-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 1rem 4% 14rem;
    box-sizing: border-box;
    width: 100%;
}

@media (max-width: 768px) {
    .ab-chat-wrap {
        padding: 0.5rem 3% 14rem;
    }
}

@media (max-width: 480px) {
    .ab-chat-wrap {
        padding: 0.3rem 2% 14rem;
    }
}

.ab-row-b {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    margin-bottom: 1rem;
    width: 100%;
}

@media (max-width: 480px) {
    .ab-row-b {
        gap: 0.4rem;
    }
}

.ab-row-u {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 0.6rem;
    margin-bottom: 1rem;
    width: 100%;
}

@media (max-width: 480px) {
    .ab-row-u {
        gap: 0.4rem;
    }
}

.ab-bu {
    background: #1B2B6B;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #EEF2FF;
    padding: 0.7rem 1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 65%;
    min-width: 0;
    font-size: 0.93rem;
    line-height: 1.6;
    overflow-wrap: break-word;
    word-break: break-word;
}

@media (max-width: 768px) {
    .ab-bu {
        font-size: 0.87rem;
        padding: 0.6rem 0.9rem;
        max-width: 75%;
    }
}

@media (max-width: 480px) {
    .ab-bu {
        font-size: 0.84rem;
        padding: 0.5rem 0.8rem;
        max-width: 82%;
    }
}

.ab-bb {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #EEF2FF;
    padding: 0.85rem 1.1rem;
    border-radius: 4px 18px 18px 18px;
    max-width: calc(100% - 44px);
    font-size: 0.93rem;
    line-height: 1.72;
    overflow-wrap: break-word;
    word-break: break-word;
}

@media (max-width: 768px) {
    .ab-bb {
        font-size: 0.87rem;
        padding: 0.7rem 1rem;
    }
}

@media (max-width: 480px) {
    .ab-bb {
        font-size: 0.84rem;
        padding: 0.6rem 0.9rem;
        max-width: calc(100% - 36px);
    }
}

.ab-bb code {
    font-family: var(--mono);
    background: rgba(6, 182, 212, 0.15);
    color: #67E8F9;
    padding: 0.1em 0.4em;
    border-radius: 4px;
    font-size: 0.85em;
}

.ab-bb pre {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #C4D4FF;
    border-radius: 10px;
    padding: 0.9rem;
    overflow-x: auto;
    font-family: var(--mono);
    font-size: 0.82em;
    line-height: 1.5;
    margin: 0.55rem 0;
}

@media (max-width: 768px) {
    .ab-bb pre {
        padding: 0.6rem;
        font-size: 0.75em;
    }
}

.ab-av {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1B2B6B, #06B6D4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    flex-shrink: 0;
}

@media (max-width: 480px) {
    .ab-av {
        width: 26px;
        height: 26px;
        font-size: 0.7rem;
    }
}

.ab-uav {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #243580;
    border: 1px solid rgba(255, 255, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.73rem;
    color: #fff;
    font-weight: 700;
    flex-shrink: 0;
}

@media (max-width: 480px) {
    .ab-uav {
        width: 24px;
        height: 24px;
        font-size: 0.65rem;
    }
}

.ab-ts {
    font-size: 0.64rem;
    color: var(--t3);
    margin-top: 0.25rem;
    padding: 0 0.25rem;
}

@media (max-width: 480px) {
    .ab-ts {
        font-size: 0.58rem;
    }
}

.practice-cta .stButton>button {
    background: rgba(6, 182, 212, 0.1) !important;
    color: var(--teal) !important;
    -webkit-text-fill-color: var(--teal) !important;
    border: 1px solid rgba(6, 182, 212, 0.35) !important;
    border-radius: 20px !important;
    font-family: var(--font) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    height: 28px !important;
    padding: 0 0.9rem !important;
    white-space: nowrap !important;
    box-shadow: none !important;
    width: auto !important;
}

@media (max-width: 480px) {
    .practice-cta .stButton>button {
        font-size: 0.7rem !important;
        height: 24px !important;
        padding: 0 0.6rem !important;
    }
}

.practice-cta .stButton>button:hover {
    background: rgba(6, 182, 212, 0.2) !important;
    border-color: var(--teal) !important;
    transform: none !important;
}

/* File badge */
.file-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(6, 182, 212, 0.1);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 20px;
    padding: 0.18rem 0.7rem;
    font-size: 0.72rem;
    color: var(--teal);
    font-weight: 600;
}

@media (max-width: 480px) {
    .file-badge {
        font-size: 0.65rem;
        padding: 0.12rem 0.5rem;
    }
}

.remove-file-btn .stButton>button {
    background: rgba(239, 68, 68, 0.08) !important;
    color: #f87171 !important;
    -webkit-text-fill-color: #f87171 !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
    border-radius: 8px !important;
    font-family: var(--font) !important;
    font-size: 0.72rem !important;
    height: 24px !important;
    padding: 0 0.6rem !important;
    box-shadow: none !important;
    width: auto !important;
}

@media (max-width: 480px) {
    .remove-file-btn .stButton>button {
        font-size: 0.65rem !important;
        height: 22px !important;
        padding: 0 0.5rem !important;
    }
}

.remove-file-btn .stButton>button:hover {
    background: rgba(239, 68, 68, 0.15) !important;
    transform: none !important;
}

/* Input bar - responsive */
[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 400 !important;
    background: linear-gradient(to top, rgba(6, 11, 43, 0.98) 0%, rgba(6, 11, 43, 0.85) 60%, transparent 100%) !important;
    padding: 1rem 0 0.8rem !important;
}

@media (max-width: 768px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
        padding: 0.8rem 0 0.6rem !important;
    }
}

@media (max-width: 480px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
        padding: 0.6rem 0 0.5rem !important;
    }
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"] {
    display: flex !important;
    align-items: center !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) .element-container,
[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stVerticalBlock"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-baseweb="textarea"],
[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-baseweb="base-input"],
[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) div[style] {
    background: #1c2f6e !important;
    border: 1.5px solid rgba(6, 182, 212, 0.4) !important;
    border-radius: 14px !important;
    box-shadow: none !important;
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea,
[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea:focus {
    background: #1c2f6e !important;
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
    caret-color: #06B6D4 !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 14px !important;
    font-family: var(--font) !important;
    font-size: 0.94rem !important;
    padding: 0.75rem 1.1rem !important;
    resize: none !important;
    line-height: 1.55 !important;
}

@media (max-width: 768px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea,
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea:focus {
        font-size: 0.88rem !important;
        padding: 0.65rem 1rem !important;
    }
}

@media (max-width: 480px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea,
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea:focus {
        font-size: 0.85rem !important;
        padding: 0.6rem 0.9rem !important;
    }
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea::placeholder {
    color: rgba(168, 180, 216, 0.5) !important;
    -webkit-text-fill-color: rgba(168, 180, 216, 0.5) !important;
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) label {
    display: none !important;
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button {
    background: linear-gradient(135deg, #1B2B6B, #06B6D4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: var(--font) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    height: 52px !important;
    white-space: nowrap !important;
    width: 100% !important;
    box-shadow: 0 0 18px rgba(6, 182, 212, 0.3) !important;
}

@media (max-width: 768px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button {
        font-size: 0.85rem !important;
        height: 48px !important;
    }
}

@media (max-width: 480px) {
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button {
        font-size: 0.8rem !important;
        height: 44px !important;
    }
}

[data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button:hover {
    background: linear-gradient(135deg, #243580, #22D3EE) !important;
    transform: none !important;
}

/* Thinking */
.ab-thinking {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 0.38rem 0.95rem;
    font-size: 0.81rem;
    color: var(--t2);
}

@media (max-width: 480px) {
    .ab-thinking {
        font-size: 0.75rem;
        padding: 0.3rem 0.7rem;
    }
}

.dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--teal);
    display: inline-block;
    animation: pu 1.2s infinite;
}

.dot:nth-child(2) {
    animation-delay: .2s;
}

.dot:nth-child(3) {
    animation-delay: .4s;
}

@keyframes pu {
    0%, 80%, 100% {
        opacity: .3;
        transform: scale(.8);
    }
    40% {
        opacity: 1;
        transform: scale(1);
    }
}

/* History */
.ab-hist-item {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    margin-bottom: 0.4rem;
}

@media (max-width: 480px) {
    .ab-hist-item {
        padding: 0.5rem 0.65rem;
    }
}

.ab-hist-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #EEF2FF;
    margin-bottom: 0.15rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

@media (max-width: 480px) {
    .ab-hist-title {
        font-size: 0.75rem;
    }
}

.ab-hist-meta {
    font-size: 0.69rem;
    color: var(--t3);
}

@media (max-width: 480px) {
    .ab-hist-meta {
        font-size: 0.62rem;
    }
}

.ab-hist-badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--teal);
    background: var(--tg);
    border: 1px solid var(--tb);
    border-radius: 20px;
    padding: 0.1rem 0.45rem;
    margin-left: 0.35rem;
}

@media (max-width: 480px) {
    .ab-hist-badge {
        font-size: 0.58rem;
        padding: 0.05rem 0.35rem;
    }
}

.ab-hist-empty {
    text-align: center;
    padding: 1.2rem 0;
    color: var(--t3);
    font-size: 0.83rem;
}

/* Panel buttons */
.panel-save .stButton>button {
    background: var(--teal) !important;
    color: #060B2B !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1rem !important;
    box-shadow: none !important;
    width: 100% !important;
}

@media (max-width: 480px) {
    .panel-save .stButton>button {
        font-size: 0.78rem !important;
        padding: 0.45rem 0.8rem !important;
    }
}

.panel-save .stButton>button:hover {
    background: #22D3EE !important;
    transform: none !important;
}

.panel-del .stButton>button {
    background: rgba(255, 255, 255, 0.06) !important;
    color: var(--t2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-size: 0.84rem !important;
    padding: 0.5rem 1rem !important;
    box-shadow: none !important;
    width: 100% !important;
}

@media (max-width: 480px) {
    .panel-del .stButton>button {
        font-size: 0.78rem !important;
        padding: 0.45rem 0.8rem !important;
    }
}

.panel-del .stButton>button:hover {
    background: rgba(239, 68, 68, 0.12) !important;
    color: #FCA5A5 !important;
    border-color: rgba(239, 68, 68, 0.35) !important;
    transform: none !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 4px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--teal);
}

/* Popover nav */
[data-testid="stPopover"] [data-testid="stPopoverBody"] {
    background: #07102E !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    box-shadow: 0 24px 56px rgba(0, 0, 0, 0.7) !important;
    padding: 1rem 1.2rem !important;
    min-width: 280px !important;
    max-width: 90vw !important;
}

@media (max-width: 768px) {
    [data-testid="stPopover"] [data-testid="stPopoverBody"] {
        padding: 0.8rem 1rem !important;
        min-width: 260px !important;
    }
}

@media (max-width: 480px) {
    [data-testid="stPopover"] [data-testid="stPopoverBody"] {
        padding: 0.7rem 0.8rem !important;
        min-width: 240px !important;
    }
}

[data-testid="stPopover"] button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 20px !important;
    font-family: var(--font) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--teal) !important;
    padding: 0.25rem 0.85rem !important;
    box-shadow: none !important;
    min-height: 0 !important;
    height: 28px !important;
    white-space: nowrap !important;
}

[data-testid="stPopover"] button[kind="secondary"]:hover {
    background: rgba(6, 182, 212, 0.15) !important;
    border-color: var(--teal) !important;
    transform: none !important;
}

[data-testid="stPopover"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
    background: #dbeafe !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
    border-radius: 10px !important;
    color: #1e3a5f !important;
}

[data-testid="stPopover"] [data-testid="stSelectbox"] [data-baseweb="select"] svg {
    color: #1e3a5f !important;
    fill: #1e3a5f !important;
}

[data-testid="stPopover"] [data-testid="stSelectbox"] label {
    color: var(--t2) !important;
    font-size: 0.8rem !important;
}

[data-testid="stPopover"] [data-testid="stTextInput"] input {
    background: #0f1d5e !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    color: var(--t1) !important;
    -webkit-text-fill-color: var(--t1) !important;
    caret-color: var(--teal) !important;
    font-family: var(--font) !important;
    font-size: 0.87rem !important;
}

[data-testid="stPopover"] [data-testid="stTextInput"] input::placeholder {
    color: var(--t3) !important;
    -webkit-text-fill-color: var(--t3) !important;
}

[data-testid="stPopover"] [data-testid="stTextInput"] label {
    color: var(--t2) !important;
    font-size: 0.8rem !important;
}

[data-testid="stPopover"] [data-testid="stToggle"] label {
    color: var(--t2) !important;
    font-size: 0.85rem !important;
}

[data-testid="stPopover"] .panel-save button {
    background: var(--teal) !important;
    color: #060B2B !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    width: 100% !important;
}

[data-testid="stPopover"] .panel-del button {
    background: rgba(255, 255, 255, 0.06) !important;
    color: var(--t2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    width: 100% !important;
}

[data-testid="stPopover"] .panel-del button:hover {
    background: rgba(239, 68, 68, 0.12) !important;
    color: #FCA5A5 !important;
    border-color: rgba(239, 68, 68, 0.35) !important;
}

[data-testid="stPopover"] p,
[data-testid="stPopover"] label,
[data-testid="stPopover"] span {
    color: var(--t2) !important;
}

[data-testid="stPopover"] strong,
[data-testid="stPopover"] h1,
[data-testid="stPopover"] h2,
[data-testid="stPopover"] h3 {
    color: #EEF2FF !important;
}

/* Additional responsive fixes */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }
    
    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        min-width: auto !important;
        flex: 1 1 auto !important;
    }
}

@media (max-width: 480px) {
    .stButton button {
        font-size: 0.75rem !important;
        padding: 0.4rem 0.6rem !important;
    }
    
    [data-testid="stTextInput"] input {
        font-size: 0.85rem !important;
        padding: 0.5rem 0.75rem !important;
    }
}

/* ── MOBILE REFINEMENTS ───────────────────────────────────────── */
@media (max-width: 768px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 0.6rem 0.8rem !important;
        padding: 0.5rem 0.8rem !important;
    }

    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
    }

    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:nth-last-child(2) span,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-last-child(2) span {
        background: var(--tg) !important;
        border: 1px solid var(--tb) !important;
        border-radius: 20px !important;
        padding: 0.2rem 0.7rem !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: var(--teal) !important;
        white-space: nowrap !important;
    }

    .ab-avatar-circle {
        width: 30px !important;
        height: 30px !important;
        font-size: 0.75rem !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
        padding: 0.6rem 0.5rem 0.5rem !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]:first-child {
        flex: 0 0 48px !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]:nth-child(2) {
        flex: 1 !important;
        margin: 0 0.25rem !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]:last-child {
        flex: 0 0 70px !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea {
        font-size: 0.85rem !important;
        padding: 0.55rem 0.8rem !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button {
        font-size: 0.75rem !important;
        height: 42px !important;
        padding: 0 0.25rem !important;
        white-space: nowrap !important;
    }

    [data-testid="stPopover"] [data-testid="stPopoverBody"] {
        max-width: 85vw !important;
        padding: 0.8rem !important;
    }
}

@media (max-width: 480px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
        gap: 0.4rem 0.6rem !important;
        padding: 0.4rem 0.5rem !important;
    }

    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:nth-last-child(2) span,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-last-child(2) span {
        font-size: 0.7rem !important;
        padding: 0.15rem 0.5rem !important;
    }

    .ab-avatar-circle {
        width: 26px !important;
        height: 26px !important;
        font-size: 0.65rem !important;
    }

    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) {
        padding: 0.5rem 0.3rem 0.4rem !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]:first-child {
        flex: 0 0 42px !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]:last-child {
        flex: 0 0 60px !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea {
        font-size: 0.8rem !important;
        padding: 0.45rem 0.7rem !important;
    }
    [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button {
        font-size: 0.7rem !important;
        height: 38px !important;
        white-space: nowrap !important;
    }

    [data-testid="stPopover"] [data-testid="stPopoverBody"] {
        max-width: 90vw !important;
        padding: 0.6rem !important;
    }
}

section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:nth-last-child(2),
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-last-child(2) {
    display: flex !important;
}

@media (max-width: 768px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: auto !important;
    }
    
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
        gap: 0.5rem !important;
        padding: 0.55rem 0.75rem !important;
    }
}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

_components.html("""<script>
(function(){
    function fix(){
        document.querySelectorAll('[role="option"]').forEach(function(el){
            var sel=el.getAttribute('aria-selected')==='true';
            el.style.setProperty('background-color',sel?'#bae6fd':'#f8fafc','important');
            el.style.setProperty('color',sel?'#0c4a6e':'#0f172a','important');
            el.style.setProperty('border-left',sel?'3px solid #06B6D4':'none','important');
            el.onmouseenter=function(){if(el.getAttribute('aria-selected')!=='true')el.style.setProperty('background-color','#e2e8f0','important');};
            el.onmouseleave=function(){if(el.getAttribute('aria-selected')!=='true')el.style.setProperty('background-color','#f8fafc','important');};
        });
    }
    new MutationObserver(fix).observe(document.body,{childList:true,subtree:true});
    fix();
})();
</script>""", height=0)

AUTH_BTN_STYLE = """<style>
[data-testid="stBaseButton-secondary"]:not(.ab-pill-btn *):not(.ab-cu-btn *):not(.remove-file-btn *){
    background:linear-gradient(135deg,#1B2B6B,#06B6D4)!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
    border:none!important;border-radius:12px!important;font-weight:700!important;height:44px!important;font-size:0.92rem!important;
    width:auto!important;min-width:160px!important;max-width:260px!important;padding:0 2rem!important;
    box-shadow:0 4px 20px rgba(6,182,212,0.35)!important;display:block!important;margin:0 auto!important;
}
/* Force white text on page links - using !important on everything */
[data-testid="stPageLink-Link"],
[data-testid="stPageLink-Link"]:link,
[data-testid="stPageLink-Link"]:visited,
[data-testid="stPageLink-Link"] span,
[data-testid="stPageLink-Link"] p,
.stPageLink-Link,
.stPageLink-Link span,
div[data-testid="stPageLink"] a,
div[data-testid="stPageLink"] a:link,
div[data-testid="stPageLink"] a:visited,
div[data-testid="stPageLink"] a span {
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
    background-color: transparent !important;
    background: transparent !important;
}

[data-testid="stPageLink-Link"]:hover,
[data-testid="stPageLink-Link"]:hover *,
div[data-testid="stPageLink"] a:hover,
div[data-testid="stPageLink"] a:hover span {
    color: #06B6D4 !important;
    -webkit-text-fill-color: #06B6D4 !important;
}

/* Target the specific paragraph inside the link */
[data-testid="stPageLink"] p {
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
}

[data-testid="stPageLink"]:hover p {
    color: #06B6D4 !important;
    -webkit-text-fill-color: #06B6D4 !important;
}
</style>"""

# ============================================
# INITIALIZE SESSION STATE
# ============================================
for k, v in {
    "logged_in": False,
    "username": None,
    "user_email": None,
    "messages": [],
    "student_name": "Student",
    "active_course": None,
    "active_topic": None,
    "persona": "default",
    "use_scaffolding": False,
    "view": "home",
    "thinking": False,
    "current_session_id": None,
    "tracker": None,
    "auth_mode": "login",
    "auth_error": "",
    "auth_success": "",
    "cin_key": 0,
    "practice_seed": None,
    "uploaded_files": [],
    "pending_image": False,
    "assignment_mode": False,
    # AUDIO EDIT 2: added audio_enabled to session state
    "audio_enabled": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================
# AUTH CHECK
# ============================================
if not st.session_state.logged_in:
    mode = st.session_state.auth_mode
    _, auth_col, _ = st.columns([1, 2, 1])
    with auth_col:
        st.markdown('<div class="auth-logo"><div class="auth-logo-icon">🤖</div><span style="font-size:1.5rem;font-weight:800;color:#EEF2FF;">AlgoBuddy</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="auth-tabs"><div class="auth-tab {"active" if mode=="login" else ""}">Sign In</div><div class="auth-tab {"active" if mode=="signup" else ""}">Create Account</div></div>', unsafe_allow_html=True)
        
        if st.session_state.auth_error: 
            st.error(st.session_state.auth_error)
        if st.session_state.auth_success: 
            st.success(st.session_state.auth_success)
        
        if mode == "login":
            st.markdown('<div class="auth-sub">Welcome back — sign in with your email 🔥</div>', unsafe_allow_html=True)
            lu = st.text_input("Email", key="li_user", placeholder="you@example.com")
            lp = st.text_input("Password", key="li_pass", placeholder="••••••••", type="password")
            st.markdown(AUTH_BTN_STYLE, unsafe_allow_html=True)
            
            if st.button("Sign In →", key="li_btn", use_container_width=False):
                if lu.strip() and lp:
                    ok, msg, ud = _auth.login(lu, lp)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.user_email = lu.strip().lower()
                        username_from_meta = ud.get("username", "")
                        if not username_from_meta or "@" in username_from_meta:
                            username_from_meta = lu.strip().split('@')[0]
                        st.session_state.username = username_from_meta
                        display_name = ud.get("display_name", "")
                        if not display_name or "@" in str(display_name):
                            display_name = username_from_meta
                        st.session_state.student_name = display_name
                        st.session_state.user_id = ud.get("id")
                        
                        # Load user's previously uploaded files from Supabase
                        from file_processor import get_user_files
                        user_id = ud.get("id")
                        if user_id:
                            files = get_user_files(user_id)
                            for f in files:
                                fname = f.get("file_name") or f.get("name") or f.get("filename") or "file"
                                ftype = f.get("file_type") or f.get("type") or "text"
                                image_data = None
                                if ftype == "image" and f.get("image_data"):
                                    image_data = {
                                        "base64": f["image_data"],
                                        "media_type": f.get("media_type", "image/png"),
                                        "filename": fname
                                    }
                                st.session_state.uploaded_files.append({
                                    "name": fname,
                                    "type": ftype,
                                    "content": f.get("content", ""),
                                    "image_data": image_data,
                                    "file_id": f.get("id")
                                })
                        
                        st.session_state.auth_error = ""
                        st.rerun()
                    else:
                        st.session_state.auth_error = msg
                        st.rerun()
                else:
                    st.session_state.auth_error = "Please fill in both fields."
                    st.rerun()
            
            st.page_link("pages/signup.py", label="No account? Create one →")
        
        else:
            st.markdown('<div class="auth-sub">Join AlgoBuddy — your AI-powered CS tutor 🎓</div>', unsafe_allow_html=True)
            su_email = st.text_input("Email", key="su_email", placeholder="you@example.com")
            su_name = st.text_input("Your name", key="su_name", placeholder="e.g. Obianuju")
            su_user = st.text_input("Choose a username", key="su_user", placeholder="e.g. uju123")
            su_pass = st.text_input("Password", key="su_pass", placeholder="At least 6 characters", type="password")
            su_pass2 = st.text_input("Confirm password", key="su_pass2", placeholder="Repeat your password", type="password")
            st.markdown(AUTH_BTN_STYLE, unsafe_allow_html=True)
            
            if st.button("Create Account →", key="su_btn", use_container_width=False):
                if not all([su_email.strip(), su_name.strip(), su_user.strip(), su_pass, su_pass2]):
                    st.session_state.auth_error = "Please fill in all fields."
                    st.rerun()
                elif su_pass != su_pass2:
                    st.session_state.auth_error = "Passwords do not match."
                    st.rerun()
                elif "@" not in su_email or "." not in su_email:
                    st.session_state.auth_error = "Please enter a valid email address."
                    st.rerun()
                elif len(su_pass) < 6:
                    st.session_state.auth_error = "Password must be at least 6 characters."
                    st.rerun()
                else:
                    ok, msg = _auth.signup(su_email, su_user, su_name, su_pass)
                    if ok:
                        st.session_state.auth_mode = "login"
                        st.session_state.auth_success = f"Account created! Please check your email to confirm, then sign in."
                        st.session_state.auth_error = ""
                        st.rerun()
                    else:
                        st.session_state.auth_error = msg
                        st.rerun()
            
            st.page_link("app.py", label="Already have an account? Sign in →")
    
    st.stop()

# ============================================
# INITIALIZE TRACKER
# ============================================
from progress_tracker import ProgressTracker as _PT
from file_processor import process_upload

_sn = st.session_state.student_name
_sf = f"{st.session_state.username}_progress.json"

if st.session_state.tracker is None:
    st.session_state.tracker = _PT(_sn)
    st.session_state.tracker.load_from_file(_sf)
    _old = st.session_state.tracker.stats.get("current_streak", 0)
    st.session_state.tracker._update_streak()
    if st.session_state.tracker.stats.get("current_streak", 0) != _old:
        st.session_state.tracker.save_to_file(_sf)

def cn():
    if not st.session_state.active_course: return None
    return get_course_display(st.session_state.active_course)

def tn():
    if not st.session_state.active_course or not st.session_state.active_topic: return None
    return get_topic_display(st.session_state.active_course, st.session_state.active_topic)

def go(v):
    if st.session_state.view != v:
        st.session_state.view = v
        st.rerun()

def _save():
    if st.session_state.messages and st.session_state.username:
        if not st.session_state.current_session_id:
            st.session_state.current_session_id = new_session_id()
        save_session(
            username=st.session_state.username,
            session_id=st.session_state.current_session_id,
            messages=st.session_state.messages,
            course_id=st.session_state.active_course,
            topic_id=st.session_state.active_topic,
            persona=st.session_state.persona,
        )

# ============================================
# REDIRECT CHECK
# ============================================
if st.session_state.pop("_go_to_practice", False):
    st.switch_page("pages/practice.py")

initials = (st.session_state.student_name[0] if st.session_state.student_name else "S").upper()
_in_chat = st.session_state.view == "chat"
LOGO = '<div style="display:flex;align-items:center;gap:0.5rem;"><div style="width:26px;height:26px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;">🤖</div><span style="font-size:0.97rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AlgoBuddy</span></div>'
AV = f'<div style="display:flex;align-items:center;justify-content:center;"><div class="ab-avatar-circle">{initials}</div></div>'

# ============================================
# ON_CHANGE CALLBACKS
# ============================================
def _on_nav_course_change():
    st.session_state.active_course = st.session_state.pop_course
    st.session_state.active_topic = None

def _on_nav_topic_change():
    st.session_state.active_topic = st.session_state.pop_topic

def _on_nav_persona_change():
    st.session_state.persona = st.session_state.pop_persona

def _on_pm_course_change():
    st.session_state.active_course = st.session_state.pm_course
    st.session_state.active_topic = None

def _on_pm_topic_change():
    st.session_state.active_topic = st.session_state.pm_topic

def _on_pm_persona_change():
    st.session_state.persona = st.session_state.pm_persona

# ============================================
# POPOVER HELPERS
# ============================================
def _courses_popover():
    st.markdown(
        '<div style="font-size:0.67rem;font-weight:700;letter-spacing:0.13em;text-transform:uppercase;color:var(--t3);margin-bottom:0.8rem;">Course & Topic</div>',
        unsafe_allow_html=True,
    )
    ck = [None] + get_course_list()
    cl = get_course_labels()
    ci = ck.index(st.session_state.active_course) if st.session_state.active_course in ck else 0

    st.selectbox(
        "Course", ck, index=ci, format_func=lambda k: cl[k],
        key="pop_course", on_change=_on_nav_course_change,
    )

    if st.session_state.active_course:
        tids = get_topics_for_course(st.session_state.active_course)
        tk = [None] + tids

        def _tlbl(t):
            if t is None: return "— All topics —"
            return get_topic_display(st.session_state.active_course, t) or t

        ct = st.session_state.active_topic if st.session_state.active_topic in tids else None
        st.selectbox(
            "Topic", tk, index=tk.index(ct), format_func=_tlbl,
            key="pop_topic", on_change=_on_nav_topic_change,
        )

def _settings_popover():
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.9rem;"><div class="ab-avatar-circle" style="width:36px;height:36px;font-size:0.9rem;">{initials}</div><div style="font-size:0.85rem;font-weight:600;color:#fff;">{st.session_state.student_name}<div style="font-size:0.7rem;color:var(--t3);">@{st.session_state.username}</div></div></div>',
        unsafe_allow_html=True,
    )
    with st.expander("✏️ Edit profile", expanded=False):
        en = st.text_input("Display name", value=st.session_state.student_name, key="edn")
        eu = st.text_input("Username", value=st.session_state.username or "", key="eun")
        st.markdown('<div style="font-size:0.75rem;color:var(--t3);margin:0.3rem 0;">Change password (leave blank to keep)</div>', unsafe_allow_html=True)
        ep1 = st.text_input("New password", key="ep1", type="password", placeholder="New password")
        ep2 = st.text_input("Confirm", key="ep2", type="password", placeholder="Repeat")
        st.markdown('<div class="panel-save">', unsafe_allow_html=True)
        if st.button("Save", key="esv", use_container_width=True):
            errs = []
            if en.strip() and en.strip() != st.session_state.student_name:
                ok, msg = _auth.update_display_name(st.session_state.username, en.strip())
                if ok: st.session_state.student_name = en.strip()
                else: errs.append(msg)
            if eu.strip() and eu.strip() != st.session_state.username:
                ok, msg = _auth.update_username(st.session_state.username, eu.strip())
                if ok: st.session_state.username = eu.strip().lower()
                else: errs.append(msg)
            if ep1 or ep2:
                if ep1 != ep2: errs.append("Passwords don't match.")
                elif len(ep1) < 6: errs.append("At least 6 characters.")
                else:
                    ok, msg = _auth.update_password(st.session_state.username, ep1)
                    if not ok: errs.append(msg)
            if errs: st.error(" ".join(errs))
            else: st.success("Saved!"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    pkeys = list(get_personas().keys())
    personas_data = get_personas()
    st.selectbox(
        "Teaching persona", pkeys,
        format_func=lambda k: personas_data[k]["display_name"],
        index=pkeys.index(st.session_state.persona) if st.session_state.persona in pkeys else 0,
        key="pop_persona", on_change=_on_nav_persona_change,
    )

    st.session_state.use_scaffolding = st.toggle(
        "Step-by-step mode", value=st.session_state.use_scaffolding, key="pop_scaffold"
    )
    st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)

    with st.expander("🕐 Chat History", expanded=False):
        sessions = load_all_sessions(st.session_state.username)
        if not sessions:
            st.markdown('<div style="font-size:0.83rem;color:var(--t3);text-align:center;padding:0.8rem 0;">No saved chats yet.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="panel-save" style="margin-bottom:0.5rem;">', unsafe_allow_html=True)
            if st.button("New Chat", key="hn", use_container_width=True):
                _save()
                st.session_state.messages = []
                st.session_state.current_session_id = new_session_id()
                clear_conversation()
                go("chat")
            st.markdown('</div>', unsafe_allow_html=True)
            for s in sessions:
                dl = format_session_date(s["updated_at"])
                cn_ = None
                if s["course_id"]:
                    cc = get_course_display(s["course_id"])
                    if cc:
                        cn_ = cc
                        if s["topic_id"]:
                            tt = get_topic_display(s["course_id"], s["topic_id"])
                            if tt: cn_ += f" › {tt}"
                badge = f'<span class="ab-hist-badge">{cn_}</span>' if cn_ else ""
                st.markdown(
                    f'<div class="ab-hist-item"><div class="ab-hist-title">{s["title"]}</div><div class="ab-hist-meta">{dl} · {s["message_count"]} msgs{badge}</div></div>',
                    unsafe_allow_html=True,
                )
                cr, cd_ = st.columns([3, 1])
                with cr:
                    if st.button("Resume →", key=f"r_{s['session_id']}", use_container_width=True):
                        _save()
                        full = load_session(st.session_state.username, s["session_id"])
                        if full:
                            st.session_state.messages = full["messages"]
                            st.session_state.current_session_id = s["session_id"]
                            st.session_state.active_course = full.get("course_id")
                            st.session_state.active_topic = full.get("topic_id")
                            st.session_state.persona = full.get("persona", "default")
                            set_conversation_history(full["messages"])
                            go("chat")
                with cd_:
                    if st.button("🗑", key=f"d_{s['session_id']}", use_container_width=True):
                        delete_session(st.session_state.username, s["session_id"])
                        st.rerun()
                st.markdown('<div style="height:0.1rem"></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    sa, sb = st.columns(2)
    with sa:
        st.markdown('<div class="panel-del">', unsafe_allow_html=True)
        if st.button("Clear chat", key="sc", use_container_width=True):
            _save()
            st.session_state.messages = []
            st.session_state.current_session_id = new_session_id()
            clear_conversation()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with sb:
        st.markdown('<div class="panel-del">', unsafe_allow_html=True)
        if st.button("Sign out", key="slo", use_container_width=True):
            _save()
            clear_all_caches()
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 Clear Cache", key="clear_cache", use_container_width=True):
        clear_all_caches()
        st.success("Cache cleared! Refresh to reload data.")
        st.rerun()

# ============================================
# NAVIGATION BAR
# ============================================
if _in_chat:
    c1, _, c2, c3, c4, c5, c6 = st.columns([2, 4.7, 0.5, 0.5, 0.5, 1.3, 0.5])
    with c1: st.markdown(LOGO, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
        if st.button("🏠", key="nh", use_container_width=True, help="Home"):
            _save()
            go("home")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        with st.popover("📚", help="Courses & Topics"):
            _courses_popover()
    with c4:
        with st.popover("⚙️", help="Settings"):
            _settings_popover()
    with c5:
        pn = get_personas().get(st.session_state.persona, get_personas()["default"])["display_name"]
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:flex-end;padding-right:0.3rem;"><span style="font-size:0.74rem;color:var(--teal);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{pn}</span></div>',
            unsafe_allow_html=True,
        )
    with c6: st.markdown(AV, unsafe_allow_html=True)
else:
    c1, _, c2, c3, c4 = st.columns([2, 6.5, 0.5, 0.5, 0.5])
    with c1: st.markdown(LOGO, unsafe_allow_html=True)
    with c2:
        with st.popover("📚", help="Courses & Topics"):
            _courses_popover()
    with c3:
        with st.popover("⚙️", help="Settings"):
            _settings_popover()
    with c4: st.markdown(AV, unsafe_allow_html=True)

st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.07);"></div>', unsafe_allow_html=True)

# ============================================
# HOME VIEW
# ============================================
if st.session_state.view == "home":
    sname = st.session_state.student_name
    cl_ = cn()
    tl_ = tn()
    if tl_: sub = f"Focused on <strong>{tl_}</strong> in {cl_}."
    elif cl_: sub = f"You're studying <strong>{cl_}</strong>."
    else: sub = "Your personal CS tutor. Pick a course or just start chatting."
    st.markdown(
        f'<div class="ab-home"><div class="ab-hero"><div class="ab-hero-icon">🤖</div><div class="ab-hero-h">Hey <span class="hl">{sname}</span>, I\'m AlgoBuddy</div><div class="ab-hero-sub">{sub}</div></div></div>',
        unsafe_allow_html=True,
    )
    CARDS = [
        ("💬", "Chat with AlgoBuddy", "Ask questions, get explanations and talk through concepts naturally", "Click to start", "go_chat", "Open Chat"),
        ("🧮", "Practice Mode", "AI-generated problems with progressive hints and instant feedback", "Click to open", "go_prac", "Open Practice"),
        ("📈", "My Progress", "Track accuracy, streaks, weak topics and XP earned", "Click to open", "go_prog", "My Progress"),
        ("🃏", "Flashcards", "Spaced repetition cards — AI-generated for every topic", "Click to open", "go_flash", "Flashcards"),
    ]
    _, mid, _ = st.columns([1, 8, 1])
    with mid:
        r1 = st.columns(2, gap="large")
        r2 = st.columns(2, gap="large")
        for col, (ico, title, desc, hint, key, bl) in zip(r1 + r2, CARDS):
            with col:
                st.markdown(
                    f'<div class="ab-card-body"><div class="ab-card-ico">{ico}</div><div class="ab-card-t">{title}</div><div class="ab-card-d">{desc}</div><div class="ab-card-hint">{hint}</div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="ab-cu-btn">', unsafe_allow_html=True)
                if st.button(bl, key=key, use_container_width=True):
                    if key == "go_chat":
                        if not st.session_state.current_session_id:
                            st.session_state.current_session_id = new_session_id()
                        go("chat")
                    elif key == "go_prac": st.switch_page("pages/practice.py")
                    elif key == "go_prog": st.switch_page("pages/progress.py")
                    elif key == "go_flash": st.switch_page("pages/flashcards.py")
                st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# CHAT VIEW
# ============================================
elif st.session_state.view == "chat":
    sname = st.session_state.student_name
    ini = (sname[0] if sname else "S").upper()
    bot = AVATAR.get(st.session_state.persona, "🤖")
    if not st.session_state.current_session_id:
        st.session_state.current_session_id = new_session_id()

    tags = [t for t in [cn(), tn()] if t]
    tag_html = "".join(f'<span class="ab-ctx-tag">{t}</span>' for t in tags)
    for f in st.session_state.uploaded_files:
        icon = "🖼️" if f["type"] == "image" else "📄"
        tag_html += f'<span class="ab-ctx-tag">{icon} {f["name"]}</span>'
    if st.session_state.assignment_mode:
        tag_html += '<span class="ab-ctx-tag" style="background:rgba(139,92,246,0.15);border-color:rgba(139,92,246,0.4);color:#a78bfa;">📝 Assignment Mode</span>'
    if tag_html:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.4rem;padding:0.5rem 2rem 0;flex-wrap:wrap;">{tag_html}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="ab-chat-wrap">', unsafe_allow_html=True)
    if not st.session_state.messages:
        display_name = st.session_state.username or sname
        greet = {
            "batman": f"Ready {display_name}. What are we solving?",
            "hermione": f"Hello {display_name}! What shall we study?",
            "tony_stark": f"Hey {display_name} lets get brilliant.",
            "yoda": f"Welcome {display_name}. Ready to learn, are you?",
            "chill_senior": f"Hey {display_name}! What are we tackling today?",
            "osuofia": f"Nnem Kedu {display_name}. Gịnị ka anyị na-amụ today?",
            "death": f"Gatoo {display_name}. its been a whileee",
            "kanayo": f"{display_name} are ready to make sacrifices?",
            "default": f"Hey {display_name}! What would you like to learn?",
        }.get(st.session_state.persona, f"Hey {display_name}!")
        focus = (
            f"Focused on <strong>{tn()}</strong> in {cn()}." if tn()
            else f"Studying <strong>{cn()}</strong>." if cn()
            else "Pick a course, upload notes via +, or just ask me anything CS-related."
        )
        st.markdown(
            f'<div style="text-align:center;padding:4rem 1rem 1rem;"><div style="font-size:1.1rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">{greet}</div><div style="font-size:0.9rem;color:#A8B4D8;">{focus}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]
        show_cta = len(bot_msgs) >= 5
        last_bot_idx = None
        if show_cta:
            for _i, _m in enumerate(st.session_state.messages):
                if _m["role"] == "assistant": last_bot_idx = _i

        for idx, msg in enumerate(st.session_state.messages):
            ts = msg.get("time", "")
            c = msg["content"]
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="ab-row-u"><div class="ab-bu">{c}</div><div class="ab-uav">{ini}</div></div><div style="text-align:right;margin-bottom:0.4rem;margin-top:-0.6rem;padding-right:2.2rem;"><span class="ab-ts">{ts}</span></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="ab-row-b"><div class="ab-av">{bot}</div><div><div class="ab-bb">{c}</div><div class="ab-ts">{ts}</div></div></div>',
                    unsafe_allow_html=True,
                )
                # AUDIO EDIT 4: play audio for the last bot message if it has audio attached
                if idx == last_bot_idx and msg.get("audio"):
                    st.audio(msg["audio"], format="audio/mp3")
                if idx == last_bot_idx:
                    st.markdown('<div class="practice-cta" style="margin-left:2.4rem;margin-top:0.1rem;margin-bottom:0.7rem;display:inline-block;">', unsafe_allow_html=True)
                    if st.button("💪 Practice what you just learned →", key="prac_cta"):
                        st.session_state.practice_seed = c
                        st.session_state["_go_to_practice"] = True
                        _save()
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("thinking"):
        st.markdown(
            '<div style="display:flex;padding:0.3rem 0 0.5rem;"><div class="ab-thinking"><span class="dot"></span><span class="dot"></span><span class="dot"></span>&nbsp;AlgoBuddy is thinking...</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div id="chat-bottom" style="height:10px;"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    _components.html("""<script>
    (function(){var el=window.parent.document.getElementById('chat-bottom');if(el)el.scrollIntoView({behavior:'smooth',block:'end'});})();
    </script>""", height=0)

    # INPUT BAR
    col_plus, col_input, col_send = st.columns([0.06, 0.84, 0.10], gap="small")

    with col_plus:
        with st.popover("＋", help="Files, course, persona, assignment mode"):
            st.markdown("**📝 Assignment Mode**")
            st.session_state.assignment_mode = st.toggle(
                "Assignment Mode", value=st.session_state.assignment_mode,
                key="toggle_assign", help="AlgoBuddy guides step-by-step without giving answers",
            )
            # AUDIO EDIT 3: voice responses toggle in the + popover
            st.markdown("<div style='height:0.3rem'></div>", unsafe_allow_html=True)
            st.session_state.audio_enabled = st.toggle(
                "🔊 Voice responses", value=st.session_state.audio_enabled,
                key="toggle_audio", help="AlgoBuddy speaks each response in the persona's voice",
            )
            st.divider()
            st.markdown("**📎 Files**")
            for fi, f in enumerate(st.session_state.uploaded_files):
                icon = "🖼️" if f["type"] == "image" else "📄"
                frow1, frow2 = st.columns([4, 1])
                with frow1:
                    st.markdown(f'<div class="file-badge">{icon} {f["name"]}</div>', unsafe_allow_html=True)
                with frow2:
                    st.markdown('<div class="remove-file-btn">', unsafe_allow_html=True)
                    if st.button("✕", key=f"rmf_{fi}", use_container_width=True):
                        # Delete from Supabase if it has a file_id
                        if f.get("file_id"):
                            from file_processor import delete_file_from_db
                            user_id = st.session_state.get("user_id")
                            if user_id:
                                delete_file_from_db(user_id, f["file_id"])

                        st.session_state.uploaded_files.pop(fi)
                        if not any(x["type"] == "image" for x in st.session_state.uploaded_files):
                            st.session_state.pending_image = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            up = st.file_uploader(
                "Upload", type=["pdf", "docx", "jpg", "jpeg", "png", "webp"],
                label_visibility="collapsed", key=f"up_{len(st.session_state.uploaded_files)}",
            )
            if up and up.name not in [x["name"] for x in st.session_state.uploaded_files]:
                with st.spinner(f"Reading {up.name}..."):
                    user_id = st.session_state.get("user_id")
                    res = process_upload(up, user_id=user_id)
                if res.get("error"):
                    st.error(res["error"])
                else:
                    st.session_state.uploaded_files.append({
                        "name": res["filename"],
                        "type": res["type"],
                        "content": res.get("content", ""),
                        "image_data": res.get("image_data"),
                        "file_id": res.get("file_id")
                    })
                    if res["type"] == "image":
                        st.session_state.pending_image = True
                    st.rerun()
            st.divider()

            st.markdown("**📚 Course & Topic**")
            ck2 = [None] + get_course_list()
            cl2 = get_course_labels()
            ci2 = ck2.index(st.session_state.active_course) if st.session_state.active_course in ck2 else 0
            st.selectbox(
                "Course", ck2, index=ci2, format_func=lambda k: cl2[k],
                key="pm_course", on_change=_on_pm_course_change,
            )
            if st.session_state.active_course:
                tids2 = get_topics_for_course(st.session_state.active_course)
                tk2 = [None] + tids2
                def _tl2(t):
                    return "All topics" if t is None else get_topic_display(st.session_state.active_course, t) or t
                ct2 = st.session_state.active_topic if st.session_state.active_topic in tids2 else None
                st.selectbox(
                    "Topic", tk2, index=tk2.index(ct2), format_func=_tl2,
                    key="pm_topic", on_change=_on_pm_topic_change,
                )
            st.divider()

            st.markdown("**🎭 Persona**")
            pkeys = list(get_personas().keys())
            personas_data = get_personas()
            st.selectbox(
                "Persona", pkeys,
                format_func=lambda k: personas_data[k]["display_name"],
                index=pkeys.index(st.session_state.persona) if st.session_state.persona in pkeys else 0,
                key="pm_persona", on_change=_on_pm_persona_change,
            )

    with col_input:
        pending_imgs = [f for f in st.session_state.uploaded_files if f["type"] == "image"]
        placeholder = (
            "Ask AlgoBuddy anything..." if not (st.session_state.pending_image and pending_imgs)
            else "Image attached — type your question..."
        )
        user_input = st.text_area(
            "msg", placeholder=placeholder, label_visibility="collapsed",
            key=f"_cin_{st.session_state.cin_key}", height=52,
        )
    with col_send:
        send = st.button("Send →", use_container_width=True, key="_send")

    if send and user_input.strip():
        try:
            clean = validate_user_message(user_input)
        except ValidationError as e:
            st.error(str(e))
            st.stop()
        st.session_state.messages.append({"role": "user", "content": clean, "time": time.strftime("%H:%M")})
        st.session_state.thinking = True
        st.session_state.cin_key += 1
        st.session_state.tracker._update_streak()
        st.session_state.tracker.save_to_file(_sf)
        # ✅ record_study_session (your original)
        st.session_state.tracker.record_study_session()
        st.session_state.tracker.save_to_file(_sf)
        st.rerun()

# ============================================
# AI RESPONSE
# ============================================
if st.session_state.get("thinking") and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last = st.session_state.messages[-1]["content"]
    text_files = [f for f in st.session_state.uploaded_files if f["type"] == "text" and f["content"]]
    combined = "\n\n".join(f"=== {f['name']} ===\n{f['content']}" for f in text_files) if text_files else None
    pending_imgs = [f for f in st.session_state.uploaded_files if f["type"] == "image"]
    _img = pending_imgs[-1]["image_data"] if st.session_state.pending_image and pending_imgs else None
    try:
        reply = get_tutor_response(
            message=last, use_scaffolding=st.session_state.use_scaffolding,
            student_name=st.session_state.student_name, course_id=st.session_state.active_course,
            topic_id=st.session_state.active_topic, persona=st.session_state.persona,
            assignment_mode=st.session_state.assignment_mode,
            file_context=combined, image_data=_img,
        )
    except Exception as e:
        err = str(e).lower()
        reply = (
            "Network issue." if any(x in err for x in ["connection", "timeout", "network", "refused"])
            else "API key issue." if any(x in err for x in ["api", "key", "auth", "invalid"])
            else f"Error: {e}"
        )
    # AUDIO EDIT 5: generate audio if voice responses is enabled
    audio_bytes = None
    if st.session_state.get("audio_enabled"):
        try:
            audio_bytes = generate_tts_audio(reply, st.session_state.persona)
        except Exception:
            audio_bytes = None
    # AUDIO EDIT 6: include audio in the appended message dict
    st.session_state.messages.append({"role": "assistant", "content": reply, "time": time.strftime("%H:%M"), "audio": audio_bytes})
    st.session_state.thinking = False
    if _img: st.session_state.pending_image = False
    bot_count = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    if bot_count == 5:
        st.session_state.tracker.record_chat_session()
        st.session_state.tracker.save_to_file(_sf)
    if text_files and not st.session_state.get("_notes_xp_awarded"):
        st.session_state.tracker.record_notes_upload()
        st.session_state.tracker.save_to_file(_sf)
        st.session_state["_notes_xp_awarded"] = True
    _save()
    st.rerun()