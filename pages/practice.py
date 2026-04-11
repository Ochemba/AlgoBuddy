import streamlit as st

st.set_page_config(page_title="Practice · AlgoBuddy", page_icon="🧮", layout="wide", initial_sidebar_state="collapsed")

from tutor_engine import generate_practice_problem, check_student_answer, check_fill_blank_answer, check_mcq_answer
from course_registry import COURSES, get_all_topic_ids_for_course, get_topic
from progress_tracker import ProgressTracker, BADGES



st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--teal:#06B6D4;--tg:rgba(6,182,212,0.15);--tb:rgba(6,182,212,0.3);--g1:rgba(255,255,255,0.05);--t1:#EEF2FF;--t2:#A8B4D8;--t3:#5A6A9A;--font:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;}
html,body,[class*="css"]{font-family:var(--font)!important;color:var(--t1)!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#060B2B 0%,#0D1547 55%,#182060 100%)!important;min-height:100vh;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"]{background:rgba(6,11,43,0.95)!important;backdrop-filter:blur(18px)!important;border-bottom:1px solid rgba(255,255,255,0.07)!important;padding:0.55rem 2rem!important;position:sticky!important;top:0!important;z-index:500!important;margin-bottom:0!important;align-items:center!important;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]{display:flex!important;align-items:center!important;padding-top:0!important;padding-bottom:0!important;gap:0!important;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"] .element-container,[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .element-container{margin:0!important;width:100%;}
.ab-pill-btn .stButton>button,.ab-pill-btn .stButton>button:focus{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:20px!important;font-family:var(--font)!important;font-size:0.78rem!important;font-weight:600!important;color:var(--teal)!important;padding:0.25rem 0.85rem!important;box-shadow:none!important;min-height:0!important;height:28px!important;white-space:nowrap!important;}
.ab-pill-btn .stButton>button:hover{background:rgba(6,182,212,0.15)!important;border-color:var(--teal)!important;transform:none!important;}
.ab-avatar-circle{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border:2px solid rgba(6,182,212,0.45);display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:#fff;}
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child{background:#dbeafe!important;border:1px solid rgba(6,182,212,0.3)!important;border-radius:10px!important;color:#1e3a5f!important;font-size:0.84rem!important;}
[data-testid="stSelectbox"] [data-baseweb="select"] svg{color:#1e3a5f!important;fill:#1e3a5f!important;}
[data-testid="stSelectbox"] label{color:var(--t2)!important;font-size:0.78rem!important;font-weight:500!important;margin-bottom:0.2rem!important;}
html body [role="option"],html body [role="option"] *{color:#0f172a!important;background-color:#f8fafc!important;}
html body [role="option"]:hover{background-color:#e2e8f0!important;}
html body [role="option"][aria-selected="true"]{background-color:#bae6fd!important;color:#0c4a6e!important;font-weight:600!important;border-left:3px solid #06B6D4!important;}
.teal-btn .stButton>button{background:var(--teal)!important;color:#060B2B!important;border:none!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;padding:0.65rem 1.8rem!important;box-shadow:0 0 16px rgba(6,182,212,0.25)!important;}
.teal-btn .stButton>button:hover{background:#22D3EE!important;transform:none!important;}
.ghost-btn .stButton>button{background:var(--g1)!important;color:var(--t2)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:10px!important;font-family:var(--font)!important;font-size:0.85rem!important;padding:0.55rem 1.4rem!important;box-shadow:none!important;}
.ghost-btn .stButton>button:hover{background:var(--tg)!important;border-color:var(--teal)!important;color:#fff!important;transform:none!important;}
.next-btn .stButton>button{background:rgba(16,185,129,0.12)!important;color:#10B981!important;border:1px solid rgba(16,185,129,0.3)!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:600!important;font-size:0.9rem!important;padding:0.65rem 1.8rem!important;box-shadow:none!important;}
.next-btn .stButton>button:hover{background:rgba(16,185,129,0.2)!important;transform:none!important;}
.prob-card{background:var(--g1);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:1.8rem 2rem;}
.prob-title{font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--teal);margin-bottom:0.8rem;}
.prob-type-badge{display:inline-block;font-size:0.68rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;border-radius:20px;padding:0.15rem 0.6rem;margin-left:0.6rem;vertical-align:middle;}
.badge-fill{background:rgba(139,92,246,0.15);color:#a78bfa;border:1px solid rgba(139,92,246,0.3);}
.badge-mcq{background:rgba(6,182,212,0.15);color:#06B6D4;border:1px solid rgba(6,182,212,0.3);}
.badge-standard{background:rgba(245,158,11,0.12);color:#F59E0B;border:1px solid rgba(245,158,11,0.3);}
.prob-text{font-size:0.97rem;line-height:1.75;color:var(--t1);}
.diff-pill{display:inline-block;padding:0.2rem 0.7rem;border-radius:20px;font-size:0.73rem;font-weight:600;margin-left:0.7rem;vertical-align:middle;}
.easy{background:rgba(16,185,129,0.15);color:#10B981;border:1px solid rgba(16,185,129,0.3);}
.medium{background:rgba(245,158,11,0.15);color:#F59E0B;border:1px solid rgba(245,158,11,0.3);}
.hard{background:rgba(239,68,68,0.15);color:#EF4444;border:1px solid rgba(239,68,68,0.3);}
.hint-card{background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.28);border-radius:12px;padding:1.1rem 1.3rem;}
.hint-lbl{font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#F59E0B;margin-bottom:0.4rem;}
.hint-txt{font-size:0.92rem;color:#FDE68A;line-height:1.65;}

/* MCQ options */
.mcq-option{display:flex;align-items:center;gap:0.9rem;background:rgba(255,255,255,0.04);border:1.5px solid rgba(255,255,255,0.1);border-radius:12px;padding:0.85rem 1.1rem;margin-bottom:0.55rem;cursor:pointer;transition:border-color 0.15s,background 0.15s;}
.mcq-option:hover{background:rgba(6,182,212,0.07);border-color:rgba(6,182,212,0.35);}
.mcq-option.selected{background:rgba(6,182,212,0.1);border-color:var(--teal);}
.mcq-option.correct{background:rgba(16,185,129,0.1);border-color:#10B981;}
.mcq-option.wrong{background:rgba(239,68,68,0.07);border-color:#EF4444;}
.mcq-letter{width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:700;color:var(--t2);flex-shrink:0;}
.mcq-option.selected .mcq-letter{background:var(--tg);border-color:var(--teal);color:var(--teal);}
.mcq-option.correct .mcq-letter{background:rgba(16,185,129,0.2);border-color:#10B981;color:#10B981;}
.mcq-option.wrong .mcq-letter{background:rgba(239,68,68,0.1);border-color:#EF4444;color:#EF4444;}
.mcq-text{font-size:0.93rem;color:var(--t1);line-height:1.5;}

[data-testid="stTextArea"] textarea,[data-testid="stTextArea"] textarea:focus{background:#dbeafe!important;color:#1e3a5f!important;caret-color:#1e3a5f!important;border:1.5px solid rgba(6,182,212,0.35)!important;border-radius:12px!important;font-family:var(--font)!important;font-size:0.94rem!important;line-height:1.65!important;padding:0.85rem 1.1rem!important;resize:vertical!important;min-height:120px!important;}
[data-testid="stTextArea"] textarea:focus{border-color:#06B6D4!important;box-shadow:0 0 0 3px rgba(6,182,212,0.15)!important;}
[data-testid="stTextArea"] textarea::placeholder{color:#7ba8c9!important;}
[data-testid="stTextArea"] label{color:var(--t2)!important;font-size:0.85rem!important;font-weight:500!important;margin-bottom:0.3rem!important;}
[data-testid="stTextInput"] input{background:#dbeafe!important;color:#1e3a5f!important;-webkit-text-fill-color:#1e3a5f!important;border:1.5px solid rgba(6,182,212,0.35)!important;border-radius:8px!important;font-family:var(--font)!important;font-size:0.9rem!important;caret-color:#1e3a5f!important;}
[data-testid="stTextInput"] input:focus{border-color:#06B6D4!important;box-shadow:0 0 0 2px rgba(6,182,212,0.2)!important;}
[data-testid="stTextInput"] input::placeholder{color:#7ba8c9!important;-webkit-text-fill-color:#7ba8c9!important;}
[data-testid="stTextInput"] [data-baseweb="base-input"],[data-testid="stTextInput"] div[style]{background:#dbeafe!important;}
[data-testid="stTextInput"] label{color:var(--t2)!important;font-size:0.8rem!important;}
.res-ok{background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.28);border-radius:12px;padding:1.2rem 1.4rem;}
.res-no{background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.22);border-radius:12px;padding:1.2rem 1.4rem;}
.res-lbl{font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;}
.res-txt{font-size:0.93rem;color:var(--t1);line-height:1.65;}
.xp-toast{display:inline-flex;align-items:center;gap:0.4rem;background:rgba(6,182,212,0.12);border:1px solid rgba(6,182,212,0.3);border-radius:20px;padding:0.2rem 0.75rem;font-size:0.78rem;color:var(--teal);font-weight:600;margin-left:0.6rem;}
.seed-banner{background:rgba(6,182,212,0.07);border:1px solid rgba(6,182,212,0.25);border-radius:8px;padding:0.5rem 0.9rem;font-size:0.82rem;color:#A8B4D8;}
[data-testid="stMetric"]{background:var(--g1)!important;border:1px solid rgba(255,255,255,0.09)!important;border-radius:12px!important;padding:0.9rem 1.1rem!important;}
[data-testid="stMetricValue"]{color:var(--teal)!important;font-weight:700!important;font-family:var(--mono)!important;}
[data-testid="stMetricLabel"]{color:var(--t3)!important;font-size:0.75rem!important;}
.gap-sm{height:0.8rem;}.gap-md{height:1.2rem;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:2px;}

/* ══ TOAST NOTIFICATIONS ══ */
@keyframes slideIn{from{transform:translateX(120%);opacity:0;}to{transform:translateX(0);opacity:1;}}
@keyframes fadeOut{from{opacity:1;}to{opacity:0;transform:translateX(120%);}}
.toast-container{position:fixed;top:70px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:0.5rem;pointer-events:none;}
.toast{display:flex;align-items:center;gap:0.6rem;padding:0.65rem 1rem;border-radius:12px;font-family:var(--font);font-size:0.84rem;font-weight:600;box-shadow:0 4px 20px rgba(0,0,0,0.4);animation:slideIn 0.35s ease forwards;pointer-events:none;min-width:180px;}
.toast.xp{background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.4);color:#06B6D4;}
.toast.badge{background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.4);color:#a78bfa;}
.toast.fading{animation:fadeOut 0.4s ease forwards;}
/* Make spinner text white */
div[data-testid="stSpinner"] div {
    color: #EEF2FF !important;
}

.stSpinner > div {
    color: #EEF2FF !important;
}
/* --- MOBILE RESPONSIVENESS OVERRIDE --- */
@media (max-width: 768px) {
    /* 1. Force the Top Navbar to stay in a row */
    [data-testid="stHeader"] ~ section [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; 
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: space-between !important;
    }

    /* 2. Shrink the gap between icons so they don't overflow */
    [data-testid="stHeader"] ~ section [data-testid="stColumn"] {
        width: auto !important;
        min-width: 0px !important;
        flex: 1 1 auto !important;
    }

    /* 3. Hide the Persona Name (c5) on mobile to save space */
    /* This targets the specific div holding the persona text */
    div[data-testid="stColumn"] div[style*="justify-content:flex-end"] {
        display: none !important;
    }

    /* 4. Ensure the Logo doesn't take up too much room */
    .auth-logo-icon {
        width: 30px !important;
        height: 30px !important;
        font-size: 0.9rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
for k, v in {
    "practice_problem": None, "practice_result": None, "hints_revealed": 0,
    "active_course": None, "active_topic": None,
    "student_name": "Student", "username": None,
    "session_score": {"correct": 0, "total": 0},
    "practice_seed": None, "uploaded_files": [], "blank_answers": {},
    "_notes_xp_awarded": False,
    "mcq_selected": None,          # which MCQ option the student clicked
    "_pending_toasts": [],         # list of {type, message} to show
    "_shown_toasts": [],           # toasts currently displayed (with fade state)
    "_prev_badges": [],            # badge snapshot before last action
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

username = st.session_state.get("username", "user")
_sf = f"{username}_progress.json"

if "tracker" not in st.session_state or st.session_state.tracker is None:
    st.session_state.tracker = ProgressTracker(st.session_state.student_name)
    st.session_state.tracker.load_from_file(_sf)

_seed       = st.session_state.practice_seed
_text_files = [f for f in st.session_state.get("uploaded_files", []) if f["type"] == "text" and f["content"]]
_file_ctx   = "\n\n".join(f"=== {f['name']} ===\n{f['content']}" for f in _text_files) if _text_files else None
_file_names = [f["name"] for f in _text_files]

if _file_ctx and not st.session_state._notes_xp_awarded:
    st.session_state.tracker.record_notes_upload()
    st.session_state.tracker.save_to_file(_sf)
    st.session_state._notes_xp_awarded = True

if _seed and not st.session_state.practice_problem:
    st.session_state["_auto_generate"] = True

sname    = st.session_state.student_name
initials = (sname[0] if sname else "S").upper()


# ══ TOAST HELPERS ═════════════════════════════════════════════════════════════

def _queue_xp_toast(amount: int, reason: str = ""):
    label = f"+{amount} XP" + (f" · {reason}" if reason else "")
    st.session_state._pending_toasts.append({"type": "xp", "message": label})

def _queue_badge_toasts(new_badge_ids: list):
    badge_map = {b["id"]: b for b in BADGES}
    for bid in new_badge_ids:
        badge = badge_map.get(bid)
        if badge:
            st.session_state._pending_toasts.append({
                "type": "badge",
                "message": f"{badge['icon']} Badge: {badge['name']}",
            })

def _render_toasts():
    """Inject toast HTML + auto-dismiss JS into the page."""
    toasts = st.session_state._pending_toasts
    if not toasts:
        return
    toast_html = '<div class="toast-container" id="ab-toasts">'
    for i, t in enumerate(toasts):
        cls = f"toast {t['type']}"
        icon = "⭐" if t["type"] == "xp" else "🏅"
        toast_html += f'<div class="{cls}" id="toast-{i}">{icon} {t["message"]}</div>'
    toast_html += "</div>"
    # JS: fade each toast out after 2.5s then remove
    js = """<script>
(function(){
    var toasts = document.querySelectorAll('#ab-toasts .toast');
    toasts.forEach(function(el, i){
        setTimeout(function(){
            el.classList.add('fading');
            setTimeout(function(){ if(el.parentNode) el.parentNode.removeChild(el); }, 400);
        }, 2500 + i * 300);
    });
})();
</script>"""
    st.markdown(toast_html + js, unsafe_allow_html=True)
    st.session_state._pending_toasts = []  # clear after rendering


def _record_attempt_with_toasts(topic_key, is_correct, hints_used, difficulty, problem_type = "standard"):
    """Wrap record_problem_attempt and queue XP/badge toasts."""
    tracker = st.session_state.tracker
    badges_before = set(tracker.stats.get("earned_badges", []))
    xp_before     = tracker.stats.get("xp", 0)

    tracker.record_problem_attempt(
        topic=topic_key, is_correct=is_correct,
        hints_used=hints_used, difficulty=difficulty,
        problem_type= problem_type
    )
    tracker.save_to_file(_sf)

    xp_after     = tracker.stats.get("xp", 0)
    badges_after = set(tracker.stats.get("earned_badges", []))

    xp_gained    = xp_after - xp_before
    new_badges   = list(badges_after - badges_before)

    if xp_gained > 0:
        _queue_xp_toast(xp_gained)
    if new_badges:
        _queue_badge_toasts(new_badges)


# ── NAV ────────────────────────────────────────────────────────────────────────
_logo, _sp, _home,fc, _pr, _av = st.columns([2.5, 5.5, 0.5, 0.5, 0.5, 0.4])
with _logo:
    st.markdown('<div style="display:flex;align-items:center;gap:0.5rem;"><div style="width:28px;height:28px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.85rem;">🤖</div><span style="font-size:1rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AlgoBuddy · Practice</span></div>', unsafe_allow_html=True)
with _home:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🏠", key="nh", use_container_width=True, help="Home"): st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)
with fc:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🃏", key="nfc", use_container_width=True): 
        st.switch_page("pages/flashcards.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _pr:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("📈", key="npr", use_container_width=True, help="Progress"): st.switch_page("pages/progress.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _av:
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:center;"><div class="ab-avatar-circle">{initials}</div></div>', unsafe_allow_html=True)
st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.07);"></div>', unsafe_allow_html=True)
st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

# ── Sub-bar ────────────────────────────────────────────────────────────────────
_, sb1, sb2, sb3, _ = st.columns([1, 2, 2, 1.2, 2])
with sb1:
    course_keys   = list(COURSES.keys())
    course_labels = {cid: f"{c['icon']} {c['display_name']}" for cid, c in COURSES.items()}
    cur_ci        = course_keys.index(st.session_state.active_course) if st.session_state.active_course in course_keys else 0
    selected_course = st.selectbox("Course", course_keys, index=cur_ci, format_func=lambda k: course_labels[k])
    st.session_state.active_course = selected_course
with sb2:
    tids       = get_all_topic_ids_for_course(selected_course)
    topic_keys = [None] + tids
    def tlbl(t): return "All topics" if t is None else (get_topic(selected_course, t) or {}).get("display_name", t)
    cur_t          = st.session_state.active_topic if st.session_state.active_topic in tids else None
    selected_topic = st.selectbox("Topic", topic_keys, index=topic_keys.index(cur_t), format_func=tlbl)
    st.session_state.active_topic = selected_topic
with sb3:
    difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], index=1, format_func=str.capitalize)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Auto-generate after sub-bar ────────────────────────────────────────────────
if st.session_state.pop("_auto_generate", False):
    with st.spinner("Generating a problem based on what you just learned..."):
        try:
            _ap = generate_practice_problem(
                topic=selected_topic or selected_course, difficulty=difficulty,
                course_id=selected_course, topic_id=selected_topic,
                seed_context=_seed, file_context=_file_ctx)
        except:
            _ap = None
    if _ap and not _ap.get("error"):
        st.session_state.practice_problem = _ap
        st.session_state.practice_result  = None
        st.session_state.hints_revealed   = 0
        st.session_state.blank_answers    = {}
        st.session_state.mcq_selected     = None
        st.session_state.practice_seed    = None
        st.rerun()

# ── Banners ────────────────────────────────────────────────────────────────────
if _file_names:
    names_str = ", ".join(_file_names)
    fc1, fc2 = st.columns([6, 1])
    with fc1:
        st.markdown(f'<div class="seed-banner">📄 <strong style="color:#EEF2FF;">{names_str}</strong> — Problems based on this file.</div>', unsafe_allow_html=True)
    with fc2:
        if st.button("✕", key="rfp", use_container_width=True):
            st.session_state.uploaded_files = [f for f in st.session_state.get("uploaded_files", []) if f["type"] == "image"]
            st.rerun()
elif _seed:
    st.markdown(f'<div class="seed-banner">💡 <strong style="color:#EEF2FF;">Practising from your last chat.</strong></div>', unsafe_allow_html=True)
else:
    with st.expander("📎 Upload notes to practice from", expanded=False):
        from file_processor import process_upload as _proc
        up = st.file_uploader("PDF or Word", type=["pdf", "docx"], label_visibility="collapsed", key="prac_up")
        if up:
            existing = [f["name"] for f in st.session_state.get("uploaded_files", [])]
            if up.name not in existing:
                with st.spinner("Reading..."):
                    res = _proc(up)
                if res.get("error"):
                    st.error(res["error"])
                elif res["type"] == "text":
                    if "uploaded_files" not in st.session_state:
                        st.session_state.uploaded_files = []
                    st.session_state.uploaded_files.append({
                        "name": res["filename"], "type": "text",
                        "content": res["content"], "image_data": None
                    })
                    st.rerun()

# ── Helper ─────────────────────────────────────────────────────────────────────
def _gen():
    return generate_practice_problem(
        topic=selected_topic or selected_course, difficulty=difficulty,
        course_id=selected_course, topic_id=selected_topic,
        seed_context=_seed, file_context=_file_ctx)


def _next_problem():
    with st.spinner("Generating..."):
        try:
            pn = _gen()
        except:
            pn = None
    if pn and not pn.get("error"):
        st.session_state.practice_problem = pn
        st.session_state.practice_result  = None
        st.session_state.hints_revealed   = 0
        st.session_state.blank_answers    = {}
        st.session_state.mcq_selected     = None
        st.session_state.practice_seed    = None
    else:
        st.session_state.practice_problem = None
        st.session_state.practice_result  = None
        st.session_state.hints_revealed   = 0
        st.session_state.mcq_selected     = None
    st.rerun()

# ── Render any pending toasts BEFORE main content ──────────────────────────────
_render_toasts()

# ── Main content ───────────────────────────────────────────────────────────────
_, main_col, _ = st.columns([1, 6, 1])
with main_col:
    st.markdown("<div style='padding:2rem 0 5rem'>", unsafe_allow_html=True)
    prob  = st.session_state.practice_problem
    score = st.session_state.session_score

    if not prob:
        st.markdown('<div style="text-align:center;padding:4rem 1rem 1.5rem;"><div style="font-size:3rem;margin-bottom:1rem;">🧮</div><div style="font-size:1.05rem;color:var(--t2);font-weight:600;margin-bottom:0.4rem;">Ready to practice?</div><div style="font-size:0.88rem;color:var(--t3);">Choose a course and difficulty above, then hit  New Problem.</div></div>', unsafe_allow_html=True)
        _, bc, _ = st.columns([2, 2, 2])
        with bc:
            st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
            if st.button("⚡ New Problem", use_container_width=True, key="gen_empty"):
                with st.spinner("Generating..."):
                    try:
                        pn = _gen()
                    except Exception as e:
                        st.error(f"⚠️ {e}")
                        pn = None
                if pn and not pn.get("error"):
                    st.session_state.practice_problem = pn
                    st.session_state.practice_result  = None
                    st.session_state.hints_revealed   = 0
                    st.session_state.blank_answers    = {}
                    st.session_state.mcq_selected     = None
                    st.session_state.practice_seed    = None
                    st.rerun()
                elif pn:
                    st.error(pn.get("error", "Could not generate."))
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        # ── Top row: score + new problem ──────────────────────────────────────
        tr1, tr2, tr3 = st.columns([3, 1, 1.4])
        with tr2:
            if score["total"] > 0:
                pct = int(score["correct"] / score["total"] * 100)
                st.metric("Session", f"{pct}%", f"{score['correct']}/{score['total']}")
        with tr3:
            st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
            if st.button("⚡ New Problem", use_container_width=True, key="gen_btn"):
                with st.spinner("Generating..."):
                    try:
                        pn = _gen()
                    except Exception as e:
                        st.error(f"⚠️ {e}")
                        pn = None
                if pn and not pn.get("error"):
                    st.session_state.practice_problem = pn
                    st.session_state.practice_result  = None
                    st.session_state.hints_revealed   = 0
                    st.session_state.blank_answers    = {}
                    st.session_state.mcq_selected     = None
                    st.session_state.practice_seed    = None
                    st.rerun()
                elif pn:
                    st.error(pn.get("error", "Could not generate."))
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)

        # ── Problem card ──────────────────────────────────────────────────────
        diff  = prob.get("difficulty", "medium")
        ptype = prob.get("type", "STANDARD")

        if ptype == "FILL_BLANK":
            type_label = "Fill in the blank"
            type_cls   = "badge-fill"
        elif ptype == "MCQ":
            type_label = "Multiple choice"
            type_cls   = "badge-mcq"
        else:
            type_label = "Written / Code"
            type_cls   = "badge-standard"

        type_badge = f'<span class="prob-type-badge {type_cls}">{type_label}</span>'
        st.markdown(
            f'<div class="prob-card"><div class="prob-title">Problem '
            f'<span class="diff-pill {diff}">{diff.upper()}</span>{type_badge}</div>'
            f'<div class="prob-text">{prob.get("problem","")}</div></div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)

        # ── Hints ─────────────────────────────────────────────────────────────
        hints = prob.get("hints", [])
        for i in range(st.session_state.hints_revealed):
            if i < len(hints):
                st.markdown(f'<div class="hint-card"><div class="hint-lbl">Hint {i+1}</div><div class="hint-txt">{hints[i]}</div></div>', unsafe_allow_html=True)
                st.markdown('<div class="gap-sm"></div>', unsafe_allow_html=True)
        if hints and st.session_state.hints_revealed < len(hints) and not st.session_state.practice_result:
            hc1, hc2 = st.columns([2, 3])
            with hc1:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button(f"💡 Hint {st.session_state.hints_revealed+1}", key="hbtn", use_container_width=True):
                    st.session_state.hints_revealed += 1
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with hc2:
                if st.session_state.hints_revealed > 0:
                    st.markdown(f'<div style="padding-top:0.55rem;font-size:0.8rem;color:var(--t3);">{st.session_state.hints_revealed}/{len(hints)} hints used</div>', unsafe_allow_html=True)
            st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)

        # ══ ANSWER INPUT BY TYPE ═════════════════════════════════════════════

        # ── MCQ ───────────────────────────────────────────────────────────────
        if ptype == "MCQ" and not st.session_state.practice_result:
            options = prob.get("options", {})
            result  = st.session_state.practice_result

            st.markdown('<div style="font-size:0.85rem;color:var(--t2);margin-bottom:0.7rem;">Choose the correct answer:</div>', unsafe_allow_html=True)

            for letter, text in options.items():
                is_sel = st.session_state.mcq_selected == letter
                cls    = "mcq-option selected" if is_sel else "mcq-option"
                btn_key = f"mcq_{letter}"
                # Render styled option + invisible button on top
                col_opt, col_btn = st.columns([10, 1])
                with col_opt:
                    st.markdown(
                        f'<div class="{cls}"><div class="mcq-letter">{letter}</div>'
                        f'<div class="mcq-text">{text}</div></div>',
                        unsafe_allow_html=True
                    )
                with col_btn:
                    st.markdown(f'<div style="opacity:0;height:52px;">', unsafe_allow_html=True)
                    if st.button(letter, key=btn_key, use_container_width=True):
                        st.session_state.mcq_selected = letter
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)

            ac1, ac2, _ = st.columns([2, 1.2, 2])
            with ac1:
                st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
                if st.button("✅ Submit Answer", use_container_width=True, key="sub_mcq"):
                    if st.session_state.mcq_selected:
                        result = check_mcq_answer(
                            correct_option=prob.get("correct_option", ""),
                            student_option=st.session_state.mcq_selected,
                            explanation=prob.get("explanation", ""),
                        )
                        st.session_state.practice_result = result
                        st.session_state.session_score["total"] += 1
                        is_c = result.get("is_correct", False)
                        if is_c:
                            st.session_state.session_score["correct"] += 1
                        topic_key = selected_topic or selected_course or "general"
                        _record_attempt_with_toasts(topic_key, is_c, st.session_state.hints_revealed, difficulty, "mcq")

                        st.session_state.tracker.record_study_session()
                        st.session_state.tracker.save_to_file(_sf)
                        st.rerun()
                    else:
                        st.warning("Select an option first!")
                st.markdown('</div>', unsafe_allow_html=True)
            with ac2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("👁 Show Answer", use_container_width=True, key="show_mcq"):
                    st.session_state.practice_result = {"show_answer": True}
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ── FILL IN THE BLANK ─────────────────────────────────────────────────
        elif ptype == "FILL_BLANK" and not st.session_state.practice_result:
            blanks = prob.get("blanks", [])
            if not blanks:
                blanks = [""] * prob.get("problem", "").count("___")
            st.markdown(f'<div style="font-size:0.85rem;color:var(--t2);margin-bottom:0.6rem;">Fill in the {len(blanks)} blank{"s" if len(blanks) != 1 else ""}:</div>', unsafe_allow_html=True)
            student_blanks = [
                st.text_input(f"Blank {bi+1}", key=f"blank_{bi}", placeholder=f"Answer {bi+1}...")
                for bi in range(len(blanks))
            ]
            st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)
            ac1, ac2, _ = st.columns([2, 1.2, 2])
            with ac1:
                st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
                if st.button("✅ Check Answers", use_container_width=True, key="sub_blank"):
                    if any(a.strip() for a in student_blanks):
                        result = check_fill_blank_answer(blanks, student_blanks)
                        st.session_state.practice_result = result
                        st.session_state.session_score["total"] += 1
                        is_c = result.get("is_correct", False)
                        if is_c:
                            st.session_state.session_score["correct"] += 1
                        topic_key = selected_topic or selected_course or "general"
                        _record_attempt_with_toasts(topic_key, is_c, st.session_state.hints_revealed, difficulty,"fill_blank")
                        st.session_state.tracker.record_study_session()
                        st.session_state.tracker.save_to_file(_sf)
                        st.rerun()
                    else:
                        st.warning("Fill in at least one blank!")
                st.markdown('</div>', unsafe_allow_html=True)
            with ac2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("👁 Show Answers", use_container_width=True, key="show_blank"):
                    st.session_state.practice_result = {"show_answer": True}
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ── STANDARD ──────────────────────────────────────────────────────────
        elif ptype == "STANDARD" and not st.session_state.practice_result:
            student_answer = st.text_area(
                "Your answer", placeholder="Type your answer or code here...",
                height=140, key="ans_box"
            )
            st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)
            ac1, ac2, _ = st.columns([2, 1.2, 2])
            with ac1:
                st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
                if st.button("✅ Submit Answer", use_container_width=True, key="sub_std"):
                    if student_answer.strip():
                        with st.spinner("Checking..."):
                            result = check_student_answer(
                                problem=prob.get("problem", ""),
                                student_answer=student_answer,
                                correct_answer=prob.get("answer", ""),
                                course_id=selected_course,
                            )
                        st.session_state.practice_result = result
                        st.session_state.session_score["total"] += 1
                        is_c = result.get("is_correct", False)
                        if is_c:
                            st.session_state.session_score["correct"] += 1
                        topic_key = selected_topic or selected_course or "general"
                        _record_attempt_with_toasts(topic_key, is_c, st.session_state.hints_revealed, difficulty,"standard")

                        st.session_state.tracker.record_study_session()
                        st.session_state.tracker.save_to_file(_sf)
                        st.rerun()
                    else:
                        st.warning("Write your answer first!")
                st.markdown('</div>', unsafe_allow_html=True)
            with ac2:
                st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                if st.button("👁 Show Answer", use_container_width=True, key="show_std"):
                    st.session_state.practice_result = {"show_answer": True}
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ══ RESULT ═══════════════════════════════════════════════════════════
        if st.session_state.practice_result:
            st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)
            result = st.session_state.practice_result

            if result.get("show_answer"):
                # Show model answer
                if ptype == "FILL_BLANK":
                    blanks = prob.get("blanks", [])
                    ans_str = " &nbsp;|&nbsp; ".join(f"Blank {i+1}: <strong>{b}</strong>" for i, b in enumerate(blanks))
                    st.markdown(
                        f'<div class="hint-card"><div class="hint-lbl">Answers</div>'
                        f'<div class="hint-txt">{ans_str}</div>'
                        f'<div style="font-size:0.88rem;color:var(--t2);margin-top:0.5rem;line-height:1.6;">{prob.get("explanation","")}</div></div>',
                        unsafe_allow_html=True
                    )
                elif ptype == "MCQ":
                    correct_opt = prob.get("correct_option", "")
                    correct_txt = prob.get("options", {}).get(correct_opt, "")
                    st.markdown(
                        f'<div class="hint-card"><div class="hint-lbl">Correct Answer</div>'
                        f'<div class="hint-txt"><strong>{correct_opt}.</strong> {correct_txt}</div>'
                        f'<div style="font-size:0.88rem;color:var(--t2);margin-top:0.5rem;line-height:1.6;">{prob.get("explanation","")}</div></div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="hint-card"><div class="hint-lbl">Model Answer</div>'
                        f'<div style="font-family:var(--mono);background:rgba(0,0,0,0.3);padding:0.8rem;border-radius:8px;font-size:0.85em;color:#C4D4FF;margin:0.4rem 0;">{prob.get("answer","")}</div>'
                        f'<div style="font-size:0.88rem;color:var(--t2);margin-top:0.5rem;line-height:1.6;">{prob.get("explanation","")}</div></div>',
                        unsafe_allow_html=True
                    )

            elif result.get("is_correct"):
                hint_free  = st.session_state.hints_revealed == 0
                xp_display = result.get("score", "")
                bonus      = '<span style="color:#F59E0B;margin-left:0.4rem;">Hint-free! 🌟</span>' if hint_free else ""
                st.markdown(
                    f'<div class="res-ok"><div class="res-lbl" style="color:#10B981;">✅ Correct! {bonus}</div>'
                    f'<div class="res-txt">{result.get("feedback","")}</div></div>',
                    unsafe_allow_html=True
                )
                st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)
                _, nb, _ = st.columns([2, 2, 2])
                with nb:
                    st.markdown('<div class="next-btn">', unsafe_allow_html=True)
                    if st.button("Next Problem →", use_container_width=True, key="nxt"):
                        _next_problem()
                    st.markdown('</div>', unsafe_allow_html=True)

            else:
                score_part = f' — {result.get("score","")}' if result.get("score") else ""
                tip = f'<div style="font-size:0.86rem;color:var(--t2);margin-top:0.5rem;line-height:1.6;">💡 {result.get("next_step","")}</div>' if result.get("next_step") else ""
                st.markdown(
                    f'<div class="res-no"><div class="res-lbl" style="color:#EF4444;">❌ Not quite{score_part}</div>'
                    f'<div class="res-txt">{result.get("feedback","")}</div>{tip}</div>',
                    unsafe_allow_html=True
                )
                # Show "Try Again" and "Next Problem" on wrong answer
                st.markdown('<div class="gap-md"></div>', unsafe_allow_html=True)
                ta1, ta2, _ = st.columns([1.5, 1.5, 3])
                with ta1:
                    st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
                    if st.button("🔄 Try Again", use_container_width=True, key="retry"):
                        st.session_state.practice_result = None
                        st.session_state.mcq_selected    = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with ta2:
                    st.markdown('<div class="next-btn">', unsafe_allow_html=True)
                    if st.button("Next →", use_container_width=True, key="nxt_wrong"):
                        _next_problem()
                    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)