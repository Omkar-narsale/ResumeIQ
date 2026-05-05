"""
ResumeIQ - Professional SaaS Dashboard
PERMANENT FIX: Zero top spacing
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.features import analyze_resume, generate_career_roadmap_fast
from utils.resume_parser import extract_text
from utils.unified_analysis import generate_unified_analysis, get_cache_key
from utils.auth import is_logged_in, get_current_user
from utils.progress_tracker import add_score_record
from pages.login import show_login_page, show_logout_button
from pages.progress_dashboard import show_progress_dashboard
from utils.resume_exporter import generate_pdf_resume, generate_docx_resume, generate_csv_export
from pages.salary_guide import show_salary_guide

load_dotenv()

# Initialize database
import db
db.init_db()

# Check authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "email" not in st.session_state:
    st.session_state.email = None
if "is_guest" not in st.session_state:
    st.session_state.is_guest = False

# Show login page if not authenticated
if not st.session_state.logged_in:
    st.set_page_config(
        page_title="ResumeIQ - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    show_login_page()
    st.stop()

st.set_page_config(
    page_title="ResumeIQ - AI Career Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== STEP 1: INJECT MANDATORY CSS AT TOP =====
st.markdown("""
<style>
/* REMOVE ALL DEFAULT SPACING */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    margin-top: 0 !important;
}

/* REMOVE STREAMLIT HEADER */
[data-testid="stHeader"] {
    display: none !important;
}

/* REMOVE TOP GAP FROM APP */
div[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* RESET MAIN SECTION */
section.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* RESET BODY */
html, body {
    margin: 0;
    padding: 0;
}

/* MAIN CONTENT WRAPPER */
.main-wrapper {
    margin-top: 60px;
    padding: 20px;
    background-color: #0B0F19;
    color: #ffffff;
}

/* TOP NAVBAR */
.top-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 60px;
    background-color: #111827;
    border-bottom: 1px solid #1F2937;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 30px;
    z-index: 999;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

.navbar-logo {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
    min-width: 150px;
}

.navbar-actions {
    display: flex;
    align-items: center;
    gap: 15px;
    min-width: 250px;
    justify-content: flex-end;
}

.navbar-action-btn {
    background-color: transparent !important;
    color: #9CA3AF !important;
    border: 1px solid #374151 !important;
    padding: 6px 12px !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    font-size: 0.85rem !important;
}

.navbar-action-btn:hover {
    color: #3B82F6 !important;
    border-color: #3B82F6 !important;
}

.navbar-profile {
    display: flex;
    align-items: center;
    gap: 8px;
    padding-left: 15px;
    border-left: 1px solid #374151;
}

.navbar-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7C3AED 0%, #3B82F6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
}

.navbar-user {
    display: flex;
    flex-direction: column;
    font-size: 0.75rem;
}

.navbar-username {
    color: #ffffff;
    font-weight: 600;
}

.navbar-status {
    color: #6B7280;
    font-size: 0.7rem;
}

h1 {
    font-size: 2.2rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 25px;
    margin-top: 0;
}

h2 {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 20px;
    margin-top: 35px;
}

h3 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 15px;
    margin-top: 0;
}

/* CARD STYLES */
.card {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 20px;
    transition: all 0.3s ease;
}

.card:hover {
    border-color: #3B82F6;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.card-title {
    font-size: 0.85rem;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    font-weight: 600;
}

.card-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 8px 0;
}

.card-desc {
    font-size: 0.85rem;
    color: #9CA3AF;
}

.hero-card {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
    border: none;
}

.hero-card .card-title {
    color: rgba(255, 255, 255, 0.8);
}

.hero-card .card-desc {
    color: rgba(255, 255, 255, 0.9);
}

/* SECTION SPACING */
.section-spacing {
    margin-bottom: 30px;
}

/* COMPARISON CARDS */
.comparison-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 20px;
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    margin-bottom: 16px;
}

.comparison-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 12px;
}

.icon-original {
    color: #EF4444;
}

.icon-enhanced {
    color: #4ADE80;
}

.comparison-text {
    font-size: 0.95rem;
    color: #D1D5DB;
    line-height: 1.6;
}

/* ATS CARD */
.ats-card {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 20px;
}

.ats-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 16px;
}

.ats-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #1F2937;
    font-size: 0.95rem;
    color: #D1D5DB;
}

.ats-item:last-child {
    border-bottom: none;
}

.ats-check {
    color: #4ADE80;
    font-weight: 700;
}

/* PROGRESS BAR */
.progress-row {
    padding: 12px 0;
    border-bottom: 1px solid #1F2937;
}

.progress-row:last-child {
    border-bottom: none;
}

.progress-label {
    color: #D1D5DB;
    font-size: 0.95rem;
    margin-bottom: 8px;
}

.progress-container {
    display: flex;
    align-items: center;
    gap: 12px;
}

.progress-bar {
    flex: 1;
    height: 6px;
    background-color: #1F2937;
    border-radius: 3px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
    border-radius: 3px;
}

.progress-percent {
    color: #ffffff;
    font-weight: 600;
    min-width: 35px;
    text-align: right;
}

/* SKILLS CARD */
.skills-card {
    background-color: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 20px;
}

.skills-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
}

.skills-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.skill-tag {
    background-color: #1F2937;
    color: #D1D5DB;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    border: 1px solid #374151;
    transition: all 0.3s;
}

.skill-tag:hover {
    background-color: #3B82F6;
    color: white;
    border-color: #2563EB;
}

.skill-tag.weak {
    border-color: #F59E0B;
    color: #FBBF24;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0B0F19 !important;
    border-right: 1px solid #1F2937 !important;
    margin-top: 60px !important;
    padding-top: 20px !important;
}

/* SIDEBAR BUTTONS */
.stButton > button {
    background-color: #1F2937 !important;
    color: #9CA3AF !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin: 6px 0 !important;
    transition: all 0.3s !important;
}

.stButton > button:hover {
    background-color: #374151 !important;
    color: #3B82F6 !important;
    border-color: #3B82F6 !important;
}

/* INPUTS */
input, textarea, select {
    background-color: #1F2937 !important;
    color: #ffffff !important;
    border: 1px solid #374151 !important;
    border-radius: 8px !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

/* TEXT COLORS */
p, div, span, label {
    color: #ffffff !important;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0B0F19;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4B5563;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .top-navbar {
        padding: 0 15px;
    }

    .main-wrapper {
        padding: 15px;
    }

    h1 {
        font-size: 1.8rem;
    }

    h2 {
        font-size: 1.3rem;
    }

    .comparison-row {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# ===== STEP 2: RENDER NAVBAR =====
st.markdown("""
<div class="top-navbar">
    <div class="navbar-logo">🚀 ResumeIQ</div>
    <div class="navbar-actions">
        <button class="navbar-action-btn">📤 Export</button>
        <button class="navbar-action-btn">🔗 Share</button>
        <div class="navbar-profile">
            <div class="navbar-avatar">O</div>
            <div class="navbar-user">
                <div class="navbar-username">Omkar</div>
                <div class="navbar-status">Active</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== INITIALIZE SESSION STATE =====
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "interview_question" not in st.session_state:
    st.session_state.interview_question = None
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "job_role" not in st.session_state:
    st.session_state.job_role = ""
if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = {
        "score": "0/10",
        "strengths": "No resume analyzed yet",
        "weaknesses": "Upload a resume to get started",
        "suggestions": "Upload a resume to get personalized suggestions",
        "file_name": "No resume uploaded"
    }
if "score_history" not in st.session_state:
    st.session_state.score_history = []
if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = {}
if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = {}
if "latest_file" not in st.session_state:
    st.session_state.latest_file = "No resume uploaded"

# ===== PAGE FUNCTIONS =====

def show_dashboard():
    st.markdown('<h1>Dashboard Overview</h1>', unsafe_allow_html=True)

    # Check if analysis exists
    analysis = st.session_state.get("latest_analysis", {})

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        score_text = analysis.get('score', '0/10') if analysis else '0/10'
        try:
            score_num = int(score_text.split("/")[0])
        except:
            score_num = 0
        st.markdown(f"""
            <div class="card hero-card">
                <div class="card-title">Resume Score</div>
                <div class="card-value">{score_num}</div>
                <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        file_name = st.session_state.get('latest_file', 'No resume uploaded')
        st.markdown(f"""
            <div class="card">
                <div class="card-title">Latest Resume</div>
                <div class="card-value" style="font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{file_name}</div>
                <div class="card-desc">Last analyzed</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    if analysis:
        st.markdown('<h2>Latest Analysis Details</h2>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            skills = analysis.get("matched_skills", [])
            skills_text = "<br>".join([f"• {s.strip('•') if isinstance(s, str) else s}" for s in (skills if isinstance(skills, list) else [skills])[:3]])
            st.markdown(f'<div class="card"><div class="card-title">✓ Skills Found</div><div style="color: #D1D5DB;">{skills_text}</div></div>', unsafe_allow_html=True)

        with col2:
            missing = analysis.get("missing_skills", [])
            missing_text = "<br>".join([f"• {m.strip('•') if isinstance(m, str) else m}" for m in (missing if isinstance(missing, list) else [missing])[:3]])
            st.markdown(f'<div class="card"><div class="card-title">⚠️ Skills Missing</div><div style="color: #D1D5DB;">{missing_text}</div></div>', unsafe_allow_html=True)

        with col3:
            priority = analysis.get("priority_skills", [])
            if isinstance(priority, list):
                priority_text = "<br>".join([f"• {p}" for p in priority[:3]])
            else:
                priority_text = f"• {priority}"
            st.markdown(f'<div class="card"><div class="card-title">🎯 Priority Focus</div><div style="color: #D1D5DB;">{priority_text}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            strengths = analysis.get("strengths", [])
            s_text = "<br>".join([f"• {s.strip('•') if isinstance(s, str) else s}" for s in (strengths if isinstance(strengths, list) else [strengths])[:3]])
            st.markdown(f'<div class="card"><div class="card-title">💪 Strengths</div><div style="color: #D1D5DB;">{s_text}</div></div>', unsafe_allow_html=True)

        with col2:
            weaknesses = analysis.get("weaknesses", [])
            w_text = "<br>".join([f"• {w.strip('•') if isinstance(w, str) else w}" for w in (weaknesses if isinstance(weaknesses, list) else [weaknesses])[:3]])
            st.markdown(f'<div class="card"><div class="card-title">📋 Weaknesses</div><div style="color: #D1D5DB;">{w_text}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

        roadmap = analysis.get("learning_roadmap", {})
        st.markdown('<h2>📚 Recommended Path</h2>', unsafe_allow_html=True)
        cols = st.columns(3, gap="medium")

        with cols[0]:
            st.markdown(f"""<div class="card">
                <div class="card-title">Level 1: Beginner</div>
                <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('beginner', 'Start with basics')}</div>
            </div>""", unsafe_allow_html=True)

        with cols[1]:
            st.markdown(f"""<div class="card">
                <div class="card-title">Level 2: Intermediate</div>
                <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('intermediate', 'Build skills')}</div>
            </div>""", unsafe_allow_html=True)

        with cols[2]:
            st.markdown(f"""<div class="card">
                <div class="card-title">Level 3: Advanced</div>
                <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('advanced', 'Master & lead')}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    st.markdown('<h2>Score History</h2>', unsafe_allow_html=True)
    if len(st.session_state.score_history) > 0:
        history_html = " → ".join([str(s) for s in st.session_state.score_history])
        st.markdown(f'<div class="card"><div style="color: #D1D5DB; font-size: 1.1rem;">Progress: {history_html}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="card"><div style="color: #9CA3AF;">📤 Upload resume to see score history</div></div>', unsafe_allow_html=True)

    if analysis:
        st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
        st.markdown('<h2>Quick Stats</h2>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            skills = analysis.get("matched_skills", [])
            skill_count = len(skills) if isinstance(skills, list) else 1
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">Skills Detected</div>
                    <div class="card-value">{skill_count}</div>
                    <div class="card-desc">From your resume</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            missing = analysis.get("missing_skills", [])
            missing_count = len(missing) if isinstance(missing, list) else 1
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">Skills to Develop</div>
                    <div class="card-value">{missing_count}</div>
                    <div class="card-desc">Priority areas</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            score_text = analysis.get('score', '5/10')
            try:
                score = int(score_text.split("/")[0])
            except:
                score = 5
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">Latest Score</div>
                    <div class="card-value">{score}</div>
                    <div class="card-desc">/10 - Updated</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    if analysis:
        st.markdown('<h2>Next Steps</h2>', unsafe_allow_html=True)

        suggestions = analysis.get("strengths", [])
        if isinstance(suggestions, list):
            suggestions_text = "<br>".join([f"✓ {s.strip('•')}" for s in suggestions[:2]])
        else:
            suggestions_text = f"✓ {suggestions.strip('•')}"

        st.markdown(f"""
            <div class="card" style="margin-bottom: 12px;">
                <div style="font-weight: 600; color: #4ADE80; margin-bottom: 8px;">Strengths to Highlight</div>
                <div style="font-size: 0.9rem; color: #D1D5DB;">{suggestions_text}</div>
            </div>
        """, unsafe_allow_html=True)

        weaknesses = analysis.get("weaknesses", [])
        if isinstance(weaknesses, list):
            weaknesses_text = "<br>".join([f"→ {w.strip('•')}" for w in weaknesses[:2]])
        else:
            weaknesses_text = f"→ {weaknesses.strip('•')}"

        st.markdown(f"""
            <div class="card">
                <div style="font-weight: 600; color: #FBBF24; margin-bottom: 8px;">Areas to Improve</div>
                <div style="font-size: 0.9rem; color: #D1D5DB;">{weaknesses_text}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="card"><div style="color: #9CA3AF; text-align: center;">📤 Upload a resume to see recommendations</div></div>', unsafe_allow_html=True)

def show_resume_review():
    st.markdown('<h1>📄 Resume Review</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Upload & Analyze</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Upload your resume to receive AI-powered analysis and feedback.
            </div>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose PDF resume", type="pdf")

    if uploaded_file is not None:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

        if st.button("🔍 Analyze Resume"):
            try:
                # Extract text from PDF
                resume_text = extract_text(uploaded_file)

                # Get target role if available
                target_role = st.session_state.get("target_role_analysis", None)

                # Analyze resume using AI
                with st.spinner("🤖 Analyzing your resume..."):
                    analysis = analyze_resume(resume_text, target_role)

                # Store analysis in session state
                analysis_data = {
                    "score": analysis.get("score", "0/10"),
                    "strengths": analysis.get("strengths", ""),
                    "weaknesses": analysis.get("weaknesses", ""),
                    "suggestions": analysis.get("suggestions", ""),
                    "file_name": uploaded_file.name
                }
                st.session_state.resume_analysis = analysis_data
                st.session_state.latest_analysis = analysis_data
                st.session_state.latest_file = uploaded_file.name

                # Save to database for progress tracking
                if st.session_state.user_id and st.session_state.user_id != "guest":
                    try:
                        score_num = int(analysis.get("score", "0/10").split("/")[0])
                        add_score_record(
                            st.session_state.user_id,
                            score_num,
                            target_role or "General",
                            uploaded_file.name,
                            resume_text,
                            analysis
                        )
                    except Exception as e:
                        st.warning(f"Could not save to progress: {str(e)}")

                st.markdown('<h2>📊 Resume Analysis Report</h2>', unsafe_allow_html=True)

                # Score Card
                score_text = analysis.get("score", "ERROR")

                if score_text == "ERROR":
                    st.error("❌ LLM Analysis Failed - Check terminal for error details")
                    with st.expander("What went wrong?"):
                        st.write("""
                        Possible causes:
                        1. **Ollama not running** - Start with: `ollama serve`
                        2. **Model not loaded** - Check: `ollama list`
                        3. **Network issue** - Restart Ollama
                        4. **Memory issue** - Close other apps

                        Check terminal output for details!
                        """)
                    return

                try:
                    score_num = int(score_text.split("/")[0]) if "/" in score_text else 0
                except:
                    score_num = 0

                st.markdown(f"""
                    <div class="card hero-card">
                        <div class="card-title">Overall Score</div>
                        <div class="card-value">{score_num}</div>
                        <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

                # DEBUG: Show what we received
                with st.expander("🔍 Debug - Raw Analysis Data"):
                    st.code(f"Score: {repr(analysis.get('score', 'MISSING'))}\nStrengths: {repr(analysis.get('strengths', 'MISSING')[:150])}\nWeaknesses: {repr(analysis.get('weaknesses', 'MISSING')[:150])}")

                st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

                # Strengths & Weaknesses
                col1, col2 = st.columns(2, gap="medium")

                with col1:
                    strengths_raw = analysis.get("strengths", "")
                    if strengths_raw and "<" not in strengths_raw:
                        strengths = strengths_raw.split("\n")
                        strengths_html = "<br>".join([s.strip() for s in strengths if s.strip()])
                    else:
                        strengths_html = "• Well-structured content<br>• Clear organization<br>• Professional presentation"

                    st.markdown(f"""
                        <div class="card">
                            <div class="skills-header" style="margin-bottom: 16px;">
                                <span>✓</span>
                                <span>Strengths</span>
                            </div>
                            <div style="color: #D1D5DB; line-height: 1.8;">
                                {strengths_html}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    weaknesses_raw = analysis.get("weaknesses", "")
                    if weaknesses_raw and "<" not in weaknesses_raw:
                        weaknesses = weaknesses_raw.split("\n")
                        weaknesses_html = "<br>".join([w.strip() for w in weaknesses if w.strip()])
                    else:
                        weaknesses_html = "• Add more quantifiable metrics<br>• Include technical skills<br>• Strengthen action verbs"

                    st.markdown(f"""
                        <div class="card">
                            <div class="skills-header" style="margin-bottom: 16px; color: #FBBF24;">
                                <span>⚠️</span>
                                <span>Areas to Improve</span>
                            </div>
                            <div style="color: #D1D5DB; line-height: 1.8;">
                                {weaknesses_html}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

                # Suggestions
                st.markdown('<h2>💡 Recommendations</h2>', unsafe_allow_html=True)
                suggestions_raw = analysis.get("suggestions", "")
                if suggestions_raw and "<" not in suggestions_raw:
                    suggestions = suggestions_raw.split("\n")
                    suggestions_text = "<br>".join([s.strip() for s in suggestions if s.strip()])
                else:
                    suggestions_text = "• Quantify your achievements with metrics<br>• Add technical skills section<br>• Use stronger action verbs<br>• Improve formatting consistency"

                st.markdown(f"""
                    <div class="card">
                        <div style="color: #D1D5DB; line-height: 1.8;">
                            {suggestions_text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

                # Export section
                st.markdown('<h2>📥 Export Resume</h2>', unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    template = st.selectbox("Template", ["Modern", "Classic", "Minimal"], key="export_template")

                with col2:
                    if st.button("📄 PDF", use_container_width=True, key="export_pdf"):
                        st.session_state.export_format = "pdf"
                        st.session_state.export_template = template

                with col3:
                    if st.button("📝 DOCX", use_container_width=True, key="export_docx"):
                        st.session_state.export_format = "docx"

                with col4:
                    if st.button("📊 CSV", use_container_width=True, key="export_csv"):
                        st.session_state.export_format = "csv"

                # Render download button based on session state
                if st.session_state.get("export_format"):
                    try:
                        if st.session_state.export_format == "pdf":
                            pdf_data = generate_pdf_resume(resume_text, st.session_state.get("export_template", "modern").lower())
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=pdf_data,
                                file_name="resume.pdf",
                                mime="application/pdf",
                                key="download_pdf_button"
                            )
                        elif st.session_state.export_format == "docx":
                            docx_data = generate_docx_resume(resume_text)
                            st.download_button(
                                label="⬇️ Download DOCX",
                                data=docx_data,
                                file_name="resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key="download_docx_button"
                            )
                        elif st.session_state.export_format == "csv":
                            csv_data = generate_csv_export(st.session_state.latest_analysis)
                            st.download_button(
                                label="⬇️ Download CSV",
                                data=csv_data,
                                file_name="analysis.csv",
                                mime="text/csv",
                                key="download_csv_button"
                            )
                    except Exception as e:
                        st.error(f"Error generating export: {str(e)}")

                st.success("✅ Resume analysis complete!")

            except Exception as e:
                st.error(f"❌ Error analyzing resume: {str(e)}")

    else:
        st.info("📤 Upload a PDF resume to get started with AI-powered analysis.")

def show_interview():
    st.markdown('<h1>🎤 Mock Interview</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Practice Interviews</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Enter your target role and practice with AI-generated interview questions.
            </div>
        </div>
    """, unsafe_allow_html=True)

    job_role = st.text_input("Enter your target job role", placeholder="e.g., Software Engineer, Product Manager")

    if job_role:
        st.session_state.job_role = job_role

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎲 Generate Question"):
                st.session_state.interview_question = f"What are your key strengths for a {job_role} position?"
                st.session_state.question_count += 1

        with col2:
            if st.button("🔄 Reset Interview"):
                st.session_state.interview_question = None
                st.session_state.question_count = 0

        if st.session_state.interview_question:
            st.markdown('<h3>Question #{}</h3>'.format(st.session_state.question_count), unsafe_allow_html=True)
            st.info(st.session_state.interview_question)

            answer = st.text_area("Your Answer", height=120, placeholder="Type your answer here...")

            if st.button("✅ Submit Answer"):
                if answer:
                    st.success("Great answer! Feedback: Your response was clear and relevant.")
                    st.info("Example better answer: [AI-generated example would appear here]")
                else:
                    st.warning("Please provide an answer first.")

def show_job_match():
    st.markdown('<h1>🎯 Job Match</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Find Your Match</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Paste a job description and see how well your resume matches the requirements.
            </div>
        </div>
    """, unsafe_allow_html=True)

    job_description = st.text_area("Paste Job Description", height=200, placeholder="Paste the job description here...")

    if st.button("📊 Analyze Match"):
        if job_description:
            st.markdown('<h3>Match Results</h3>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                    <div class="card">
                        <div class="card-title">Overall Match</div>
                        <div class="card-value">78%</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class="card">
                        <div class="card-title">Skills Match</div>
                        <div class="card-value">82%</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown("""
                    <div class="card">
                        <div class="card-title">Experience Match</div>
                        <div class="card-value">75%</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Please paste a job description first.")

def show_rewriter():
    st.markdown('<h1>✨ Resume Rewriter</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Enhance Your Resume</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Get AI-powered suggestions to improve your resume with stronger language and achievements.
            </div>
        </div>
    """, unsafe_allow_html=True)

    resume_text = st.text_area("Paste your resume text", height=250, placeholder="Paste your resume content here...")

    if st.button("✨ Get Suggestions"):
        if resume_text:
            st.markdown('<h3>AI-Enhanced Version</h3>', unsafe_allow_html=True)
            st.markdown("""
                <div class="card">
                    <div style="color: #D1D5DB; line-height: 1.8;">
                        Your resume has been analyzed. AI suggestions will appear here with improved language,
                        stronger action verbs, and better formatting for ATS compatibility.
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please paste your resume text first.")

def show_learning():
    st.markdown('<h1>📈 Career Advisor</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Career Development</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Get personalized learning recommendations and career growth strategies.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<h2>Generate Learning Path</h2>', unsafe_allow_html=True)

    target_role = st.text_input("Enter your target role", placeholder="e.g., Senior Engineer, Tech Lead, Product Manager, Data Scientist")

    # Add option for AI-powered personalized roadmap
    st.markdown("---")
    st.markdown("**Optional:** Upload your resume for AI-powered personalized recommendations")
    resume_file = st.file_uploader("Choose PDF resume (optional)", type="pdf", key="career_advisor_resume")

    if st.button("🎯 Generate Learning Path"):
        if target_role:
            # Check if resume was uploaded for AI analysis
            resume_text = None
            if resume_file:
                try:
                    resume_text = extract_text(resume_file)
                except:
                    st.warning("Could not extract resume text, using role-based recommendations only.")

            st.markdown(f'<h3>Learning Path for {target_role}</h3>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # If resume provided, show AI-powered analysis first
            if resume_text:
                st.markdown('<h2>🤖 AI-Powered Personalized Roadmap</h2>', unsafe_allow_html=True)
                with st.spinner("Generating personalized roadmap..."):
                    try:
                        roadmap = generate_career_roadmap_fast(target_role, resume_text)

                        # Display strong skills from resume
                        if roadmap.get("strong_skills"):
                            st.markdown('<h3>💪 Skills Found in Your Resume</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                                <div class="card">
                                    <div style="color: #D1D5DB; line-height: 1.8;">
                                        {roadmap.get("strong_skills", "").replace(chr(10), "<br>")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        # Display missing skills
                        if roadmap.get("missing_skills"):
                            st.markdown('<h3>📋 Skills to Develop</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                                <div class="card">
                                    <div style="color: #D1D5DB; line-height: 1.8;">
                                        {roadmap.get("missing_skills", "").replace(chr(10), "<br>")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        # Display roadmap
                        if roadmap.get("roadmap"):
                            st.markdown('<h3>📚 Learning Roadmap</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                                <div class="card">
                                    <div style="color: #D1D5DB; line-height: 1.8; white-space: pre-wrap;">
                                        {roadmap.get("roadmap", "")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        # Display focus areas
                        if roadmap.get("focus_areas"):
                            st.markdown('<h3>🎯 Focus Areas</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                                <div class="card">
                                    <div style="color: #D1D5DB; line-height: 1.8;">
                                        {roadmap.get("focus_areas", "").replace(chr(10), "<br>")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        # Display next actions
                        if roadmap.get("next_actions"):
                            st.markdown('<h3>✅ Next Actions</h3>', unsafe_allow_html=True)
                            st.markdown(f"""
                                <div class="card">
                                    <div style="color: #D1D5DB; line-height: 1.8;">
                                        {roadmap.get("next_actions", "").replace(chr(10), "<br>")}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

                        st.success("✅ AI-powered roadmap generated successfully!")
                        st.markdown("---")
                    except Exception as e:
                        st.error(f"Error generating AI roadmap: {str(e)}")
                        st.info("Showing standard learning path instead...")

            # Display standard learning paths (as before)
            st.markdown('<h2>Structured Learning Paths</h2>', unsafe_allow_html=True)

            # Define role-specific learning paths
            role_paths = {
                "senior engineer": {
                    "phases": [
                        {"title": "Phase 1: Foundation (0-3 Months)", "skills": ["System Design", "Advanced Algorithms", "Architecture Patterns"], "resources": ["System Design Interview Book", "LeetCode Hard Problems", "Build scalable API"]},
                        {"title": "Phase 2: Specialization (3-6 Months)", "skills": ["Distributed Systems", "Database Optimization", "Performance Tuning"], "resources": ["Designing Data-Intensive Applications", "Database Deep Dive", "Profiling"]},
                        {"title": "Phase 3: Leadership (6-12 Months)", "skills": ["Mentoring", "Code Review Mastery", "Technical Decision"], "resources": ["Lead projects", "Mentor engineers", "Architecture design"]}
                    ],
                    "progression": ["Mid-Level", "Senior Engineer", "Staff Engineer"],
                    "courses": ["System Design", "Scalable Architecture", "Advanced Design"],
                    "books": ["Designing Data-Intensive", "Clean Code", "Refactoring"]
                },
                "tech lead": {
                    "phases": [
                        {"title": "Phase 1: Technical Depth (0-3 Months)", "skills": ["Architecture", "Technical Strategy", "Code Quality"], "resources": ["ADR patterns", "Design Patterns", "SOLID Principles"]},
                        {"title": "Phase 2: Team Leadership (3-6 Months)", "skills": ["Team Management", "Communication", "Conflict Resolution"], "resources": ["Leadership course", "Crucial Conversations", "Radical Candor"]},
                        {"title": "Phase 3: Strategic Vision (6-12 Months)", "skills": ["Product Thinking", "Roadmap Planning", "Collaboration"], "resources": ["Sprint planning", "Strategy sessions", "Architecture reviews"]}
                    ],
                    "progression": ["Senior Engineer", "Tech Lead", "Engineering Manager"],
                    "courses": ["Leadership", "Technical Communication", "Strategic Planning"],
                    "books": ["The Phoenix Project", "Team Topologies", "Staff Engineer"]
                },
                "product manager": {
                    "phases": [
                        {"title": "Phase 1: PM Fundamentals (0-3 Months)", "skills": ["Product Strategy", "User Research", "Market Analysis"], "resources": ["Inspired by Cagan", "User interviews", "Competitive analysis"]},
                        {"title": "Phase 2: Execution (3-6 Months)", "skills": ["Roadmap Management", "Stakeholder Management", "Analytics"], "resources": ["OKR framework", "Data-driven decisions", "Stakeholder mgmt"]},
                        {"title": "Phase 3: Strategic Leadership (6-12 Months)", "skills": ["Business Strategy", "Team Building", "Vision Setting"], "resources": ["Lead product vision", "Build teams", "Define direction"]}
                    ],
                    "progression": ["Associate PM", "Product Manager", "Senior PM"],
                    "courses": ["PM Fundamentals", "Data Analytics", "Stakeholder Mgmt"],
                    "books": ["Inspired", "Empowered", "Lean Playbook"]
                },
                "data scientist": {
                    "phases": [
                        {"title": "Phase 1: Advanced ML (0-3 Months)", "skills": ["Deep Learning", "Neural Networks", "Computer Vision"], "resources": ["Fast.ai", "PyTorch", "Kaggle competitions"]},
                        {"title": "Phase 2: Production ML (3-6 Months)", "skills": ["MLOps", "Model Deployment", "Feature Engineering"], "resources": ["MLflow", "Kubeflow", "Model monitoring"]},
                        {"title": "Phase 3: Strategy (6-12 Months)", "skills": ["AI Strategy", "Team Leadership", "Research"], "resources": ["Lead projects", "Publish papers", "Guide direction"]}
                    ],
                    "progression": ["Data Scientist", "Senior Data Scientist", "ML Director"],
                    "courses": ["Advanced ML", "MLOps", "AI Strategy"],
                    "books": ["Hands-On ML", "Deep Learning", "AI-Powered Companies"]
                },
                "engineering manager": {
                    "phases": [
                        {"title": "Phase 1: Management (0-3 Months)", "skills": ["People Management", "1-on-1s", "Performance Mgmt"], "resources": ["Manager's Path", "Crucial Conversations", "Radical Candor"]},
                        {"title": "Phase 2: Team Scaling (3-6 Months)", "skills": ["Hiring", "Team Culture", "Process Design"], "resources": ["Build hiring", "Design workflows", "Define culture"]},
                        {"title": "Phase 3: Strategic Impact (6-12 Months)", "skills": ["Org Design", "Business Acumen", "Executive Comm"], "resources": ["Org changes", "Define strategy", "Presentations"]}
                    ],
                    "progression": ["Team Lead", "Engineering Manager", "Director"],
                    "courses": ["Management", "Executive Comm", "Org Design"],
                    "books": ["Manager's Path", "Elegant Puzzle", "Radical Candor"]
                }
            }

            # Find matching role
            matched_role = None
            for role_key in role_paths.keys():
                if role_key in target_role.lower() or target_role.lower() in role_key:
                    matched_role = role_key
                    break

            path_config = role_paths.get(matched_role, role_paths["senior engineer"])

            # Display phases
            for phase in path_config["phases"]:
                st.markdown(f"""
                    <div class="card" style="margin-bottom: 20px;">
                        <h3 style="margin-top: 0; color: #3B82F6;">{phase['title']}</h3>
                        <div style="color: #D1D5DB; margin-bottom: 15px;">
                            <strong>Skills:</strong><br>
                            {'<br>'.join(['• ' + s for s in phase['skills']])}
                        </div>
                        <div style="color: #D1D5DB;">
                            <strong>Resources:</strong><br>
                            {'<br>'.join(['✓ ' + r for r in phase['resources']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
            st.markdown('<h2>Your Growth Plan</h2>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                    <div class="card">
                        <div class="card-title">Career Progression</div>
                        <div style="color: #D1D5DB; padding: 10px 0; line-height: 2;">
                            {'<br>'.join(['→ ' + p for p in path_config['progression']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="card">
                        <div class="card-title">Top Courses</div>
                        <div style="color: #D1D5DB; padding: 10px 0; line-height: 1.8;">
                            {'<br>'.join(['• ' + c for c in path_config['courses']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class="card">
                        <div class="card-title">Key Focus</div>
                        <div style="color: #D1D5DB; padding: 10px 0; line-height: 1.8;">
                            • Continuous Learning<br>
                            • Hands-on Projects<br>
                            • Mentoring & Networking<br>
                            • Certifications
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="card">
                        <div class="card-title">Must-Read Books</div>
                        <div style="color: #D1D5DB; padding: 10px 0; line-height: 1.8;">
                            {'<br>'.join(['• ' + b for b in path_config['books']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("Please enter a target role to generate your personalized learning path.")

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    # Default learning recommendations
    st.markdown('<h2>Quick Learning Resources</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-title">Top Courses</div>
                <div style="color: #D1D5DB; padding: 10px 0; line-height: 1.8;">
                    • System Design Interview<br>
                    • AWS Solutions Architect<br>
                    • Kubernetes Administration<br>
                    • Leadership Fundamentals
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-title">Books & Articles</div>
                <div style="color: #D1D5DB; padding: 10px 0; line-height: 1.8;">
                    • Designing Data-Intensive Applications<br>
                    • The Phoenix Project<br>
                    • Clean Code<br>
                    • Staff Engineer by Will Larson
                </div>
            </div>
        """, unsafe_allow_html=True)

def show_advanced_analysis():
    """Advanced AI analysis combining skills, ATS, feedback, roadmap in ONE call"""
    st.markdown('<h1>🚀 Advanced Resume Analysis</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card" style="margin-bottom: 20px;">
            <div class="card-title">Unified Deep Dive</div>
            <div style="color: #D1D5DB; padding: 10px 0;">
                Get comprehensive analysis: skills, ATS check, feedback, and learning path in one scan.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        uploaded_file = st.file_uploader("Choose PDF resume", type="pdf", key="advanced_analysis_file")

    with col2:
        target_role = st.text_input("Target role (e.g., Data Analyst, Software Engineer)",
                                   placeholder="Leave empty for general analysis")

    if uploaded_file is not None and st.button("🔍 Run Full Analysis"):
        try:
            resume_text = extract_text(uploaded_file)
            cache_key = get_cache_key(resume_text, target_role or "general")

            # Check cache first
            if cache_key in st.session_state.analysis_cache:
                analysis = st.session_state.analysis_cache[cache_key]
                st.info("📦 Loaded from cache (faster!)")
            else:
                with st.spinner("🤖 Analyzing your resume..."):
                    analysis = generate_unified_analysis(resume_text, target_role or "General Professional")
                    st.session_state.analysis_cache[cache_key] = analysis

            # Extract score for history
            score_str = analysis.get("score", "0/10")
            try:
                score_num = int(score_str.split("/")[0])
            except:
                score_num = 0

            # Track last 3 scores
            st.session_state.score_history.append(score_num)
            st.session_state.score_history = st.session_state.score_history[-3:]

            # Update dashboard data
            st.session_state.latest_analysis = analysis
            st.session_state.latest_file = uploaded_file.name

            # Display results
            st.markdown('<h2>📊 Analysis Results</h2>', unsafe_allow_html=True)

            # Score card
            st.markdown(f"""
                <div class="card hero-card">
                    <div class="card-title">Resume Score</div>
                    <div class="card-value">{score_num}</div>
                    <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # Skills section
            col1, col2, col3 = st.columns(3, gap="medium")

            with col1:
                st.markdown('<h3>✓ Matched Skills</h3>', unsafe_allow_html=True)
                skills_html = "<br>".join([f"• {s}" for s in analysis.get("matched_skills", [])[:3]])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB;">{skills_html}</div></div>',
                           unsafe_allow_html=True)

            with col2:
                st.markdown('<h3>⚠️ Missing Skills</h3>', unsafe_allow_html=True)
                missing_html = "<br>".join([f"• {s}" for s in analysis.get("missing_skills", [])[:3]])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB;">{missing_html}</div></div>',
                           unsafe_allow_html=True)

            with col3:
                st.markdown('<h3>🎯 Priority Skills</h3>', unsafe_allow_html=True)
                priority_html = "<br>".join([f"• {s}" for s in analysis.get("priority_skills", [])[:3]])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB;">{priority_html}</div></div>',
                           unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # Strengths & Weaknesses
            col1, col2 = st.columns(2, gap="medium")

            with col1:
                st.markdown('<h3>💪 Strengths</h3>', unsafe_allow_html=True)
                strengths_html = "<br>".join([f"• {s}" for s in analysis.get("strengths", [])])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB;">{strengths_html}</div></div>',
                           unsafe_allow_html=True)

            with col2:
                st.markdown('<h3>📋 Weaknesses</h3>', unsafe_allow_html=True)
                weaknesses_html = "<br>".join([f"• {s}" for s in analysis.get("weaknesses", [])])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB;">{weaknesses_html}</div></div>',
                           unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # ATS Check
            st.markdown('<h2>🤖 ATS Compatibility</h2>', unsafe_allow_html=True)
            ats_checks = analysis.get("ats_checks", {})
            ats_cols = st.columns(3, gap="medium")

            ats_items = [
                ("Keywords", ats_checks.get("keywords", "Unknown")),
                ("Action Verbs", ats_checks.get("verbs", "Unknown")),
                ("Clarity", ats_checks.get("clarity", "Unknown"))
            ]

            for i, (label, status) in enumerate(ats_items):
                with ats_cols[i]:
                    status_color = "#4ADE80" if status == "Pass" else "#EF4444"
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">{label}</div>
                            <div style="color: {status_color}; font-weight: 700; font-size: 1.2rem;">{status}</div>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # Improved Bullet
            improved = analysis.get("improved_bullet", {})
            if improved.get("original"):
                st.markdown('<h2>💡 Resume Enhancement</h2>', unsafe_allow_html=True)
                st.markdown(f"""
                    <div class="comparison-row">
                        <div>
                            <div class="comparison-header"><span class="icon-original">❌</span> Original</div>
                            <div class="comparison-text">{improved.get('original', '')}</div>
                        </div>
                        <div>
                            <div class="comparison-header"><span class="icon-enhanced">✓</span> Enhanced</div>
                            <div class="comparison-text">{improved.get('improved', '')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # Learning Roadmap
            roadmap = analysis.get("learning_roadmap", {})
            if roadmap:
                st.markdown('<h2>📚 Learning Roadmap</h2>', unsafe_allow_html=True)
                roadmap_cols = st.columns(3, gap="medium")

                with roadmap_cols[0]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">Beginner</div>
                            <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('beginner', 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                with roadmap_cols[1]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">Intermediate</div>
                            <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('intermediate', 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)

                with roadmap_cols[2]:
                    st.markdown(f"""
                        <div class="card">
                            <div class="card-title">Advanced</div>
                            <div style="color: #D1D5DB; font-size: 0.9rem;">{roadmap.get('advanced', 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

            # Score History
            if len(st.session_state.score_history) > 1:
                st.markdown('<h2>📈 Score History</h2>', unsafe_allow_html=True)
                history_html = " → ".join([str(s) for s in st.session_state.score_history])
                st.markdown(f'<div class="card"><div style="color: #D1D5DB; font-size: 1.1rem;">{history_html}</div></div>',
                           unsafe_allow_html=True)

            st.success("✅ Analysis complete! Results cached for speed.")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    else:
        st.info("📤 Upload a resume and enter target role to begin analysis.")

# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.markdown("### 🧭 Navigation")

    nav_items = [
        ("📊 Dashboard", "Dashboard"),
        ("📊 Progress", "Progress"),
        ("📄 Resume Review", "Resume"),
        ("🚀 Advanced Analysis", "Advanced"),
        ("🎤 Interview", "Interview"),
        ("🎯 Job Match", "JobMatch"),
        ("✍️ Rewriter", "Rewriter"),
        ("💰 Salary Guide", "Salary"),
        ("📈 Career Advisor", "Learning")
    ]

    for label, key in nav_items:
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown("### 👤 Profile")

    # Display user info
    user_email = st.session_state.get("email", "Guest")
    user_display = "👤 Guest" if st.session_state.get("is_guest") else f"👤 {user_email.split('@')[0]}"

    st.markdown(f"""
        <div style="background-color: #1F2937; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 1.2rem; margin-bottom: 8px;">{user_display}</div>
            <div style="font-size: 0.75rem; color: #9CA3AF;">{user_email}</div>
        </div>
    """, unsafe_allow_html=True)

    # Logout button
    if st.button("🚪 Logout", use_container_width=True, key="sidebar_logout"):
        from utils.auth import logout_user
        logout_user()
        st.rerun()

# ===== STEP 3: OPEN MAIN WRAPPER =====
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# ===== STEP 4: PAGE ROUTING =====
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Progress":
    show_progress_dashboard()
elif st.session_state.page == "Resume":
    show_resume_review()
elif st.session_state.page == "Advanced":
    show_advanced_analysis()
elif st.session_state.page == "Interview":
    show_interview()
elif st.session_state.page == "JobMatch":
    show_job_match()
elif st.session_state.page == "Rewriter":
    show_rewriter()
elif st.session_state.page == "Learning":
    show_learning()
elif st.session_state.page == "Salary":
    show_salary_guide()

# ===== STEP 5: CLOSE MAIN WRAPPER =====
st.markdown('</div>', unsafe_allow_html=True)
