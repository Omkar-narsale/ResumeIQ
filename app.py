"""
ResumeIQ - Professional SaaS Dashboard
PERMANENT FIX: Zero top spacing
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.features import analyze_resume, generate_career_roadmap
from utils.resume_parser import extract_text

load_dotenv()

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

# ===== PAGE FUNCTIONS =====

def show_dashboard():
    st.markdown('<h1>Dashboard Overview</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        score_text = st.session_state.resume_analysis.get('score', '0/10')
        score_num = int(score_text.split("/")[0]) if "/" in score_text else 0
        st.markdown(f"""
            <div class="card hero-card">
                <div class="card-title">Resume Score</div>
                <div class="card-value">{score_num}</div>
                <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        file_name = st.session_state.resume_analysis.get('file_name', 'No resume uploaded')
        st.markdown(f"""
            <div class="card">
                <div class="card-title">Latest Resume</div>
                <div class="card-value" style="font-size: 0.9rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{file_name}</div>
                <div class="card-desc">Last analyzed</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    st.markdown('<h2>Key Metrics</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-title">Resume Score</div>
                <div class="card-value">92</div>
                <div class="card-desc">+5 from last review</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-title">Job Match</div>
                <div class="card-value">87%</div>
                <div class="card-desc">8 positions matched</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <div class="card-title">Interview Score</div>
                <div class="card-value">85</div>
                <div class="card-desc">Last session: Good</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    st.markdown('<h2>Performance Trends</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-title">Applications</div>
                <div class="card-value">24</div>
                <div class="card-desc">+8 this month</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-title">Interviews</div>
                <div class="card-value">12</div>
                <div class="card-desc">+4 this month</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <div class="card-title">Offers</div>
                <div class="card-value">3</div>
                <div class="card-desc">+1 this month</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="card">
                <div class="card-title">Success Rate</div>
                <div class="card-value">25%</div>
                <div class="card-desc">↑ 5% trending</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

    st.markdown('<h2>Recent Activity</h2>', unsafe_allow_html=True)

    score_text = st.session_state.resume_analysis.get('score', '0/10')
    activities = [
        (f"Resume uploaded: {st.session_state.resume_analysis.get('file_name', 'No resume')}", f"Analysis score: {score_text}", "Just now"),
        ("Resume evaluated", "Get detailed feedback on strengths and weaknesses", "Latest"),
        ("Job match completed", "Compare your resume against job descriptions", "Available"),
        ("Interview practice", "Practice with AI-generated interview questions", "Ready"),
    ]

    for title, desc, time in activities:
        st.markdown(f"""
            <div class="card" style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-weight: 600; color: #ffffff; margin-bottom: 4px;">{title}</div>
                        <div style="font-size: 0.9rem; color: #9CA3AF;">{desc}</div>
                    </div>
                    <div style="font-size: 0.85rem; color: #6B7280;">{time}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

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
                st.session_state.resume_analysis = {
                    "score": analysis.get("score", "0/10"),
                    "strengths": analysis.get("strengths", ""),
                    "weaknesses": analysis.get("weaknesses", ""),
                    "suggestions": analysis.get("suggestions", ""),
                    "file_name": uploaded_file.name
                }

                st.markdown('<h2>📊 Resume Analysis Report</h2>', unsafe_allow_html=True)

                # Score Card
                score_text = analysis.get("score", "0/10")
                score_num = int(score_text.split("/")[0]) if "/" in score_text else 0

                st.markdown(f"""
                    <div class="card hero-card">
                        <div class="card-title">Overall Score</div>
                        <div class="card-value">{score_num}</div>
                        <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)

                # Strengths & Weaknesses
                col1, col2 = st.columns(2, gap="medium")

                with col1:
                    strengths = analysis.get("strengths", "").split("\n")
                    strengths_html = "<br>".join([s.strip() for s in strengths if s.strip()])
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
                    weaknesses = analysis.get("weaknesses", "").split("\n")
                    weaknesses_html = "<br>".join([w.strip() for w in weaknesses if w.strip()])
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
                suggestions = analysis.get("suggestions", "").split("\n")
                suggestions_text = "<br>".join([s.strip() for s in suggestions if s.strip()])
                st.markdown(f"""
                    <div class="card">
                        <div style="color: #D1D5DB; line-height: 1.8;">
                            {suggestions_text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

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
                with st.spinner("Generating personalized roadmap based on your resume..."):
                    try:
                        roadmap = generate_career_roadmap(target_role, resume_text)

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

# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.markdown("### 🧭 Navigation")

    nav_items = [
        ("📊 Dashboard", "Dashboard"),
        ("📄 Resume Review", "Resume"),
        ("🎤 Interview", "Interview"),
        ("🎯 Job Match", "JobMatch"),
        ("✍️ Rewriter", "Rewriter"),
        ("📈 Learning", "Learning")
    ]

    for label, key in nav_items:
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown("### 👤 Profile")
    st.markdown("""
        <div style="background-color: #1F2937; padding: 12px; border-radius: 8px; text-align: center;">
            <div style="font-size: 1.5rem; color: #7C3AED; margin-bottom: 8px;">●</div>
            <div style="font-weight: 600; color: #ffffff;">Omkar</div>
            <div style="font-size: 0.85rem; color: #9CA3AF;">Premium Plan</div>
            <div style="font-size: 0.75rem; color: #6B7280; margin-top: 4px;">Active • Pro Member</div>
        </div>
    """, unsafe_allow_html=True)

# ===== STEP 3: OPEN MAIN WRAPPER =====
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# ===== STEP 4: PAGE ROUTING =====
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Resume":
    show_resume_review()
elif st.session_state.page == "Interview":
    show_interview()
elif st.session_state.page == "JobMatch":
    show_job_match()
elif st.session_state.page == "Rewriter":
    show_rewriter()
elif st.session_state.page == "Learning":
    show_learning()

# ===== STEP 5: CLOSE MAIN WRAPPER =====
st.markdown('</div>', unsafe_allow_html=True)
