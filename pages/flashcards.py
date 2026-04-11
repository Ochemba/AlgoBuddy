import streamlit as st
import json, os, uuid
from datetime import date, timedelta
import emoji

# Add this import for datetime used in _schedule_card
from datetime import date, timedelta,datetime

st.set_page_config(page_title="Flashcards · AlgoBuddy", page_icon="🃏", layout="wide", initial_sidebar_state="collapsed")

from tutor_engine import generate_flashcards
from course_registry import COURSES, get_all_topic_ids_for_course, get_topic
from progress_tracker import ProgressTracker

from supabase_client import supabase
from datetime import date, timedelta

# Add caching for Supabase calls
@st.cache_data(ttl=60)
def get_cached_flashcards_from_db(user_id):
    """Cache flashcards from Supabase"""
    if not user_id:
        return []
    try:
        from supabase_client import supabase
        result = supabase().table("flashcards").select("*").eq("user_id", user_id).execute()
        return result.data
    except Exception as e:
        print(f"Error loading flashcards: {e}")
        return []

# Modify _load_all_cards function:
def _load_all_cards() -> list:
    """Load all flashcards for current user - WITH CACHING"""
    user_id = _get_user_id()
    if not user_id:
        return []
    
    # Check if we already loaded in this session
    if st.session_state.get("flashcards_loaded", False) and st.session_state.get("cached_flashcards"):
        return st.session_state.cached_flashcards
    
    # Use cached database call
    data = get_cached_flashcards_from_db(user_id)
    
    cards = []
    for row in data:
        cards.append({
            "card_id": row["card_id"],
            "front": row["front"],
            "back": row["back"],
            "difficulty": row["difficulty"],
            "interval": row["interval"],
            "ease_factor": row["ease_factor"],
            "due_date": row["due_date"],
            "reviews": row["reviews"],
            "last_result": row["last_result"]
        })
    
    # Store in session state
    st.session_state.cached_flashcards = cards
    st.session_state.flashcards_loaded = True
    return cards

# Modify _save_all_cards to clear cache:
def _save_all_cards(cards: list):
    """Save all flashcards and clear cache"""
    user_id = _get_user_id()
    if not user_id:
        return
    try:
        # Delete existing
        supabase().table("flashcards").delete().eq("user_id", user_id).execute()
        
        # Insert new
        if cards:
            inserts = []
            for card in cards:
                inserts.append({
                    "user_id": user_id,
                    "card_id": card.get("card_id", str(uuid.uuid4())),
                    "front": card["front"],
                    "back": card["back"],
                    "difficulty": card.get("difficulty", "medium"),
                    "interval": card.get("interval", 1),
                    "ease_factor": card.get("ease_factor", 2.5),
                    "due_date": card.get("due_date", date.today().isoformat()),
                    "reviews": card.get("reviews", 0),
                    "last_result": card.get("last_result")
                })
            supabase().table("flashcards").insert(inserts).execute()
        
        # Clear all caches
        get_cached_flashcards_from_db.clear()
        st.session_state.flashcards_loaded = False
        st.session_state.cached_flashcards = []
        
    except Exception as e:
        print(f"Error saving cards: {e}")

# Add session state initialization at the top of flashcards.py:
if "flashcards_loaded" not in st.session_state:
    st.session_state.flashcards_loaded = False
    st.session_state.cached_flashcards = []


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--teal:#06B6D4;--tg:rgba(6,182,212,0.15);--tb:rgba(6,182,212,0.3);--g1:rgba(255,255,255,0.05);--g2:rgba(255,255,255,0.09);--t1:#EEF2FF;--t2:#A8B4D8;--t3:#5A6A9A;--font:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;}
html,body,[class*="css"]{font-family:var(--font)!important;color:var(--t1)!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#060B2B 0%,#0D1547 55%,#182060 100%)!important;min-height:100vh;}

/* Action Card Styling - Added min-height for alignment */
.action-card {
    background: var(--g1);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1.5rem 1.4rem;
    text-align: center;
    margin-bottom: 0.8rem;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

/* Nav */
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"]{background:rgba(6,11,43,0.95)!important;backdrop-filter:blur(18px)!important;border-bottom:1px solid rgba(255,255,255,0.07)!important;padding:0.55rem 2rem!important;position:sticky!important;top:0!important;z-index:500!important;margin-bottom:0!important;align-items:center!important;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]{display:flex!important;align-items:center!important;padding-top:0!important;padding-bottom:0!important;gap:0!important;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"] .element-container,[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .element-container{margin:0!important;width:100%;}
.ab-pill-btn .stButton>button,.ab-pill-btn .stButton>button:focus{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:20px!important;font-family:var(--font)!important;font-size:0.78rem!important;font-weight:600!important;color:var(--teal)!important;padding:0.25rem 0.85rem!important;box-shadow:none!important;min-height:0!important;height:28px!important;white-space:nowrap!important;}
.ab-pill-btn .stButton>button:hover{background:rgba(6,182,212,0.15)!important;border-color:var(--teal)!important;transform:none!important;}
.ab-avatar-circle{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border:2px solid rgba(6,182,212,0.45);display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:#fff;}

/* Selectbox */
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child{background:#dbeafe!important;border:1px solid rgba(6,182,212,0.3)!important;border-radius:10px!important;color:#1e3a5f!important;font-size:0.84rem!important;}
[data-testid="stSelectbox"] [data-baseweb="select"] svg{color:#1e3a5f!important;fill:#1e3a5f!important;}
[data-testid="stSelectbox"] label{color:var(--t2)!important;font-size:0.78rem!important;font-weight:500!important;}

/* ══ FLASHCARD ══ */
.fc-wrap{perspective:1000px;width:100%;max-width:580px;margin:0 auto;height:280px;cursor:pointer;}
.fc-inner{position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform 0.5s ease;}
.fc-inner.flipped{transform:rotateY(180deg);}
.fc-face{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:2rem 2.2rem;text-align:center;box-sizing:border-box;}
.fc-front{background:linear-gradient(135deg,#0D1547,#1B2B6B);border:1px solid rgba(6,182,212,0.35);box-shadow:0 8px 32px rgba(0,0,0,0.4);}
.fc-back{background:linear-gradient(135deg,#07102E,#0D1547);border:1px solid rgba(6,182,212,0.5);box-shadow:0 8px 32px rgba(0,0,0,0.4);transform:rotateY(180deg);}
.fc-label{font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--teal);margin-bottom:0.8rem;}
.fc-text{font-size:1.05rem;font-weight:600;color:#EEF2FF;line-height:1.6;}
.fc-back .fc-text{font-size:0.97rem;font-weight:400;color:#A8B4D8;}
.fc-hint{font-size:0.72rem;color:var(--t3);margin-top:1rem;}
.fc-diff{display:inline-block;font-size:0.67rem;font-weight:700;border-radius:20px;padding:0.15rem 0.55rem;margin-bottom:0.6rem;}
.fc-diff.easy{color:#10B981;background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);}
.fc-diff.medium{color:#F59E0B;background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);}
.fc-diff.hard{color:#EF4444;background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);}

/* ══ REVIEW BUTTONS ══ */
.easy-btn .stButton>button{background:rgba(16,185,129,0.12)!important;color:#10B981!important;-webkit-text-fill-color:#10B981!important;border:1px solid rgba(16,185,129,0.3)!important;border-radius:12px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;height:48px!important;width:100%!important;box-shadow:none!important;}
.hard-btn .stButton>button{background:rgba(239,68,68,0.1)!important;color:#f87171!important;-webkit-text-fill-color:#f87171!important;border:1px solid rgba(239,68,68,0.3)!important;border-radius:12px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;height:48px!important;width:100%!important;box-shadow:none!important;}
.flip-btn .stButton>button{background:rgba(6,182,212,0.1)!important;color:var(--teal)!important;-webkit-text-fill-color:var(--teal)!important;border:1px solid rgba(6,182,212,0.35)!important;border-radius:12px!important;font-family:var(--font)!important;font-weight:600!important;font-size:0.88rem!important;height:40px!important;width:100%!important;box-shadow:none!important;}
.teal-btn .stButton>button{background:var(--teal)!important;color:#060B2B!important;border:none!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;padding:0.65rem 1.8rem!important;box-shadow:0 0 16px rgba(6,182,212,0.25)!important;}
.ghost-btn .stButton>button{background:var(--g1)!important;color:var(--t2)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:10px!important;font-family:var(--font)!important;font-size:0.85rem!important;padding:0.5rem 1rem!important;box-shadow:none!important;width:100%!important;}

/* ══ DECK LIST ══ */
.deck-card{background:var(--g1);border:1px solid rgba(255,255,255,0.09);border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.5rem;display:flex;align-items:center;justify-content:space-between;}
.deck-title{font-size:0.92rem;font-weight:700;color:#EEF2FF;margin-bottom:0.15rem;}
.deck-meta{font-size:0.72rem;color:var(--t3);}
.deck-due{font-size:0.72rem;font-weight:700;color:var(--teal);margin-left:0.5rem;}

/* ══ PROGRESS BAR ══ */
.fc-prog-bg{background:rgba(255,255,255,0.07);border-radius:20px;height:6px;overflow:hidden;margin-bottom:0.4rem;}
.fc-prog-fill{height:6px;border-radius:20px;background:linear-gradient(90deg,#1B2B6B,#06B6D4);transition:width 0.4s;}

/* ══ STATS CHIPS ══ */
.stat-chip{display:inline-flex;align-items:center;gap:0.35rem;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.09);border-radius:20px;padding:0.22rem 0.7rem;font-size:0.75rem;color:var(--t2);margin:0.15rem;}
.stat-chip strong{color:#EEF2FF;}

::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:2px;}

/* --- MOBILE RESPONSIVENESS OVERRIDE --- */
@media (max-width: 768px) {
    [data-testid="stHeader"] ~ section [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; 
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
    }
    [data-testid="stHeader"] ~ section [data-testid="stColumn"] {
        width: auto !important;
        min-width: 0px !important;
        flex: 1 1 auto !important;
    }
    div[data-testid="stColumn"] div[style*="justify-content:flex-end"] {
        display: none !important;
    }
    .auth-logo-icon {
        width: 30px !important;
        height: 30px !important;
        font-size: 0.9rem !important;
    }
}
/* Make spinner text white */
div[data-testid="stSpinner"] div {
    color: #EEF2FF !important;
}
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
for k, v in {
    "student_name": "Student", "username": None,
    "active_course": None, "active_topic": None,
    "uploaded_files": [],
    "fc_deck": [],
    "fc_card_idx": 0,
    "fc_flipped": False,
    "fc_session_easy": 0,
    "fc_session_hard": 0,
    "fc_view": "home",
}.items():
    if k not in st.session_state: st.session_state[k] = v

if "tracker" not in st.session_state or st.session_state.tracker is None:
    st.session_state.tracker = ProgressTracker(st.session_state.student_name)
    _sf = f"{st.session_state.get('username','user')}_progress.json"
    st.session_state.tracker.load_from_file(_sf)

_sf = f"{st.session_state.get('username','user')}_progress.json"
_fc_file = f"{st.session_state.get('username','user')}_flashcards.json"
sname = st.session_state.student_name
initials = (sname[0] if sname else "S").upper()

if "flashcards_loaded" not in st.session_state:
    st.session_state.flashcards_loaded = False
    st.session_state.cached_flashcards = []
    st.session_state.flashcards_last_load = None
    st.session_state.flashcards_needs_refresh = False

# ============================================
# CACHED SUPABASE FUNCTIONS
# ============================================
def _get_user_id() -> str | None:
    """Get current user ID from session state (no DB call)"""
    return st.session_state.get("user_id")

def _load_all_cards() -> list:
    """Load flashcards - ONLY calls Supabase ONCE per session"""
    # If already loaded and no refresh needed, return cached
    if st.session_state.flashcards_loaded and not st.session_state.flashcards_needs_refresh:
        return st.session_state.cached_flashcards
    
    # Otherwise, load from Supabase
    user_id = _get_user_id()
    if not user_id:
        return []
    
    try:
        result = supabase().table("flashcards").select("*").eq("user_id", user_id).execute()
        cards = []
        for row in result.data:
            cards.append({
                "card_id": row["card_id"],
                "front": row["front"],
                "back": row["back"],
                "difficulty": row["difficulty"],
                "interval": row["interval"],
                "ease_factor": row["ease_factor"],
                "due_date": row["due_date"],
                "reviews": row["reviews"],
                "last_result": row["last_result"]
            })
        
        # Store in session state
        st.session_state.cached_flashcards = cards
        st.session_state.flashcards_loaded = True
        st.session_state.flashcards_needs_refresh = False
        st.session_state.flashcards_last_load = datetime.now()
        
        return cards
    except Exception as e:
        print(f"Error loading flashcards: {e}")
        return []

def _save_all_cards(cards: list):
    """Save flashcards and mark cache as dirty"""
    user_id = _get_user_id()
    if not user_id:
        return
    
    try:
        # Delete all existing cards for this user
        supabase().table("flashcards").delete().eq("user_id", user_id).execute()
        
        # Insert new cards
        if cards:
            inserts = []
            for card in cards:
                inserts.append({
                    "user_id": user_id,
                    "card_id": card.get("card_id", str(uuid.uuid4())),
                    "front": card["front"],
                    "back": card["back"],
                    "difficulty": card.get("difficulty", "medium"),
                    "interval": card.get("interval", 1),
                    "ease_factor": card.get("ease_factor", 2.5),
                    "due_date": card.get("due_date", date.today().isoformat()),
                    "reviews": card.get("reviews", 0),
                    "last_result": card.get("last_result")
                })
            supabase().table("flashcards").insert(inserts).execute()
        
        # Mark cache as needing refresh
        st.session_state.cached_flashcards = cards
        st.session_state.flashcards_needs_refresh = False
        
    except Exception as e:
        print(f"Error saving cards: {e}")

def _get_due_cards(cards: list) -> list:
    """Get cards due for review - uses cached cards"""
    today = date.today().isoformat()
    return [c for c in cards if c.get("due_date", today) <= today]

def _schedule_card(card: dict, result: str) -> dict:
    """Update card schedule based on review result."""
    interval = card.get("interval", 1)
    ease = card.get("ease_factor", 2.5)
    
    if result == "easy":
        ease = min(2.5, ease + 0.1)
        interval = max(1, round(interval * ease))
    else:
        ease = max(1.3, ease - 0.15)
        interval = 1
    
    card["interval"] = interval
    card["ease_factor"] = round(ease, 2)
    card["due_date"] = (date.today() + timedelta(days=interval)).isoformat()
    card["reviews"] = card.get("reviews", 0) + 1
    card["last_result"] = result
    
    # Update in database immediately
    user_id = _get_user_id()
    if user_id:
        try:
            supabase().table("flashcards").update({
                "interval": interval,
                "ease_factor": round(ease, 2),
                "due_date": card["due_date"],
                "reviews": card["reviews"],
                "last_result": result,
                "updated_at": datetime.now().isoformat()
            }).eq("user_id", user_id).eq("card_id", card["card_id"]).execute()
            
            # Update cached version
            for i, cached_card in enumerate(st.session_state.cached_flashcards):
                if cached_card["card_id"] == card["card_id"]:
                    st.session_state.cached_flashcards[i] = card.copy()
                    break
                    
        except Exception:
            pass
    
    return card


# ── NAV ────────────────────────────────────────────────────────────────────────
_l, _, _h, _p, _pr, _av = st.columns([3, 4, 0.5, 0.5, 0.5, 0.5])
with _l:
    st.markdown('<div style="display:flex;align-items:center;gap:0.5rem;"><div style="width:26px;height:26px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;">🤖</div><span style="font-size:0.97rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AlgoBuddy · Flashcards</span></div>', unsafe_allow_html=True)
with _h:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🏠", key="nh", use_container_width=True): st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _p:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🧮", key="np", use_container_width=True): st.switch_page("pages/practice.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _pr:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("📈", key="npr", use_container_width=True): st.switch_page("pages/progress.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _av:
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:center;"><div class="ab-avatar-circle">{initials}</div></div>', unsafe_allow_html=True)
st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.07);"></div>', unsafe_allow_html=True)

all_cards = _load_all_cards()
due_cards = _get_due_cards(all_cards)

# ══ VIEW: HOME ════════════════════════════════════════════════════════════════
if st.session_state.fc_view == "home":
    _, main, _ = st.columns([1, 7, 1])
    with main:
        st.markdown("<div style='padding:2rem 0 4rem'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:1.8rem;">
            <div style="font-size:1.3rem;font-weight:800;color:#fff;letter-spacing:-0.03em;">🃏 Flashcards</div>
            <div style="font-size:0.85rem;color:var(--t3);margin-top:0.2rem;">Review due cards or generate new ones from your notes or course topic.</div>
        </div>""", unsafe_allow_html=True)

        total = len(all_cards)
        due_n = len(due_cards)
        mastered = len([c for c in all_cards if c.get("ease_factor", 2.5) >= 2.4 and c.get("reviews", 0) >= 3])
        st.markdown(f"""
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
            <span class="stat-chip">🃏 <strong>{total}</strong> total cards</span>
            <span class="stat-chip"> 🗓️ <strong>{due_n}</strong> due today</span>
            <span class="stat-chip">🏆<strong>{mastered}</strong> mastered</span>
            <span class="stat-chip">🔥 <strong>{st.session_state.tracker.stats.get('flashcards_reviewed',0)}</strong> reviewed all-time</span>
        </div>""", unsafe_allow_html=True)

        # Corrected Action buttons section
        r1, r2, r3 = st.columns(3, gap="large")
        with r1:
            st.markdown(f'<div class="action-card"><div style="font-size:1.8rem;margin-bottom:0.5rem;">📅</div><div style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">Review Due</div><div style="font-size:0.8rem;color:var(--t2);margin-bottom:1rem;">{due_n} card{"s" if due_n!=1 else ""} waiting</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
            if st.button("Start Review →", key="start_review", use_container_width=True, disabled=due_n==0):
                st.session_state.fc_deck      = due_cards.copy()
                st.session_state.fc_card_idx  = 0
                st.session_state.fc_flipped   = False
                st.session_state.fc_view      = "review"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="action-card"><div style="font-size:1.8rem;margin-bottom:0.5rem;">🔄</div><div style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">Review All</div><div style="font-size:0.8rem;color:var(--t2);margin-bottom:1rem;">Go through every card</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            if st.button("Review All →", key="review_all", use_container_width=True, disabled=total==0):
                st.session_state.fc_deck      = all_cards.copy()
                st.session_state.fc_card_idx  = 0
                st.session_state.fc_flipped   = False
                st.session_state.fc_view      = "review"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with r3:
            st.markdown('<div class="action-card"><div style="font-size:1.8rem;margin-bottom:0.5rem;">✨</div><div style="font-size:0.95rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">Generate Cards</div><div style="font-size:0.8rem;color:var(--t2);margin-bottom:1rem;">From notes or topic</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            if st.button("Generate →", key="go_gen", use_container_width=True):
                st.session_state.fc_view = "generate"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        if all_cards:
            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)
            dcol1, dcol2 = st.columns([5, 1])
            with dcol1:
                st.markdown('<div style="font-size:0.67rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--t3);margin-bottom:0.7rem;">Due Cards</div>', unsafe_allow_html=True)
            with dcol2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("🗑 Clear all", key="del_all", use_container_width=True):
                    _save_all_cards([])
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            today = date.today().isoformat()
            due_display = [c for c in all_cards if c.get("due_date", today) <= today]

            if due_display:
                for i, card in enumerate(due_display[:20]):
                    diff = card.get("difficulty", "medium")
                    reviews = card.get("reviews", 0)
                    label = "New" if reviews == 0 else f"{reviews} review{'s' if reviews != 1 else ''}"
                    st.markdown(f"""
                    <div class="deck-card">
                        <div class="deck-info">
                            <div class="deck-title">{card['front'][:80]}{'…' if len(card['front'])>80 else ''}</div>
                            <div class="deck-meta">
                                <span class="fc-diff {diff}">{diff}</span>
                                · {label}
                                <span class="deck-due">Due today</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="text-align:center;padding:1.5rem 0;color:var(--t3);font-size:0.88rem;">'
                    '✅ All caught up — no cards due today.'
                    '</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

# ══ VIEW: REVIEW ══════════════════════════════════════════════════════════════
elif st.session_state.fc_view == "review":
    deck    = st.session_state.fc_deck
    idx     = st.session_state.fc_card_idx
    total_d = len(deck)
 
    if idx >= total_d:
        # Session complete
        easy_n = st.session_state.fc_session_easy
        hard_n = st.session_state.fc_session_hard
        reviewed = easy_n + hard_n
 
        st.session_state.tracker.record_flashcard_review(reviewed)
        st.session_state.tracker.save_to_file(_sf)
        # Force cache refresh so home shows updated due counts
        st.session_state.fc_needs_reload = True
 
        _, mc, _ = st.columns([1, 5, 1])
        with mc:
            st.markdown(f"""
            <div style="text-align:center;padding:5rem 1rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">🎉</div>
                <div style="font-size:1.3rem;font-weight:800;color:#fff;margin-bottom:0.5rem;">Session Complete!</div>
                <div style="font-size:0.9rem;color:var(--t2);margin-bottom:2rem;">
                    {reviewed} cards reviewed &nbsp;·&nbsp;
                    <span style="color:#10B981;">{easy_n} easy</span> &nbsp;·&nbsp;
                    <span style="color:#f87171;">{hard_n} hard</span>
                </div>
            </div>""", unsafe_allow_html=True)
            c1, c2 = st.columns(2, gap="large")
            with c1:
                st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
                if st.button("Review Again", key="review_again", use_container_width=True):
                    st.session_state.fc_card_idx  = 0
                    st.session_state.fc_flipped   = False
                    st.session_state.fc_session_easy = 0
                    st.session_state.fc_session_hard = 0
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("← Back to Decks", key="back_home", use_container_width=True):
                    st.session_state.fc_needs_reload = True
                    st.session_state.fc_view = "home"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        card     = deck[idx]
        flipped  = st.session_state.fc_flipped
        diff     = card.get("difficulty", "medium")
        progress = int((idx / total_d) * 100)
 
        _, mc, _ = st.columns([1, 6, 1])
        with mc:
            st.markdown("<div style='padding:2rem 0'>", unsafe_allow_html=True)
 
            # Progress
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                <span style="font-size:0.72rem;color:var(--t3);">Card {idx+1} of {total_d}</span>
                <span style="font-size:0.72rem;color:var(--teal);font-weight:600;">
                    ✅ {st.session_state.fc_session_easy} &nbsp; ❌ {st.session_state.fc_session_hard}
                </span>
            </div>
            <div class="fc-prog-bg"><div class="fc-prog-fill" style="width:{progress}%;"></div></div>
            <div style="height:1.2rem"></div>""", unsafe_allow_html=True)
 
            # Card — CSS flip via class toggle
            flip_class = "flipped" if flipped else ""
            st.markdown(f"""
            <div class="fc-wrap">
                <div class="fc-inner {flip_class}">
                    <div class="fc-face fc-front">
                        <span class="fc-diff {diff}">{diff.upper()}</span>
                        <div class="fc-label">Question</div>
                        <div class="fc-text">{card['front']}</div>
                        <div class="fc-hint">Click Reveal Answer to see the answer</div>
                    </div>
                    <div class="fc-face fc-back">
                        <div class="fc-label">Answer</div>
                        <div class="fc-text">{card['back']}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
 
            st.markdown('<div style="height:1.4rem"></div>', unsafe_allow_html=True)
 
            if not flipped:
                _, fb, _ = st.columns([2, 3, 2])
                with fb:
                    st.markdown('<div class="flip-btn" style="display:flex;justify-content:center;">', unsafe_allow_html=True)
                    if st.button("👁 Reveal Answer", key="flip", use_container_width=False):
                        st.session_state.fc_flipped = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-size:0.78rem;color:var(--t3);text-align:center;margin-bottom:0.8rem;">How well did you know this?</div>', unsafe_allow_html=True)
                _, hc, gap, ec, _ = st.columns([1, 2, 0.3, 2, 1])
                with hc:
                    st.markdown('<div class="hard-btn">', unsafe_allow_html=True)
                    if st.button("😓 Hard", key="hard_btn", use_container_width=True):
                        _schedule_card(card, "hard")   # updates Supabase directly
                        st.session_state.fc_session_hard += 1
                        st.session_state.fc_card_idx += 1
                        st.session_state.fc_flipped = False
                        st.session_state.tracker.record_study_session()
                        st.session_state.tracker.save_to_file(_sf)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with ec:
                    st.markdown('<div class="easy-btn">', unsafe_allow_html=True)
                    if st.button("😊 Easy", key="easy_btn", use_container_width=True):
                        _schedule_card(card, "easy")   # updates Supabase directly
                        st.session_state.fc_session_easy += 1
                        st.session_state.fc_card_idx += 1
                        st.session_state.fc_flipped = False
                        st.session_state.tracker.record_study_session()
                        st.session_state.tracker.save_to_file(_sf)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
 
            # Skip / back home
            st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
            sk1, sk2 = st.columns(2, gap="large")
            with sk1:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("⏭ Skip", key="skip_btn", use_container_width=True):
                    st.session_state.fc_card_idx += 1
                    st.session_state.fc_flipped = False
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with sk2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("← Exit Review", key="exit_rev", use_container_width=True):
                    st.session_state.fc_view = "home"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
 
            st.markdown("</div>", unsafe_allow_html=True)
 
# ══ VIEW: GENERATE ════════════════════════════════════════════════════════════
elif st.session_state.fc_view == "generate":
    _, gc, _ = st.columns([1, 6, 1])
    with gc:
        st.markdown("<div style='padding:2rem 0 4rem'>", unsafe_allow_html=True)
        st.markdown("""<div style="margin-bottom:1.5rem;"><div style="font-size:1.1rem;font-weight:800;color:#fff;">✨ Generate Flashcards</div><div style="font-size:0.85rem;color:var(--t3);margin-top:0.2rem;">AI generates cards from your uploaded notes or a course topic.</div></div>""", unsafe_allow_html=True)
        text_files = [f for f in st.session_state.get("uploaded_files", []) if f["type"] == "text"]
        source_options = ["Course topic"] + [f["name"] for f in text_files]
        source = st.selectbox("Generate from", source_options, key="fc_source")
        if source == "Course topic":
            course_keys = list(COURSES.keys())
            course_labels = {cid: f"{c['icon']} {c['display_name']}" for cid, c in COURSES.items()}
            cur_ci = course_keys.index(st.session_state.active_course) if st.session_state.active_course in course_keys else 0
            sel_course = st.selectbox("Course", course_keys, index=cur_ci, format_func=lambda k: course_labels[k], key="fc_course")
            tids = get_all_topic_ids_for_course(sel_course)
            topic_keys = [None] + tids
            def tlbl(t): return "All topics" if t is None else (get_topic(sel_course, t) or {}).get("display_name", t)
            cur_t = st.session_state.active_topic if st.session_state.active_topic in tids else None
            sel_topic = st.selectbox("Topic", topic_keys, index=topic_keys.index(cur_t), format_func=tlbl, key="fc_topic")
            file_ctx = None
            topic_label = tlbl(sel_topic) if sel_topic else course_labels[sel_course]
        else:
            file_data = next((f for f in text_files if f["name"] == source), None)
            file_ctx = file_data["content"] if file_data else None
            sel_course = st.session_state.active_course
            sel_topic = st.session_state.active_topic
            topic_label = source
        count = st.selectbox("How many cards?", [5, 8, 10, 15, 20], index=1, key="fc_count")
        st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
            if st.button("✨ Generate Cards", key="gen_cards", use_container_width=True):
                with st.spinner(f"Generating {count} flashcards..."):
                    try:
                        new_cards = generate_flashcards(sel_course, sel_topic, count, file_ctx)
                        if not new_cards:
                            raise ValueError("AI returned empty list")
                    except Exception as e:
                        st.error(f"⚠️ AI generation failed: {e}")
                        st.warning("Using fallback generator (simple cards from your text/topic).")
                        # Fallback: create simple cards from the context
                        if file_ctx:
                            # Split text into chunks and turn each into a Q/A pair
                            lines = [line.strip() for line in file_ctx.split('\n') if line.strip()]
                            new_cards = []
                            for i, line in enumerate(lines[:count*2]):   # roughly half the lines become questions
                                if i % 2 == 0 and i+1 < len(lines):
                                    front = f"Explain: {line}"
                                    back = lines[i+1]
                                else:
                                    front = f"What is '{line[:50]}' about?"
                                    back = f"This is a summary of {line[:100]}..."
                                new_cards.append({"front": front, "back": back, "difficulty": "medium"})
                            if not new_cards:
                                new_cards = [{"front": "No content to generate from", "back": "Please upload notes or select a topic.", "difficulty": "medium"}]
                        elif sel_course and sel_topic:
                            # Create generic topic-based cards
                            topic_display = get_topic(sel_course, sel_topic).get('display_name', sel_topic)
                            new_cards = [
                                {"front": f"What is the main concept of '{topic_display}'?",
                                 "back": f"Review your course material for '{topic_display}'.",
                                 "difficulty": "medium"},
                                {"front": f"Give an example related to '{topic_display}'.",
                                 "back": "Think of a real-world application from the lesson.",
                                 "difficulty": "medium"},
                            ] * (count // 2)
                            new_cards = new_cards[:count]
                        else:
                            new_cards = []
                            st.error("No context available. Please select a topic or upload a file.")
                if new_cards:
                    existing = _load_all_cards()
                    today = date.today().isoformat()
                    for card in new_cards:
                        card.update({"card_id": str(uuid.uuid4()), 
                                     "due_date": today, 
                                     "interval": 1, 
                                     "ease_factor": 2.5, 
                                     "reviews": 0, 
                                     "last_result": None})
                    existing.extend(new_cards)
                    _save_all_cards(existing)
                    st.success(f"✅ {len(new_cards)} flashcards added!")
                    st.session_state.fc_view = "home"
                    st.rerun()
                else:
                    st.error("No flashcards could be generated. Please try again with different input.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            if st.button("← Back", key="back_gen", use_container_width=True):
                st.session_state.fc_view = "home"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)