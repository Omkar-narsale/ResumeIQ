"""
Login and signup page for ResumeIQ
"""

import streamlit as st
from utils.auth import login_user, register_user, logout_user

def show_login_page():
    """Display login/signup page"""
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 40px;
        background-color: #111827;
        border-radius: 12px;
        border: 1px solid #1F2937;
    }
    .login-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .divider {
        text-align: center;
        margin: 20px 0;
        color: #6B7280;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.auth_mode = "signup"
            st.rerun()

    st.markdown('<div class="divider">─────────────────────</div>', unsafe_allow_html=True)

    if st.session_state.auth_mode == "login":
        show_login_form()
    else:
        show_signup_form()

    st.markdown("---")
    st.info("💡 **Demo Mode**: You can use email: `demo@example.com` password: `demo123` to test")

    if st.button("👤 Continue as Guest", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user_id = "guest"
        st.session_state.email = "guest@example.com"
        st.session_state.is_guest = True
        st.rerun()

def show_login_form():
    """Display login form"""
    st.markdown("<h3 style='text-align: center;'>Welcome Back</h3>", unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input(
            "Email",
            placeholder="your@email.com",
            label_visibility="collapsed"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            label_visibility="collapsed"
        )

        submit = st.form_submit_button("🔓 Login", use_container_width=True)

        if submit:
            if not email or not password:
                st.error("❌ Please enter email and password")
            else:
                result = login_user(email, password)

                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.user_id = result["user_id"]
                    st.session_state.email = result["email"]
                    st.session_state.is_guest = False
                    st.success(result["message"])
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

def show_signup_form():
    """Display signup form"""
    st.markdown("<h3 style='text-align: center;'>Create Account</h3>", unsafe_allow_html=True)

    with st.form("signup_form"):
        email = st.text_input(
            "Email",
            placeholder="your@email.com",
            label_visibility="collapsed"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 6 characters",
            label_visibility="collapsed"
        )
        password_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm password",
            label_visibility="collapsed"
        )

        submit = st.form_submit_button("✍️ Create Account", use_container_width=True)

        if submit:
            if not email or not password:
                st.error("❌ Please fill all fields")
            elif password != password_confirm:
                st.error("❌ Passwords don't match")
            else:
                result = register_user(email, password)

                if result["success"]:
                    st.success(result["message"])
                    st.info("✅ Account created! Now you can login.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")

def show_logout_button():
    """Show logout button in sidebar"""
    with st.sidebar:
        if st.session_state.get("logged_in"):
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.get("is_guest"):
                    st.write("👤 **Guest**")
                else:
                    st.write(f"👤 **{st.session_state.email.split('@')[0]}**")
            with col2:
                if st.button("🚪 Logout", use_container_width=True):
                    logout_user()
                    st.rerun()
