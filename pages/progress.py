import streamlit as st
st.set_page_config(page_title="Progress · AlgoBuddy", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

from supabase_client import retry_on_error

from datetime import date, datetime, timedelta
from progress_tracker import ProgressTracker, LEVELS, BADGES
from course_registry import COURSES
try:
    from progress_tracker import BADGES_TIER2
except ImportError:
    BADGES_TIER2 = []

# ============================================
# SESSION STATE INITIALIZATION - MUST BE FIRST
# ============================================
# Initialize ALL session state variables before using them
if "progress_loaded" not in st.session_state:
    st.session_state.progress_loaded = False
if "cached_progress_stats" not in st.session_state:
    st.session_state.cached_progress_stats = None
if "cached_progress_tracker" not in st.session_state:
    st.session_state.cached_progress_tracker = None
if "progress_username" not in st.session_state:
    st.session_state.progress_username = None
if "progress_last_load" not in st.session_state:
    st.session_state.progress_last_load = None
if "progress_needs_refresh" not in st.session_state:
    st.session_state.progress_needs_refresh = False

# ============================================
# FUNCTION TO LOAD PROGRESS DATA (CACHED)
# ============================================
def load_progress_data(username, force_refresh=False):
    """Load progress data - only reads file when needed"""
    
    # If force refresh, clear cache
    if force_refresh:
        st.session_state.progress_loaded = False
        st.session_state.cached_progress_stats = None
        st.session_state.cached_progress_tracker = None
        st.session_state.progress_needs_refresh = False
    
    # If already loaded and username matches, return cached
    if (st.session_state.progress_loaded and 
        st.session_state.progress_username == username and
        not st.session_state.progress_needs_refresh):
        return st.session_state.cached_progress_tracker
    
    # Otherwise, load from file
    tracker = ProgressTracker(username)
    tracker.load_from_file(f"{username}_progress.json")
    
    # Store in session state
    st.session_state.cached_progress_tracker = tracker
    st.session_state.cached_progress_stats = tracker.stats.copy()
    st.session_state.progress_username = username
    st.session_state.progress_loaded = True
    st.session_state.progress_needs_refresh = False
    st.session_state.progress_last_load = datetime.now()
    
    return tracker

# ============================================
# GET CURRENT USER
# ============================================
username = st.session_state.get("username", "user")
sname = st.session_state.get("student_name", "Student")
initials = (sname[0] if sname else "S").upper()

# Load tracker (cached)
tracker = load_progress_data(username)

# ============================================
# CSS STYLES (your existing CSS - keeping exactly as is)
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{--teal:#06B6D4;--tg:rgba(6,182,212,0.15);--tb:rgba(6,182,212,0.3);--g1:rgba(255,255,255,0.05);--g2:rgba(255,255,255,0.09);--t1:#EEF2FF;--t2:#A8B4D8;--t3:#5A6A9A;--ok:#10B981;--warn:#F59E0B;--err:#EF4444;--font:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;}
html,body,[class*="css"]{font-family:var(--font)!important;color:var(--t1)!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#060B2B 0%,#0D1547 55%,#182060 100%)!important;min-height:100vh;}
/* Nav */
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type {
    background: rgba(6,11,43,0.95)!important;
    backdrop-filter: blur(18px)!important;
    border-bottom: 1px solid rgba(255,255,255,0.07)!important;
    padding: 0.55rem 1rem!important;
    position: sticky!important;
    top: 0!important;
    z-index: 500!important;
    width: 100vw !important;
    overflow-x: hidden !important;
}
[data-testid="stColumn"] {
    flex: 1 1 auto !important;
    min-width: 0 !important; 
}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]{display:flex!important;align-items:center!important;padding-top:0!important;padding-bottom:0!important;gap:0!important;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"] .element-container,[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] .element-container{margin:0!important;width:100%;}
.ab-pill-btn .stButton>button,.ab-pill-btn .stButton>button:focus{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:20px!important;font-family:var(--font)!important;font-size:0.78rem!important;font-weight:600!important;color:var(--teal)!important;padding:0.25rem 0.85rem!important;box-shadow:none!important;min-height:0!important;height:28px!important;white-space:nowrap!important;}
.ab-pill-btn .stButton>button:hover{background:rgba(6,182,212,0.15)!important;border-color:var(--teal)!important;transform:none!important;}
.ab-avatar-circle{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border:2px solid rgba(6,182,212,0.45);display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:#fff;}
.ab-subpage-nav{display:flex!important;align-items:center!important;justify-content:space-between!important;background:rgba(6,11,43,0.95);backdrop-filter:blur(18px);border-bottom:1px solid rgba(255,255,255,0.07);padding:0.55rem 1.5rem;position:sticky;top:0;z-index:500;width:100%;box-sizing:border-box;gap:0.8rem;}
.ab-subpage-logo{display:flex;align-items:center;gap:0.5rem;min-width:0;flex:1;}
.ab-nav-icon{display:inline-flex;align-items:center;justify-content:center;width:30px;height:28px;border-radius:20px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12);text-decoration:none;font-size:0.88rem;color:var(--teal);flex-shrink:0;transition:background 0.15s;}
.ab-nav-icon:hover{background:rgba(6,182,212,0.15);border-color:var(--teal);}
.ab-card{background:var(--g1);border:1px solid rgba(255,255,255,0.09);border-radius:14px;padding:1.5rem 1.6rem;margin-bottom:1.2rem;}
.ab-card-title{font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:var(--teal);margin-bottom:1.1rem;}
.stat-card{background:var(--g1);border:1px solid rgba(255,255,255,0.09);border-radius:14px;padding:1.1rem 1.3rem;}
.stat-val{font-size:1.9rem;font-weight:800;font-family:var(--mono);color:#4DB8FF;line-height:1.1;}
.stat-lbl{font-size:0.72rem;color:var(--t3);margin-top:0.2rem;}
.stat-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:0.7rem;margin-bottom:1.4rem;}
.level-card{background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(27,43,107,0.4));border:1px solid rgba(6,182,212,0.3);border-radius:16px;padding:1.6rem 1.8rem;margin-bottom:1.2rem;}
.level-icon{font-size:2.4rem;margin-bottom:0.4rem;}
.level-name{font-size:1.2rem;font-weight:800;color:#fff;letter-spacing:-0.02em;}
.level-xp{font-size:0.82rem;color:var(--t2);margin-top:0.2rem;}
.xp-bar-bg{background:rgba(255,255,255,0.07);border-radius:20px;height:8px;overflow:hidden;margin:0.7rem 0 0.3rem;}
.xp-bar-fill{height:8px;border-radius:20px;background:linear-gradient(90deg,#1B2B6B,#06B6D4);transition:width 0.6s ease;}
.level-track{display:flex;justify-content:space-between;gap:0.3rem;margin-top:0.8rem;}
.level-pip{flex:1;height:4px;border-radius:2px;background:rgba(255,255,255,0.07);}
.level-pip.done{background:var(--teal);}
.badge-grid{display:flex;flex-wrap:wrap;gap:0.5rem;}
.badge-item{display:inline-flex;flex-direction:column;align-items:center;background:var(--g1);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:0.9rem 1rem;min-width:90px;text-align:center;opacity:0.35;transition:opacity 0.2s;position:relative;cursor:default;}
.badge-item.earned{opacity:1;border-color:var(--teal);background:var(--tg);}
.badge-ico{font-size:1.6rem;margin-bottom:0.3rem;}
.badge-name{font-size:0.67rem;font-weight:700;color:var(--t2);line-height:1.3;}
.badge-item.earned .badge-name{color:var(--teal);}
.badge-desc{font-size:0.62rem;color:var(--t3);margin-top:0.15rem;line-height:1.3;}
.badge-item::after{content:attr(data-tip);position:absolute;bottom:calc(100% + 8px);left:50%;transform:translateX(-50%);background:#0D1547;color:#A8B4D8;font-size:0.72rem;line-height:1.5;font-family:var(--font);border:1px solid rgba(6,182,212,0.3);border-radius:8px;padding:0.45rem 0.8rem;white-space:normal;max-width:180px;text-align:center;pointer-events:none;opacity:0;transition:opacity 0.15s;z-index:999;box-shadow:0 4px 16px rgba(0,0,0,0.4);}
.badge-item:hover::after{opacity:1;}
.ab-topic-row{display:flex;align-items:center;gap:0.8rem;padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.05);}
.ab-topic-row:last-child{border-bottom:none;}
.ab-topic-name{font-size:0.87rem;color:var(--t2);min-width:120px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.ab-bar-bg{flex:1;background:rgba(255,255,255,0.07);border-radius:20px;height:7px;overflow:hidden;}
.ab-bar-fill{height:7px;border-radius:20px;}
.ab-topic-acc{font-size:0.82rem;font-family:var(--mono);color:#4DB8FF;min-width:44px;text-align:right;}
.xp-row{display:flex;justify-content:space-between;align-items:center;padding:0.35rem 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.82rem;}
.xp-row:last-child{border-bottom:none;}
.xp-amount{color:#4DB8FF;font-family:var(--mono);font-weight:700;}
.xp-reason{color:var(--t2);}
.xp-date{color:var(--t3);font-size:0.72rem;}
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:2px;}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"]{
    flex-wrap:nowrap!important;
}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]{
    flex:0 0 auto!important;min-width:0!important;width:auto!important;
}
section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:first-child,
[data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child{
    flex:1 1 auto!important;
}
@media (max-width:768px){
    .stat-grid{grid-template-columns:repeat(2,1fr)!important;}
    .stat-val{font-size:1.3rem!important;}
    .level-card{padding:1.2rem 1.2rem!important;}
    .level-name{font-size:1rem!important;}
    .badge-grid{gap:0.35rem!important;}
    .badge-item{min-width:72px!important;padding:0.65rem 0.6rem!important;}
    .badge-ico{font-size:1.3rem!important;}
    .badge-name{font-size:0.6rem!important;}
    [data-testid="stHorizontalBlock"]:has(.ab-card){flex-direction:column!important;}
    [data-testid="stHorizontalBlock"]:has(.ab-card) [data-testid="stColumn"]{width:100%!important;min-width:100%!important;}
    .ab-topic-name{min-width:80px!important;font-size:0.78rem!important;}
}
@media (max-width:480px){
    .stat-grid{grid-template-columns:repeat(2,1fr)!important;gap:0.5rem!important;}
    .stat-val{font-size:1.1rem!important;}
}
/* Mobile navbar fix - match flashcards.py */
@media (max-width: 768px) {
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        padding: 0.55rem 0.75rem !important;
        gap: 0.5rem !important;
    }
    
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"],
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
        width: auto !important;
        min-width: auto !important;
        flex: 0 0 auto !important;
    }
    
    section.main > div > div:first-child [data-testid="stHorizontalBlock"]:first-of-type [data-testid="stColumn"]:first-child,
    [data-testid="stMain"] > div > div > div:first-child [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child {
        flex: 1 1 100% !important;
        margin-bottom: 0.3rem !important;
    }
} 
</style>
""", unsafe_allow_html=True)

# ============================================
# NAVIGATION BAR - FIXED to match flashcards.py
# ============================================
_l, _sp, _h, _p, _fc, _av = st.columns([2, 0.5, 0.6, 0.6, 0.6, 0.6])
with _l:
    st.markdown('<div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;"><div style="width:26px;height:26px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.82rem;flex-shrink:0;">🤖</div><span style="font-size:0.97rem;font-weight:800;letter-spacing:-0.03em;background:linear-gradient(90deg,#fff,#06B6D4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">AlgoBuddy · Progress</span></div>', unsafe_allow_html=True)
with _h:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🏠", key="nh", use_container_width=True): 
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _p:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🧮", key="np", use_container_width=True): 
        st.switch_page("pages/practice.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _fc:
    st.markdown('<div class="ab-pill-btn">', unsafe_allow_html=True)
    if st.button("🃏", key="nfc", use_container_width=True): 
        st.switch_page("pages/flashcards.py")
    st.markdown('</div>', unsafe_allow_html=True)
with _av:
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div class="ab-avatar-circle">{initials}</div></div>', unsafe_allow_html=True)

# JS to fix nav
import streamlit.components.v1 as _c
_c.html("""<script>
(function(){
    function fix(){
        try{
            var doc=window.parent.document;
            var b=doc.querySelector('[data-testid="stHorizontalBlock"]');
            if(!b) return;
            b.style.setProperty('flex-wrap','nowrap','important');
            b.style.setProperty('align-items','center','important');
            var cols=b.querySelectorAll(':scope > [data-testid="stColumn"]');
            cols.forEach(function(c,i){
                if(i===0){c.style.setProperty('flex','1 1 auto','important');}
                else{c.style.setProperty('flex','0 0 auto','important');c.style.setProperty('min-width','0','important');c.style.setProperty('width','auto','important');}
            });
        }catch(e){}
    }
    fix(); setTimeout(fix,200); setTimeout(fix,600);
    new MutationObserver(fix).observe(document.body,{childList:true,subtree:true});
})();
</script>""", height=0)

# ============================================
# MAIN CONTENT - Using cached data
# ============================================
stats = tracker.stats
summary = tracker.get_stats_summary()
level = summary["level"]
lp = summary["level_progress"]
xp = summary["xp"]
earned_badges = summary["earned_badges"]
t1_ids = {b["id"] for b in BADGES}
tier2_unlocked = t1_ids.issubset(set(earned_badges))

_,main_col,_ = st.columns([1,8,1])
with main_col:
    st.markdown("<div style='padding:1.8rem 0 4rem'>", unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:1.3rem;font-weight:800;color:#fff;letter-spacing:-0.03em;margin-bottom:1.5rem;">📈 {sname}\'s Progress</div>', unsafe_allow_html=True)

    # Level + XP card
    next_level = LEVELS[min(LEVELS.index(level)+1, len(LEVELS)-1)]
    level_idx = LEVELS.index(level)
    xp_bar_pct = lp["pct"]

    pips_html = "".join(
        f'<div class="level-pip {"done" if i <= level_idx else ""}"></div>'
        for i in range(len(LEVELS))
    )

    st.markdown(f"""
    <div class="level-card">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
                <div class="level-icon">{level['icon']}</div>
                <div class="level-name">{level['name']}</div>
                <div class="level-xp">{xp} XP total</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.72rem;color:var(--t3);margin-bottom:0.2rem;">Next: {next_level['name']} {next_level['icon']}</div>
                <div style="font-size:1.1rem;font-weight:700;color:var(--teal);">{lp['needed']} XP to go</div>
            </div>
        </div>
        <div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{xp_bar_pct}%;"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:var(--t3);margin-bottom:0.7rem;">
            <span>{level['min_xp']} XP</span><span>{xp} XP</span><span>{level['min_xp']+1} XP</span>
        </div>
        <div class="level-track">{pips_html}</div>
    </div>""", unsafe_allow_html=True)

    # Stat cards
    stat_data = [
        ("🧩", "Problems", stats["problems_attempted"]),
        ("🎯", "Accuracy", f"{tracker.get_accuracy():.1f}%"),
        ("❤️‍🔥", "Streak", f"{stats['current_streak']} days"),
        ("🥇", "Best", f"{stats.get('longest_streak',0)} days"),
        ("💡", "Hint-Free", stats.get("hint_free_solves",0)),
    ]
    stat_html = "".join(
        f'<div class="stat-card"><div style="font-size:0.82rem;color:var(--t3);margin-bottom:0.3rem;">{icon} {label}</div>'
        f'<div class="stat-val">{val}</div></div>'
        for icon,label,val in stat_data
    )
    st.markdown(f'<div class="stat-grid">{stat_html}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)

    # Two-column layout
    left, right = st.columns([3, 2], gap="large")

    with left:
        # Topic performance
        topic_perf = stats.get("topic_performance", {})
        rows_html = ""
        if topic_perf:
            for topic, data in sorted(topic_perf.items(), key=lambda x: -x[1]["accuracy"]):
                acc = data["accuracy"]
                pct = int(acc)
                tname = topic.replace("_", " ").title()
                colour = "#10B981" if acc >= 80 else "#F59E0B" if acc >= 60 else "#EF4444"
                rows_html += (
                    '<div class="ab-topic-row">'
                    f'<span class="ab-topic-name">{tname}</span>'
                    f'<div class="ab-bar-bg"><div class="ab-bar-fill" style="width:{pct}%;background:{colour};"></div></div>'
                    f'<span class="ab-topic-acc">{acc:.0f}%</span>'
                    '</div>'
                )
        else:
            rows_html = '<div style="font-size:0.88rem;color:var(--t3);padding:0.5rem 0;">No problems attempted yet — head to Practice! 💪</div>'
        st.markdown(f'<div class="ab-card"><div class="ab-card-title">Topic Performance</div>{rows_html}</div>', unsafe_allow_html=True)

        # Recent XP history
        xp_hist = list(reversed(stats.get("xp_history", [])))[:10]
        if xp_hist:
            rows = ""
            for entry in xp_hist:
                rows += f'<div class="xp-row"><span class="xp-reason">{entry["reason"]}</span><span class="xp-amount">+{entry["amount"]} XP</span></div>'
            st.markdown(f'<div class="ab-card"><div class="ab-card-title">Recent XP</div>{rows}</div>', unsafe_allow_html=True)

    with right:
        # Tier 1 Badges
        badges_html = ""
        earned_count = 0
        for badge in BADGES:
            earned = badge["id"] in earned_badges
            if earned: 
                earned_count += 1
            cls = "badge-item earned" if earned else "badge-item"
            badges_html += f'<div class="{cls}" data-tip="{badge["desc"]}"><div class="badge-ico">{badge["icon"]}</div><div class="badge-name">{badge["name"]}</div></div>'
        st.markdown(
            f'<div class="ab-card"><div class="ab-card-title">Badges &nbsp;<span style="font-weight:400;color:var(--t3);">{earned_count}/{len(BADGES)}</span></div>'
            f'<div class="badge-grid">{badges_html}</div></div>',
            unsafe_allow_html=True
        )

        # Tier 2 Badges
        if tier2_unlocked:
            t2_earned = sum(1 for b in BADGES_TIER2 if b["id"] in earned_badges)
            t2_html = ""
            for badge in BADGES_TIER2:
                earned = badge["id"] in earned_badges
                cls = "badge-item tier2 earned" if earned else "badge-item tier2"
                t2_html += f'<div class="{cls}" data-tip="{badge["desc"]}"><div class="badge-ico">{badge["icon"]}</div><div class="badge-name">{badge["name"]}</div></div>'
            st.markdown(
                f'<div class="ab-card" style="border-color:rgba(139,92,246,0.25);background:rgba(139,92,246,0.04);">'
                f'<div class="ab-card-title" style="color:#a78bfa;">✦ Tier 2 &nbsp;<span style="font-weight:400;color:var(--t3);">{t2_earned}/{len(BADGES_TIER2)}</span></div>'
                f'<div class="badge-grid">{t2_html}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="ab-card" style="opacity:0.5;">'
                f'<div class="ab-card-title" style="color:var(--t3);">🔒 Tier 2 &nbsp;<span style="font-weight:400;">0/{len(BADGES_TIER2)}</span></div>'
                f'<div style="font-size:0.8rem;color:var(--t3);font-style:italic;">Earn all Tier 1 badges to unlock.</div></div>',
                unsafe_allow_html=True
            )

        # Activity
        st.markdown(f"""
        <div class="ab-card">
            <div class="ab-card-title">Activity</div>
            <div style="display:flex;flex-direction:column;gap:0.6rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.88rem;"><span style="color:var(--t2);">🃏 Flashcards reviewed</span><span style="color:#4DB8FF;font-family:var(--mono);font-weight:700;">{stats.get('flashcards_reviewed',0)}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:0.88rem;"><span style="color:var(--t2);">💬 Chat sessions</span><span style="color:#4DB8FF;font-family:var(--mono);font-weight:700;">{stats.get('chat_sessions',0)}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:0.88rem;"><span style="color:var(--t2);">📎 Notes uploaded</span><span style="color:#4DB8FF;font-family:var(--mono);font-weight:700;">{stats.get('notes_uploaded',0)}</span></div>
                <div style="display:flex;justify-content:space-between;font-size:0.88rem;"><span style="color:var(--t2);">✅ Problems correct</span><span style="color:#4DB8FF;font-family:var(--mono);font-weight:700;">{stats.get('problems_correct',0)}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Recommendations — derive directly from topic_perf so thresholds are correct
        topic_perf_r = stats.get("topic_performance", {})
        weak   = sorted(
            [{"topic": t, "accuracy": d["accuracy"]} for t, d in topic_perf_r.items() if d["accuracy"] < 60],
            key=lambda x: x["accuracy"]
        )
        strong = sorted(
            [{"topic": t, "accuracy": d["accuracy"]} for t, d in topic_perf_r.items() if d["accuracy"] >= 80],
            key=lambda x: -x["accuracy"]
        )
        if weak or strong:
            rec = ""
            if weak:
                rec += '<div style="font-size:0.72rem;font-weight:700;color:#EF4444;letter-spacing:0.08em;margin-bottom:0.35rem;"> NEEDS PRACTICE</div>'
                for t in weak[:3]:
                    rec += f'<div style="font-size:0.84rem;color:var(--t2);padding:0.15rem 0;">• {t["topic"].replace("_"," ").title()} — {t["accuracy"]:.0f}%</div>'
            if strong:
                rec += '<div style="font-size:0.72rem;font-weight:700;color:#10B981;letter-spacing:0.08em;margin:0.7rem 0 0.35rem;"> STRONG AREAS</div>'
                for t in strong[:3]:
                    rec += f'<div style="font-size:0.84rem;color:var(--t2);padding:0.15rem 0;">• {t["topic"].replace("_"," ").title()} — {t["accuracy"]:.0f}%</div>'
            st.markdown(f'<div class="ab-card"><div class="ab-card-title">Recommendations</div>{rec}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)