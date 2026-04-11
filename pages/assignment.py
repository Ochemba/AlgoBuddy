# pages/assignment.py — Assignment Help Mode
"""
Step-by-step guided assignment help.
Paste your assignment → get a breakdown → chat through each step with the AI.
The AI NEVER gives the answer — it guides you to figure it out yourself.
"""

import streamlit as st
import time

st.set_page_config(
    page_title="AlgoBuddy — Assignment Help",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from assignment_helper import AssignmentHelper
from auth import AuthManager

_auth = AuthManager()

# ── Shared CSS (mirrors app.py theme) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
    --navy:#060B2B;--n2:#0D1547;--n3:#1B2B6B;
    --teal:#06B6D4;--tg:rgba(6,182,212,0.15);--tb:rgba(6,182,212,0.3);
    --g1:rgba(255,255,255,0.05);--g2:rgba(255,255,255,0.09);
    --t1:#EEF2FF;--t2:#A8B4D8;--t3:#5A6A9A;
    --font:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;
}
html,body,[class*="css"]{font-family:var(--font)!important;color:var(--t1)!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stAppViewContainer"]{
    background:linear-gradient(160deg,#060B2B 0%,#0D1547 55%,#182060 100%)!important;
    min-height:100vh;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active {
    background:#0f1d5e!important;background-color:#0f1d5e!important;
    color:#EEF2FF!important;-webkit-text-fill-color:#EEF2FF!important;
    border:1px solid rgba(255,255,255,0.15)!important;border-radius:10px!important;
    font-family:var(--font)!important;caret-color:#06B6D4!important;
}
[data-testid="stTextInput"] input:focus{border-color:#06B6D4!important;box-shadow:0 0 0 3px rgba(6,182,212,0.15)!important;}
[data-testid="stTextInput"] input::placeholder{color:rgba(168,180,216,0.5)!important;-webkit-text-fill-color:rgba(168,180,216,0.5)!important;}
[data-testid="stTextInput"] [data-baseweb="base-input"],[data-testid="stTextInput"] div[style]{background:#0f1d5e!important;background-color:#0f1d5e!important;}
[data-testid="stTextInput"] label{color:#A8B4D8!important;font-size:0.82rem!important;}

/* ── Text area ── */
[data-testid="stTextArea"] textarea,
[data-testid="stTextArea"] textarea:focus {
    background:#0f1d5e!important;background-color:#0f1d5e!important;
    color:#EEF2FF!important;-webkit-text-fill-color:#EEF2FF!important;
    border:1px solid rgba(255,255,255,0.15)!important;border-radius:10px!important;
    font-family:var(--font)!important;font-size:0.9rem!important;
    caret-color:#06B6D4!important;line-height:1.6!important;
}
[data-testid="stTextArea"] textarea:focus{border-color:#06B6D4!important;box-shadow:0 0 0 3px rgba(6,182,212,0.15)!important;}
[data-testid="stTextArea"] textarea::placeholder{color:rgba(168,180,216,0.4)!important;-webkit-text-fill-color:rgba(168,180,216,0.4)!important;}
[data-testid="stTextArea"] [data-baseweb="base-input"],[data-testid="stTextArea"] div[style]{background:#0f1d5e!important;background-color:#0f1d5e!important;}
[data-testid="stTextArea"] label{color:#A8B4D8!important;font-size:0.82rem!important;}

/* ── Nav bar ── */
.ab-nav{
    background:rgba(6,11,43,0.95);backdrop-filter:blur(18px);
    border-bottom:1px solid rgba(255,255,255,0.07);
    padding:0.6rem 2rem;display:flex;align-items:center;gap:0.7rem;
    position:sticky;top:0;z-index:500;
}
.ab-nav-logo{display:flex;align-items:center;gap:0.5rem;text-decoration:none;}
.ab-nav-icon{width:26px;height:26px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;}
.ab-nav-title{font-size:0.97rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.ab-nav-sep{color:rgba(255,255,255,0.2);font-size:0.9rem;}
.ab-nav-page{font-size:0.82rem;font-weight:600;color:var(--teal);}
.ab-pill-btn .stButton>button{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:20px!important;font-family:var(--font)!important;font-size:0.78rem!important;font-weight:600!important;color:var(--teal)!important;padding:0.25rem 0.85rem!important;box-shadow:none!important;min-height:0!important;height:28px!important;white-space:nowrap!important;}
.ab-pill-btn .stButton>button:hover{background:rgba(6,182,212,0.15)!important;border-color:var(--teal)!important;transform:none!important;}
.ab-pill-btn{display:inline-flex;align-items:center;}

/* ── Page layout ── */
.assign-wrap{max-width:860px;margin:0 auto;padding:2rem 4% 4rem;}

/* ── Step card ── */
.step-card{
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem;
    transition:border-color 0.2s,background 0.2s;
}
.step-card.active{background:rgba(6,182,212,0.08);border-color:rgba(6,182,212,0.35);}
.step-card.done{background:rgba(16,185,129,0.07);border-color:rgba(16,185,129,0.3);}
.step-num{font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t3);margin-bottom:0.25rem;}
.step-num.active{color:var(--teal);}
.step-num.done{color:#34d399;}
.step-desc{font-size:0.9rem;color:#EEF2FF;font-weight:500;}
.step-hint{font-size:0.8rem;color:var(--t2);margin-top:0.3rem;font-style:italic;}

/* ── Concept badge ── */
.concept-badge{display:inline-block;font-size:0.72rem;font-weight:600;color:var(--teal);background:var(--tg);border:1px solid var(--tb);border-radius:20px;padding:0.2rem 0.65rem;margin:0.2rem 0.2rem 0 0;}

/* ── Difficulty pill ── */
.diff-easy{color:#34d399;background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);}
.diff-medium{color:#fbbf24;background:rgba(251,191,36,0.1);border:1px solid rgba(251,191,36,0.3);}
.diff-hard{color:#f87171;background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.3);}
.diff-pill{display:inline-block;font-size:0.72rem;font-weight:700;letter-spacing:0.05em;text-transform:uppercase;border-radius:20px;padding:0.2rem 0.7rem;}

/* ── Chat messages ── */
.ab-row-b{display:flex;align-items:flex-start;gap:0.6rem;margin-bottom:0.9rem;}
.ab-row-u{display:flex;justify-content:flex-end;align-items:flex-end;gap:0.6rem;margin-bottom:0.9rem;}
.ab-bu{background:#1B2B6B;border:1px solid rgba(255,255,255,0.12);color:#EEF2FF;padding:0.7rem 1rem;border-radius:18px 18px 4px 18px;max-width:70%;font-size:0.9rem;line-height:1.6;overflow-wrap:break-word;word-break:break-word;}
.ab-bb{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:#EEF2FF;padding:0.85rem 1.1rem;border-radius:4px 18px 18px 18px;max-width:calc(100% - 44px);font-size:0.9rem;line-height:1.7;overflow-wrap:break-word;word-break:break-word;}
.ab-bb code{font-family:var(--mono);background:rgba(6,182,212,0.15);color:#67E8F9;padding:0.1em 0.4em;border-radius:4px;font-size:0.85em;}
.ab-bb pre{background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.08);color:#C4D4FF;border-radius:10px;padding:0.9rem;overflow-x:auto;font-family:var(--mono);font-size:0.82em;line-height:1.5;margin:0.5rem 0;}
.ab-av{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#1B2B6B,#06B6D4);display:flex;align-items:center;justify-content:center;font-size:0.82rem;flex-shrink:0;}
.ab-uav{width:28px;height:28px;border-radius:50%;background:#243580;border:1px solid rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:0.73rem;color:#fff;font-weight:700;flex-shrink:0;}
.ab-ts{font-size:0.64rem;color:var(--t3);margin-top:0.2rem;padding:0 0.25rem;}

/* ── Summary card ── */
.summary-card{background:rgba(6,182,212,0.06);border:1px solid rgba(6,182,212,0.25);border-radius:14px;padding:1.5rem 1.6rem;margin-top:1rem;}
.summary-title{font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:1rem;}
.summary-row{display:flex;gap:0.5rem;margin-bottom:0.5rem;font-size:0.88rem;}
.summary-label{color:var(--t3);min-width:120px;}
.summary-value{color:#EEF2FF;font-weight:500;}

/* ── Primary + ghost buttons ── */
.btn-primary .stButton>button{background:linear-gradient(135deg,#1B2B6B,#06B6D4)!important;color:#fff!important;-webkit-text-fill-color:#fff!important;border:none!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;height:44px!important;box-shadow:0 4px 18px rgba(6,182,212,0.3)!important;width:100%!important;}
.btn-primary .stButton>button:hover{background:linear-gradient(135deg,#243580,#22D3EE)!important;transform:none!important;}
.btn-ghost .stButton>button{background:rgba(255,255,255,0.05)!important;color:var(--teal)!important;-webkit-text-fill-color:var(--teal)!important;border:1px solid rgba(6,182,212,0.35)!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:600!important;font-size:0.88rem!important;height:40px!important;box-shadow:none!important;width:100%!important;}
.btn-ghost .stButton>button:hover{background:rgba(6,182,212,0.12)!important;transform:none!important;}
.btn-success .stButton>button{background:rgba(52,211,153,0.12)!important;color:#34d399!important;-webkit-text-fill-color:#34d399!important;border:1px solid rgba(52,211,153,0.35)!important;border-radius:10px!important;font-family:var(--font)!important;font-weight:600!important;font-size:0.88rem!important;height:40px!important;box-shadow:none!important;width:100%!important;}
.btn-success .stButton>button:hover{background:rgba(52,211,153,0.2)!important;transform:none!important;}

.ab-thinking{display:inline-flex;align-items:center;gap:0.5rem;background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:0.38rem 0.95rem;font-size:0.81rem;color:var(--t2);}
.dot{width:5px;height:5px;border-radius:50%;background:var(--teal);display:inline-block;animation:pu 1.2s infinite;}
.dot:nth-child(2){animation-delay:.2s;}.dot:nth-child(3){animation-delay:.4s;}
@keyframes pu{0%,80%,100%{opacity:.3;transform:scale(.8);}40%{opacity:1;transform:scale(1);}}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:var(--teal);}
</style>
""", unsafe_allow_html=True)

# ── State defaults ─────────────────────────────────────────────────────────────
for k, v in {
    "logged_in": False, "username": None, "student_name": "Student",
    "assign_helper": None,        # AssignmentHelper instance
    "assign_breakdown": None,     # breakdown dict from analyze_assignment()
    "assign_messages": [],        # chat history for this assignment
    "assign_thinking": False,
    "assign_done": False,
    "assign_cin_key": 0,
    "assign_text_submitted": "",  # the assignment text that was submitted
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Redirect to login if not authenticated
if not st.session_state.logged_in:
    st.switch_page("app.py")

# ── Nav bar ────────────────────────────────────────────────────────────────────
nav_logo, _, nav_home, nav_new = st.columns([3, 5, 0.9, 1.1])
with nav_logo:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.5rem;padding:0.55rem 0;">
        <div style="width:26px;height:26px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;flex-shrink:0;">🤖</div>
        <span style="font-size:0.97rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AlgoBuddy</span>
        <span style="color:rgba(255,255,255,0.2);margin:0 0.2rem;">›</span>
        <span style="font-size:0.82rem;font-weight:600;color:var(--teal);">Assignment Help</span>
    </div>""", unsafe_allow_html=True)

with nav_home:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

with nav_new:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("✦ New Assignment", key="nav_new_assign", use_container_width=True):
        st.session_state.assign_helper         = None
        st.session_state.assign_breakdown      = None
        st.session_state.assign_messages       = []
        st.session_state.assign_done           = False
        st.session_state.assign_text_submitted = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border-bottom:1px solid rgba(255,255,255,0.07);margin-bottom:0;"></div>', unsafe_allow_html=True)

# ══ PHASE 1 — Paste Assignment ══════════════════════════════════════════════════
if st.session_state.assign_breakdown is None:

    _, col, _ = st.columns([1, 6, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem 0 1.5rem;">
            <div style="font-size:2rem;margin-bottom:0.6rem;">📝</div>
            <div style="font-size:1.4rem;font-weight:800;color:#fff;margin-bottom:0.4rem;">Assignment Help Mode</div>
            <div style="font-size:0.92rem;color:#A8B4D8;">
                Paste your assignment below. AlgoBuddy will break it into steps<br>
                and guide you through each one — <em>without</em> giving away the answer.
            </div>
        </div>""", unsafe_allow_html=True)

        assignment_text = st.text_area(
            "Your assignment",
            placeholder="Paste your full assignment question here...\n\nExample: Write a Python function called 'find_max' that takes a list of numbers as input and returns the largest number. Handle the case where the list is empty by returning None.",
            height=220,
            label_visibility="collapsed",
            key="assign_input"
        )

        st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        analyse_clicked = st.button("Analyse My Assignment →", key="btn_analyse", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if analyse_clicked:
            if not assignment_text.strip():
                st.error("Please paste your assignment text first.")
            elif len(assignment_text.strip()) < 20:
                st.error("That looks too short — please paste the full assignment question.")
            else:
                with st.spinner("Breaking down your assignment..."):
                    helper = AssignmentHelper(st.session_state.student_name)
                    breakdown = helper.analyze_assignment(assignment_text.strip())

                if breakdown is None:
                    st.error("Could not analyse the assignment. Please check your API key and try again.")
                else:
                    st.session_state.assign_helper         = helper
                    st.session_state.assign_breakdown      = breakdown
                    st.session_state.assign_text_submitted = assignment_text.strip()
                    st.session_state.assign_messages       = []
                    st.session_state.assign_done           = False

                    # Get opening message from the AI
                    opening = helper.get_guidance("I'm ready to start working on this assignment!")
                    st.session_state.assign_messages.append({
                        "role": "assistant", "content": opening, "time": time.strftime("%H:%M")
                    })
                    st.rerun()

# ══ PHASE 2 — Step-by-step guidance ════════════════════════════════════════════
else:
    helper    = st.session_state.assign_helper
    breakdown = st.session_state.assign_breakdown
    total     = len(breakdown["steps"])
    done_count = len(helper.steps_completed)

    # Two-column layout: steps sidebar on left, chat on right
    left, right = st.columns([1.6, 3.4], gap="large")

    # ── Left: breakdown overview ──────────────────────────────────────────────
    with left:
        st.markdown('<div style="padding:1.5rem 0 0 0.5rem;">', unsafe_allow_html=True)

        # Assignment snippet
        text_preview = st.session_state.assign_text_submitted[:120]
        if len(st.session_state.assign_text_submitted) > 120:
            text_preview += "…"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.85rem 1rem;margin-bottom:1.2rem;">
            <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t3);margin-bottom:0.4rem;">Assignment</div>
            <div style="font-size:0.82rem;color:#A8B4D8;line-height:1.5;">{text_preview}</div>
        </div>""", unsafe_allow_html=True)

        # Difficulty + concepts
        diff = breakdown.get("difficulty_estimate", "medium").lower()
        diff_class = f"diff-{diff}" if diff in ("easy", "medium", "hard") else "diff-medium"
        concepts = breakdown.get("concepts_required", [])
        concepts_html = "".join(f'<span class="concept-badge">{c}</span>' for c in concepts)
        st.markdown(f"""
        <div style="margin-bottom:1.2rem;">
            <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t3);margin-bottom:0.5rem;">Difficulty</div>
            <span class="diff-pill {diff_class}">{diff.upper()}</span>
            <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t3);margin:0.8rem 0 0.4rem;">Concepts</div>
            <div>{concepts_html}</div>
        </div>""", unsafe_allow_html=True)

        # Progress bar
        progress_pct = int((done_count / total) * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="margin-bottom:1.2rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:0.35rem;">
                <span style="font-size:0.72rem;color:var(--t3);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Progress</span>
                <span style="font-size:0.72rem;color:var(--teal);font-weight:700;">{done_count}/{total} steps</span>
            </div>
            <div style="background:rgba(255,255,255,0.06);border-radius:20px;height:6px;overflow:hidden;">
                <div style="background:linear-gradient(90deg,#1B2B6B,#06B6D4);height:100%;width:{progress_pct}%;border-radius:20px;transition:width 0.4s;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Step list
        st.markdown('<div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--t3);margin-bottom:0.6rem;">Steps</div>', unsafe_allow_html=True)
        for step in breakdown["steps"]:
            n = step["step_number"]
            is_done   = n in helper.steps_completed
            is_active = (n == helper.current_step + 1) and not is_done
            card_cls  = "step-card done" if is_done else ("step-card active" if is_active else "step-card")
            num_cls   = "step-num done"  if is_done else ("step-num active"  if is_active else "step-num")
            icon      = "✓" if is_done else ("→" if is_active else str(n))
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="{num_cls}">Step {icon}</div>
                <div class="step-desc">{step['description']}</div>
                {'<div class="step-hint">' + step.get("hint","") + '</div>' if is_active and step.get("hint") else ""}
            </div>""", unsafe_allow_html=True)

        # Mark step done + show summary buttons
        st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)

        if not helper.is_assignment_complete():
            current_step_n = helper.current_step + 1
            if current_step_n <= total:
                st.markdown('<div class="btn-success">', unsafe_allow_html=True)
                if st.button(f"✓ Mark Step {current_step_n} Done", key="btn_step_done", use_container_width=True):
                    helper.mark_step_complete(current_step_n)
                    # Tell the AI the step was completed
                    ai_msg = helper.get_guidance(f"I've completed step {current_step_n}!")
                    st.session_state.assign_messages.append({
                        "role": "assistant", "content": ai_msg, "time": time.strftime("%H:%M")
                    })
                    if helper.is_assignment_complete():
                        st.session_state.assign_done = True
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:0.8rem;background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.3);border-radius:10px;margin-bottom:0.6rem;">
                <div style="font-size:1.2rem">🎉</div>
                <div style="font-size:0.88rem;font-weight:700;color:#34d399;margin-top:0.2rem;">All steps complete!</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Right: chat ────────────────────────────────────────────────────────────
    with right:
        st.markdown('<div style="padding:1.5rem 0.5rem 6rem 0;">', unsafe_allow_html=True)

        # ── Summary (shown when complete) ──
        if st.session_state.assign_done:
            summary = helper.generate_summary()
            objectives_html = "".join(f"<li style='color:#A8B4D8;margin-bottom:0.2rem;'>{o}</li>" for o in summary.get("learning_objectives", []))
            next_html = "".join(f"<li style='color:#A8B4D8;margin-bottom:0.2rem;'>{s}</li>" for s in summary.get("next_steps", []))
            st.markdown(f"""
            <div class="summary-card">
                <div class="summary-title">🏆 Assignment Complete!</div>
                <div class="summary-row"><span class="summary-label">Status</span><span class="summary-value" style="color:#34d399;">{summary['status']}</span></div>
                <div class="summary-row"><span class="summary-label">Difficulty</span><span class="summary-value">{summary['difficulty'].upper()}</span></div>
                <div class="summary-row"><span class="summary-label">Steps</span><span class="summary-value">{summary['steps_completed']}/{summary['total_steps']} completed</span></div>
                <div style="margin-top:0.8rem;">
                    <div style="font-size:0.75rem;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">What you learned</div>
                    <ul style="margin:0;padding-left:1.2rem;">{objectives_html}</ul>
                </div>
                {"<div style='margin-top:0.8rem;'><div style='font-size:0.75rem;font-weight:700;color:var(--t3);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;'>Practice next</div><ul style='margin:0;padding-left:1.2rem;'>" + next_html + "</ul></div>" if summary.get("next_steps") else ""}
            </div>""", unsafe_allow_html=True)
            st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

        # ── Chat messages ──
        sn_init = (st.session_state.student_name[0] if st.session_state.student_name else "S").upper()
        for msg in st.session_state.assign_messages:
            ts = msg.get("time", "")
            c  = msg["content"]
            if msg["role"] == "user":
                st.markdown(f'<div class="ab-row-u"><div class="ab-bu">{c}</div><div class="ab-uav">{sn_init}</div></div><div style="text-align:right;margin-bottom:0.3rem;margin-top:-0.5rem;padding-right:2.2rem;"><span class="ab-ts">{ts}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ab-row-b"><div class="ab-av">📝</div><div><div class="ab-bb">{c}</div><div class="ab-ts">{ts}</div></div></div>', unsafe_allow_html=True)

        # Thinking indicator
        if st.session_state.assign_thinking:
            st.markdown('<div style="display:flex;margin:0.3rem 0;"><div class="ab-thinking"><span class="dot"></span><span class="dot"></span><span class="dot"></span>&nbsp;AlgoBuddy is thinking...</div></div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Sticky input bar ──
        st.markdown("""
        <style>
        /* Make the input row fixed to bottom on assignment page */
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]){
            position:fixed!important;bottom:0!important;left:0!important;right:0!important;
            z-index:400!important;background:linear-gradient(to top,rgba(6,11,43,0.85) 0%,transparent 70%)!important;
            padding:1rem 0 0.7rem!important;
        }
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stColumn"]{display:flex!important;align-items:center!important;padding-top:0!important;padding-bottom:0!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) .element-container,
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-testid="stVerticalBlock"]{margin-top:0!important;margin-bottom:0!important;padding:0!important;width:100%!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-baseweb="textarea"],
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) [data-baseweb="base-input"],
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) div[style]{background:#1c2f6e!important;background-color:#1c2f6e!important;border:1.5px solid rgba(6,182,212,0.4)!important;border-radius:14px!important;box-shadow:none!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea,
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea:focus{background:#1c2f6e!important;background-color:#1c2f6e!important;color:#EEF2FF!important;-webkit-text-fill-color:#EEF2FF!important;caret-color:#06B6D4!important;border:none!important;outline:none!important;box-shadow:none!important;border-radius:14px!important;font-family:var(--font)!important;font-size:0.9rem!important;padding:0.75rem 1.1rem!important;resize:vertical!important;line-height:1.55!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) textarea::placeholder{color:rgba(168,180,216,0.5)!important;-webkit-text-fill-color:rgba(168,180,216,0.5)!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) label{display:none!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button{background:linear-gradient(135deg,#1B2B6B,#06B6D4)!important;color:#fff!important;border:none!important;border-radius:14px!important;font-family:var(--font)!important;font-weight:700!important;font-size:0.9rem!important;height:52px!important;white-space:nowrap!important;width:100%!important;box-shadow:0 0 18px rgba(6,182,212,0.3)!important;}
        [data-testid="stMain"] [data-testid="stHorizontalBlock"]:has([data-testid="stTextArea"]) button:hover{background:linear-gradient(135deg,#243580,#22D3EE)!important;transform:none!important;}
        </style>
        """, unsafe_allow_html=True)

        _gl, ic, sc, _gr = st.columns([1.5, 7.5, 1.2, 0.8])
        with ic:
            user_msg = st.text_area(
                "chat", placeholder="Ask for a hint, share your attempt, or ask a question...",
                label_visibility="collapsed",
                key=f"_acin_{st.session_state.assign_cin_key}",
                height=72
            )
        with sc:
            send = st.button("Send →", key="_asend", use_container_width=True)

        if send and user_msg.strip():
            st.session_state.assign_messages.append({
                "role": "user", "content": user_msg.strip(), "time": time.strftime("%H:%M")
            })
            st.session_state.assign_thinking = True
            st.session_state.assign_cin_key += 1
            st.rerun()

# ── AI response ────────────────────────────────────────────────────────────────
if st.session_state.assign_thinking and st.session_state.assign_helper:
    last_user = next(
        (m["content"] for m in reversed(st.session_state.assign_messages) if m["role"] == "user"),
        ""
    )
    try:
        reply = st.session_state.assign_helper.get_guidance(last_user)
    except Exception as e:
        reply = f"⚠️ Error getting guidance: {e}"

    st.session_state.assign_messages.append({
        "role": "assistant", "content": reply, "time": time.strftime("%H:%M")
    })
    st.session_state.assign_thinking = False
    st.rerun()