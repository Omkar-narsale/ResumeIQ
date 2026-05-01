"""
Authentication module for ResumeIQ
Handles user login, signup, and session management
"""

import bcrypt
import streamlit as st
from db import add_user, get_user_by_email, update_last_login

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except:
        return False

def register_user(email: str, password: str) -> dict:
    """
    Register new user

    Args:
        email: User email
        password: User password (will be hashed)

    Returns:
        {"success": bool, "message": str, "user_id": str or None}
    """
    # Validate inputs
    if not email or "@" not in email:
        return {"success": False, "message": "Invalid email format"}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters"}

    # Check if user exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return {"success": False, "message": "Email already registered"}

    # Create user
    password_hash = hash_password(password)
    user_id = add_user(email, password_hash)

    if user_id:
        return {
            "success": True,
            "message": "Account created successfully!",
            "user_id": user_id
        }
    else:
        return {
            "success": False,
            "message": "Registration failed. Please try again."
        }

def login_user(email: str, password: str) -> dict:
    """
    Login user

    Args:
        email: User email
        password: User password

    Returns:
        {"success": bool, "message": str, "user_id": str or None, "email": str or None}
    """
    # Get user
    user = get_user_by_email(email)

    if not user:
        return {"success": False, "message": "Email not found"}

    # Verify password
    if not verify_password(password, user['password_hash']):
        return {"success": False, "message": "Invalid password"}

    # Update last login
    update_last_login(user['id'])

    return {
        "success": True,
        "message": "Login successful!",
        "user_id": user['id'],
        "email": user['email']
    }

def logout_user():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.email = None

def is_logged_in() -> bool:
    """Check if user is logged in"""
    return st.session_state.get("logged_in", False)

def get_current_user() -> dict:
    """Get current user info"""
    if is_logged_in():
        return {
            "user_id": st.session_state.user_id,
            "email": st.session_state.email
        }
    return None
