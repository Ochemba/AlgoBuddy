import streamlit as st

st.set_page_config(page_title="AlgoBuddy — Create Account", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")

from auth import AuthManager
_auth = AuthManager()

for k, v in {
    "logged_in": False, "username": None,
    "messages": [], "student_name": "Student",
    "active_course": None, "active_topic": None,
    "persona": "default", "use_scaffolding": False,
    "view": "home", "thinking": False,
    "show_courses": False, "show_settings": False,
    "tracker": None,
    "auth_error": "", "auth_success": "",
    "auth_mode": "signup", "cin_key": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.logged_in:
    st.switch_page("app.py")

# Same AUTH_BTN_STYLE from app.py
AUTH_BTN_STYLE = """<style>
[data-testid="stBaseButton-secondary"]:not(.ab-pill-btn *):not(.ab-cu-btn *):not(.remove-file-btn *){
    background:linear-gradient(135deg,#1B2B6B,#06B6D4)!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
    border:none!important;border-radius:12px!important;font-weight:700!important;height:44px!important;font-size:0.92rem!important;
    width:auto!important;min-width:160px!important;max-width:260px!important;padding:0 2rem!important;
    box-shadow:0 4px 20px rgba(6,182,212,0.35)!important;display:block!important;margin:0 auto!important;
}
/* Force white text on page links */
[data-testid="stPageLink-Link"],
[data-testid="stPageLink-Link"]:link,
[data-testid="stPageLink-Link"]:visited,
[data-testid="stPageLink-Link"] span,
[data-testid="stPageLink-Link"] p,
div[data-testid="stPageLink"] a,
div[data-testid="stPageLink"] a:link,
div[data-testid="stPageLink"] a:visited,
div[data-testid="stPageLink"] a span {
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
    background: transparent !important;
}
[data-testid="stPageLink-Link"]:hover,
[data-testid="stPageLink-Link"]:hover *,
div[data-testid="stPageLink"] a:hover,
div[data-testid="stPageLink"] a:hover span {
    color: #06B6D4 !important;
    -webkit-text-fill-color: #06B6D4 !important;
}
[data-testid="stPageLink"] p {
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
}
[data-testid="stPageLink"]:hover p {
    color: #06B6D4 !important;
    -webkit-text-fill-color: #06B6D4 !important;
}
[data-testid="stPageLink"] {
    display: flex !important;
    justify-content: center !important;
    margin-top: 0.6rem !important;
}
</style>"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
:root{ --font:'Plus Jakarta Sans',sans-serif; --teal:#06B6D4; --t1:#EEF2FF; --t2:#A8B4D8; }
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
.auth-logo{display:flex;align-items:center;gap:0.7rem;justify-content:center;margin-bottom:1.8rem;}
.auth-logo-icon{width:40px;height:40px;background:linear-gradient(135deg,#1B2B6B,#06B6D4);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;}
.auth-sub{font-size:0.88rem;color:#A8B4D8;text-align:center;margin-bottom:1.6rem;}
.auth-tabs{display:flex;gap:0;margin-bottom:1.8rem;border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,0.1);}
.auth-tab{flex:1;padding:0.55rem 0;text-align:center;font-size:0.88rem;font-weight:600;color:#A8B4D8;background:rgba(255,255,255,0.03);}
.auth-tab.active{background:rgba(6,182,212,0.18);color:#06B6D4;border-bottom:2px solid #06B6D4;}

/* ══ INPUTS — dark bg on ALL states including focus ══ */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active,
[data-testid="stTextInput"] input:hover,
[data-testid="stTextInput"] input:not([disabled]) {
    background: #0f1d5e !important;
    background-color: #0f1d5e !important;
    color: #EEF2FF !important;
    -webkit-text-fill-color: #EEF2FF !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-family: var(--font) !important;
    font-size: 0.9rem !important;
    caret-color: #06B6D4 !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 0 3px rgba(6,182,212,0.15) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: rgba(168,180,216,0.5) !important;
    -webkit-text-fill-color: rgba(168,180,216,0.5) !important;
}
[data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stTextInput"] div[style] {
    background: #0f1d5e !important;
    background-color: #0f1d5e !important;
}
[data-testid="stTextInput"] label {
    color: #A8B4D8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

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
</style>
""", unsafe_allow_html=True)

_, auth_col, _ = st.columns([1, 2, 1])
with auth_col:
    st.markdown("""
    <div class="auth-logo">
        <div class="auth-logo-icon">🤖</div>
        <span style="font-size:1.5rem;font-weight:800;color:#EEF2FF;">AlgoBuddy</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="auth-tabs">
        <div class="auth-tab">Sign In</div>
        <div class="auth-tab active">Create Account</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
    if st.session_state.auth_success:
        st.success(st.session_state.auth_success)

    st.markdown('<div class="auth-sub">Join AlgoBuddy. Your AI-powered CS tutor 🎓</div>', unsafe_allow_html=True)

    # Define each field ONCE - no duplicates
    su_email = st.text_input("Email address", key="su_email", placeholder="you@example.com")
    su_name = st.text_input("Your name", key="su_name", placeholder="e.g. Obianuju")
    su_user = st.text_input("Choose a username", key="su_user", placeholder="e.g. uju123 (letters, numbers, _ only)")
    su_pass = st.text_input("Password", key="su_pass", placeholder="At least 6 characters", type="password")
    su_pass2 = st.text_input("Confirm password", key="su_pass2", placeholder="Repeat your password", type="password")

    # Apply AUTH_BTN_STYLE before the button
    st.markdown(AUTH_BTN_STYLE, unsafe_allow_html=True)

    if st.button("Create Account →", key="su_btn", use_container_width=False):
        # Validate all fields
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
            # Pass email, username, display_name, password to signup
            ok, msg = _auth.signup(su_email, su_user, su_name, su_pass)
            if ok:
                st.session_state.auth_success = f"✅ Account created! Please check your email to confirm, then sign in."
                st.session_state.auth_error = ""
                # Don't auto-redirect - let user know to check email
                st.rerun()
            else:
                st.session_state.auth_error = msg
                st.rerun()

    st.page_link("app.py", label="Already have an account? \nSign in →")