# Code Changes - Before & After

## 1. Resume Analyzer - Complete Overhaul

### ❌ BEFORE (Broken - Random Scores)
```python
# app.py - show_resume_review()
if st.button("🔍 Analyze Resume"):
    # Generate FAKE scores based on file size
    import random
    file_size = uploaded_file.size
    base_score = 80 + (file_size % 15)
    overall_score = min(100, base_score + random.randint(-5, 10))
    ats_score = min(100, overall_score - random.randint(0, 5))
    keyword_score = min(100, overall_score - random.randint(5, 15))
    
    # Display HARDCODED strengths (same for all resumes)
    st.markdown("""
        <div class="card">
            <div class="skills-header">✓ Strengths</div>
            <div>
                • Clear structure & formatting
                • Strong action verbs
                • Quantified achievements
                • Relevant skills highlighted
                • Professional summary
            </div>
        </div>
    """)
    
    # Display HARDCODED weaknesses (same for all resumes)
    st.markdown("""
        <div class="card">
            <div class="skills-header">⚠️ Areas to Improve</div>
            <div>
                • Add more metrics to achievements
                • Expand technical skills section
                • Include certifications
                • Add specific project results
                • Strengthen impact statements
            </div>
        </div>
    """)
```

### ✅ AFTER (AI-Powered - Real Analysis)
```python
# app.py - show_resume_review()
if st.button("🔍 Analyze Resume"):
    try:
        # Extract ACTUAL text from PDF
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Get target role if available
        target_role = st.session_state.get("target_role_analysis", None)
        
        # Analyze using AI (NOT random)
        with st.spinner("🤖 Analyzing your resume..."):
            analysis = analyze_resume(resume_text, target_role)
        
        # Store real analysis results
        st.session_state.resume_analysis = {
            "score": analysis.get("score", "0/10"),
            "strengths": analysis.get("strengths", ""),
            "weaknesses": analysis.get("weaknesses", ""),
            "suggestions": analysis.get("suggestions", ""),
            "file_name": uploaded_file.name
        }
        
        # Display ACTUAL score from AI
        score_text = analysis.get("score", "0/10")
        score_num = int(score_text.split("/")[0]) if "/" in score_text else 0
        st.markdown(f"""
            <div class="card hero-card">
                <div class="card-title">Overall Score</div>
                <div class="card-value">{score_num}</div>
                <div class="card-desc">/10 - {'Excellent' if score_num >= 8 else 'Good' if score_num >= 6 else 'Needs Work'}</div>
            </div>
        """)
        
        # Display AI-analyzed STRENGTHS (unique per resume)
        strengths = analysis.get("strengths", "").split("\n")
        strengths_html = "<br>".join([s.strip() for s in strengths if s.strip()])
        st.markdown(f"""
            <div class="card">
                <div class="skills-header">✓ Strengths</div>
                <div>{strengths_html}</div>
            </div>
        """)
        
        # Display AI-analyzed WEAKNESSES (unique per resume)
        weaknesses = analysis.get("weaknesses", "").split("\n")
        weaknesses_html = "<br>".join([w.strip() for w in weaknesses if w.strip()])
        st.markdown(f"""
            <div class="card">
                <div class="skills-header">⚠️ Areas to Improve</div>
                <div>{weaknesses_html}</div>
            </div>
        """)
        
        # Display AI-generated SUGGESTIONS
        suggestions = analysis.get("suggestions", "").split("\n")
        suggestions_text = "<br>".join([s.strip() for s in suggestions if s.strip()])
        st.markdown(f"""
            <div class="card">
                <div>💡 Recommendations</div>
                <div>{suggestions_text}</div>
            </div>
        """)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
```

---

## 2. New Function: analyze_resume()

### ✅ NEW in features.py
```python
def analyze_resume(resume_text: str, target_role: str = None) -> dict:
    """
    Analyze resume and return structured feedback with score, strengths, weaknesses, suggestions
    
    Args:
        resume_text: Resume content
        target_role: Optional target role for role-specific analysis
    
    Returns:
        Dictionary with score, strengths, weaknesses, suggestions
    """
    llm = get_llm_handler()
    
    role_context = f"for a {target_role} role" if target_role else "in general"
    
    prompt = f"""Analyze this resume {role_context}. Provide structured feedback.

RESUME:
{resume_text}

Return in this EXACT format (max 150-200 words total):

SCORE: [X/10]

STRENGTHS:
• [Strength 1 - specific to resume content]
• [Strength 2 - specific to resume content]
• [Strength 3 - specific to resume content]

WEAKNESSES:
• [Weakness 1 - specific area to improve]
• [Weakness 2 - specific area to improve]
• [Weakness 3 - specific area to improve]

SUGGESTIONS:
• [Actionable improvement 1]
• [Actionable improvement 2]
• [Actionable improvement 3]"""
    
    system_prompt = f"You are an expert resume reviewer. Provide SPECIFIC, CONCRETE feedback based ONLY on the resume content. Be honest but constructive. {'Focus on ' + target_role + ' requirements.' if target_role else 'Focus on general best practices.'}"
    
    response = llm.ask_claude(prompt, system_prompt)
    return parse_resume_analysis(response)
```

### ✅ NEW Parser in features.py
```python
def parse_resume_analysis(response: str) -> dict:
    """Parse resume analysis response into structured format"""
    result = {
        "score": "0/10",
        "strengths": "",
        "weaknesses": "",
        "suggestions": ""
    }
    
    lines = response.split("\n")
    current_section = None
    current_content = []
    
    for line in lines:
        line_upper = line.upper()
        
        if line_upper.startswith("SCORE:"):
            result["score"] = line.replace("SCORE:", "").replace("Score:", "").strip()
            current_section = None
        elif line_upper.startswith("STRENGTHS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "strengths"
            current_content = []
        elif line_upper.startswith("WEAKNESSES:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "weaknesses"
            current_content = []
        elif line_upper.startswith("SUGGESTIONS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "suggestions"
            current_content = []
        elif current_section and line.strip():
            current_content.append(line.strip())
    
    if current_section and current_content:
        result[current_section] = "\n".join(current_content).strip()
    
    return result
```

---

## 3. Career Roadmap - Role-Awareness Added

### ❌ BEFORE (Generic for All Roles)
```python
# features.py - generate_career_roadmap()
def generate_career_roadmap(target_role: str, resume_text: str = None) -> dict:
    prompt = f"""Create a career development roadmap for someone targeting a {target_role} position.

Provide in this exact format:
MISSING_SKILLS:
[List top 5-7 critical skills needed]

LEARNING_ROADMAP:
Phase 1 - Foundations (Month 1-2):
[Specific steps with resources]
...
"""
    # No role-specific guidance
    # Gives same skills for Data Analyst and Software Engineer
```

### ✅ AFTER (Role-Specific)
```python
# features.py - generate_career_roadmap() - ENHANCED
def generate_career_roadmap(target_role: str, resume_text: str = None) -> dict:
    # Role-specific skill guidelines
    role_skills = {
        "data analyst": {
            "primary": "Python, SQL, Excel, Data Visualization, Statistics, Power BI, Tableau",
            "avoid": "System Design, Kubernetes, Docker (unless data engineering focus)"
        },
        "software engineer": {
            "primary": "DSA, System Design, APIs, Backend/Frontend, Git, Testing",
            "avoid": "Statistics, Deep Learning (unless ML-focused)"
        },
        "ml engineer": {
            "primary": "Machine Learning, Deep Learning, Python, TensorFlow, Mathematics, Statistics",
            "avoid": "DevOps, Frontend development (unless relevant)"
        },
        "frontend developer": {
            "primary": "React/Vue, JavaScript/TypeScript, CSS, UI/UX, Testing, Performance",
            "avoid": "Database design, System Design (in depth)"
        },
        "backend developer": {
            "primary": "Database design, APIs, System Design, Authentication, Scaling, Testing",
            "avoid": "Frontend, Graphics"
        },
        "devops engineer": {
            "primary": "Docker, Kubernetes, CI/CD, AWS/GCP, Infrastructure, Networking, Monitoring",
            "avoid": "Frontend, Graphics"
        }
    }
    
    # Get role-specific guidance
    role_lower = target_role.lower()
    role_key = next((k for k in role_skills if k in role_lower), "software engineer")
    skill_guide = role_skills[role_key]
    
    context = ""
    if resume_text:
        context = f"\n\nCURRENT EXPERIENCE:\n{resume_text}\n\nREVIEW: Extract existing skills and avoid suggesting duplicates."
    
    prompt = f"""Create a ROLE-SPECIFIC {target_role} career roadmap.{context}

PRIMARY FOCUS AREAS (prioritize these): {skill_guide['primary']}
AVOID SUGGESTING: {skill_guide['avoid']}

Provide in this exact format:

MISSING_SKILLS:
[List 3-5 role-specific critical skills needed for {target_role}]

LEARNING_ROADMAP:
Month 1-2 (Foundation):
[2-3 specific, achievable steps for {target_role}]

Month 3-4 (Intermediate):
[2-3 intermediate steps]

Month 5-6 (Advanced):
[2-3 advanced steps]

FOCUS_AREAS:
[Top 2-3 priority areas that matter most for {target_role}]

TIMELINE: [realistic timeline]

NEXT_ACTIONS:
[2-3 immediate actionable steps to start today]"""
    
    system_prompt = f"You are a career coach specializing in {target_role} positions. Provide personalized, role-specific roadmaps. DO NOT suggest generic skills. Focus on what matters for {target_role}."
    
    response = llm.ask_claude(prompt, system_prompt)
    return parse_roadmap_response(response)
```

---

## 4. Career Advisor - Resume Integration

### ❌ BEFORE (No Resume Integration)
```python
# app.py - show_career_advisor()
target_role = st.text_input("Enter your target role", placeholder="...")

if st.button("🎯 Generate Learning Path"):
    if target_role:
        # Just shows hardcoded paths
        # No AI analysis, no resume context
        st.markdown(hardcoded_learning_path_html)
```

### ✅ AFTER (Resume + AI Integration)
```python
# app.py - show_career_advisor() - ENHANCED
target_role = st.text_input("Enter your target role", placeholder="...")

# NEW: Optional resume upload for personalization
st.markdown("---")
st.markdown("**Optional:** Upload your resume for AI-powered personalized recommendations")
resume_file = st.file_uploader("Choose PDF resume (optional)", type="pdf", key="career_advisor_resume")

if st.button("🎯 Generate Learning Path"):
    if target_role:
        # NEW: Extract resume if provided
        resume_text = None
        if resume_file:
            try:
                resume_text = extract_text_from_pdf(resume_file)
            except:
                st.warning("Could not extract resume text...")
        
        # NEW: AI-powered analysis if resume provided
        if resume_text:
            st.markdown('<h2>🤖 AI-Powered Personalized Roadmap</h2>')
            with st.spinner("Generating personalized roadmap..."):
                try:
                    roadmap = generate_career_roadmap(target_role, resume_text)
                    
                    # Display AI results
                    st.markdown('<h3>📋 Skills to Develop</h3>')
                    st.markdown(roadmap.get("missing_skills", "").replace("\n", "<br>"))
                    
                    st.markdown('<h3>📚 Learning Roadmap</h3>')
                    st.markdown(roadmap.get("roadmap", ""))
                    
                    st.markdown('<h3>🎯 Focus Areas</h3>')
                    st.markdown(roadmap.get("focus_areas", "").replace("\n", "<br>"))
                    
                    st.markdown('<h3>✅ Next Actions</h3>')
                    st.markdown(roadmap.get("next_actions", "").replace("\n", "<br>"))
                    
                    st.success("✅ AI-powered roadmap generated!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Still show standard paths as fallback
        st.markdown('<h2>Structured Learning Paths</h2>')
        # ... existing hardcoded paths ...
```

---

## 5. Imports Updates

### ❌ BEFORE
```python
# app.py
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
```

### ✅ AFTER
```python
# app.py
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.features import analyze_resume, generate_career_roadmap
from utils.resume_parser import extract_text_from_pdf

load_dotenv()
```

---

## Summary of Changes

| Feature | Before | After |
|---------|--------|-------|
| **Resume Score** | Random (80-95) | AI-generated (unique per resume) |
| **Strengths** | Hardcoded (same for all) | AI-analyzed (based on actual resume) |
| **Weaknesses** | Hardcoded (same for all) | AI-identified (unique per resume) |
| **Suggestions** | Hardcoded (same for all) | AI-generated (actionable & specific) |
| **Career Path - Data Analyst** | System Design, DSA, AWS | SQL, Python, Power BI, Statistics |
| **Career Path - ML Engineer** | DSA, System Design, AWS | ML, Deep Learning, TensorFlow, Math |
| **Career Path - Backend Dev** | Generic skills | Database design, APIs, System Design |
| **Resume Integration** | None | Optional upload for personalization |
| **AI Personalization** | None | Role-aware skill recommendations |
| **Output Length** | Varies | 150-200 words (concise) |

---

## Testing Commands

```bash
# Check syntax
python -m py_compile app.py utils/features.py

# Run app
streamlit run app.py

# Test resume analysis
# 1. Go to Resume Review
# 2. Upload PDF
# 3. Click Analyze
# Expected: Real analysis, not random scores

# Test career path
# 1. Go to Career Advisor
# 2. Enter "Data Analyst"
# 3. Click Generate
# Expected: SQL, Python, Power BI (NOT System Design)

# Test with resume
# 1. Go to Career Advisor
# 2. Enter "Backend Developer"
# 3. Upload resume
# 4. Click Generate
# Expected: Personalized roadmap based on current skills
```
