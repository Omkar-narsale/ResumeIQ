"""
Career Coaching Features Module
Job matching, resume rewriting, interview prep, and career guidance
"""

from utils.llm_handler import get_llm_handler


def match_job_description(resume_text: str, job_description: str) -> dict:
    """
    Compare resume against job description and provide match score

    Args:
        resume_text: Full resume text
        job_description: Job posting text

    Returns:
        Dictionary with match_score, matched_skills, missing_skills, suggestions
    """
    llm = get_llm_handler()

    prompt = f"""Analyze how well this resume matches the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide analysis in this exact format:
MATCH_SCORE: [0-100]
MATCHED_SKILLS: [comma-separated skills found in both]
MISSING_SKILLS: [comma-separated skills required but missing from resume]
SUGGESTIONS: [specific steps to improve match]"""

    system_prompt = "You are an expert recruiter. Analyze resume-job fit accurately and provide actionable suggestions."

    response = llm.ask_claude(prompt, system_prompt)
    return parse_match_response(response)


def rewrite_resume(resume_text: str, target_role: str = None) -> str:
    """
    Rewrite resume professionally

    Args:
        resume_text: Original resume text
        target_role: Optional target role to tailor towards

    Returns:
        Professionally rewritten resume
    """
    llm = get_llm_handler()

    role_context = f"for a {target_role} position" if target_role else "for better impact"

    prompt = f"""Professionally rewrite this resume {role_context}.

ORIGINAL RESUME:
{resume_text}

Rewrite it with:
- Stronger action verbs
- Quantified achievements
- Better formatting
- Professional language
- Optimized for ATS

Return ONLY the rewritten resume, no explanations."""

    system_prompt = "You are a professional resume writer. Rewrite resumes to maximize impact and ATS compatibility."

    return llm.ask_claude(prompt, system_prompt)


def generate_personalized_questions(resume_text: str, job_role: str, num_questions: int = 3) -> list:
    """
    Generate interview questions based on resume and job role

    Args:
        resume_text: Resume content
        job_role: Target job role
        num_questions: Number of questions to generate

    Returns:
        List of personalized interview questions
    """
    llm = get_llm_handler()

    prompt = f"""Generate {num_questions} personalized interview questions based on this resume and target role.

RESUME:
{resume_text}

TARGET ROLE: {job_role}

Generate questions that:
1. Relate to their actual experience from the resume
2. Are specific to the {job_role} role
3. Are challenging but fair
4. Don't repeat common generic questions

Format as numbered list:
1. [Question 1]
2. [Question 2]
3. [Question 3]"""

    system_prompt = "You are an expert technical interviewer. Generate insightful, personalized questions based on candidate's actual experience."

    response = llm.ask_claude(prompt, system_prompt)
    return parse_questions_response(response)


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

    role_focus = ""
    if target_role:
        role_lower = target_role.lower()
        if "data analyst" in role_lower:
            role_focus = """
ROLE AWARENESS - Data Analyst:
Focus on: SQL, Python, Data visualization, Statistics, Excel, Power BI
Avoid: System design, Backend architecture, DevOps"""
        elif "software engineer" in role_lower or "backend" in role_lower:
            role_focus = """
ROLE AWARENESS - Software Engineer:
Focus on: DSA, Projects, System design, APIs, Backend systems
Avoid: Statistics, Data visualization tools"""
        elif "frontend" in role_lower:
            role_focus = """
ROLE AWARENESS - Frontend Developer:
Focus on: React/Vue, JavaScript, CSS, UI/UX, Performance
Avoid: Database design, System architecture"""
        elif "ml engineer" in role_lower or "machine learning" in role_lower:
            role_focus = """
ROLE AWARENESS - ML Engineer:
Focus on: Machine Learning, Deep Learning, Python, TensorFlow, Mathematics
Avoid: Frontend development, DevOps infrastructure"""
        elif "devops" in role_lower:
            role_focus = """
ROLE AWARENESS - DevOps Engineer:
Focus on: Docker, Kubernetes, CI/CD, AWS/GCP, Infrastructure
Avoid: Frontend development, UI/UX"""

    prompt = f"""You are an expert resume evaluator.

Analyze the given resume and provide a structured evaluation.

RESUME:
{resume_text}

TARGET ROLE: {target_role if target_role else 'General Professional'}{role_focus}

IMPORTANT RULES (STRICT):
1. Output MUST be plain text ONLY
2. DO NOT use HTML tags
3. DO NOT return empty sections
4. If information is missing, provide reasonable assumption
5. Keep output structured and clean
6. DO NOT return code or markdown blocks
7. Maximum 150-200 words total

OUTPUT FORMAT (FOLLOW EXACTLY):

Score: X/10

Strengths:
* Point 1
* Point 2
* Point 3

Weaknesses:
* Point 1
* Point 2
* Point 3

Suggestions:
* Improvement 1
* Improvement 2
* Improvement 3"""

    system_prompt = "You are an expert resume reviewer. Provide SPECIFIC, CONCRETE feedback based ONLY on the resume content. Be honest but constructive. Output PLAIN TEXT ONLY - no HTML tags. Follow the format exactly."

    response = llm.ask_claude(prompt, system_prompt)
    return parse_resume_analysis(response)


def generate_career_roadmap(target_role: str, resume_text: str = None) -> dict:
    """
    Generate ROLE-AWARE learning roadmap with personalized skill gaps

    Args:
        target_role: Desired career position (Data Analyst, Software Engineer, ML Engineer, etc)
        resume_text: Optional current resume for comparison

    Returns:
        Dictionary with missing_skills, roadmap, focus_areas, timeline
    """
    llm = get_llm_handler()

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
            "avoid": "CSS, UI frameworks"
        },
        "devops engineer": {
            "primary": "Docker, Kubernetes, CI/CD, AWS/GCP, Infrastructure, Networking, Monitoring",
            "avoid": "Frontend, Graphics"
        }
    }

    # Get role-specific guidance or use default
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


# ======================== PARSING HELPERS ========================

def parse_match_response(response: str) -> dict:
    """Parse job match analysis response"""
    result = {
        "match_score": "0",
        "matched_skills": "",
        "missing_skills": "",
        "suggestions": ""
    }

    lines = response.split("\n")
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith("MATCH_SCORE:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            result["match_score"] = line.replace("MATCH_SCORE:", "").strip().split("/")[0]
            current_section = None
            current_content = []
        elif line.startswith("MATCHED_SKILLS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "matched_skills"
            current_content = [line.replace("MATCHED_SKILLS:", "").strip()]
        elif line.startswith("MISSING_SKILLS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "missing_skills"
            current_content = [line.replace("MISSING_SKILLS:", "").strip()]
        elif line.startswith("SUGGESTIONS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "suggestions"
            current_content = [line.replace("SUGGESTIONS:", "").strip()]
        elif current_section and line.strip():
            current_content.append(line)

    if current_section and current_content:
        result[current_section] = "\n".join(current_content).strip()

    return result


def parse_questions_response(response: str) -> list:
    """Parse numbered questions from response"""
    questions = []
    lines = response.split("\n")

    for line in lines:
        line = line.strip()
        if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
            # Remove number prefix
            question = line.split(".", 1)[1].strip()
            if question:
                questions.append(question)

    return questions


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


def parse_roadmap_response(response: str) -> dict:
    """Parse career roadmap response"""
    result = {
        "missing_skills": "",
        "roadmap": "",
        "focus_areas": "",
        "timeline": "",
        "next_actions": ""
    }

    lines = response.split("\n")
    current_section = None
    current_content = []

    for line in lines:
        line_upper = line.upper()

        if line_upper.startswith("MISSING_SKILLS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "missing_skills"
            current_content = [line.replace("MISSING_SKILLS:", "").replace("Missing_Skills:", "").strip()]
        elif line_upper.startswith("LEARNING_ROADMAP:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "roadmap"
            current_content = [line.replace("LEARNING_ROADMAP:", "").replace("Learning_Roadmap:", "").strip()]
        elif line_upper.startswith("FOCUS_AREAS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "focus_areas"
            current_content = [line.replace("FOCUS_AREAS:", "").replace("Focus_Areas:", "").strip()]
        elif line_upper.startswith("TIMELINE:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "timeline"
            current_content = [line.replace("TIMELINE:", "").replace("Timeline:", "").strip()]
        elif line_upper.startswith("NEXT_ACTIONS:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "next_actions"
            current_content = [line.replace("NEXT_ACTIONS:", "").replace("Next_Actions:", "").strip()]
        elif current_section and line.strip():
            current_content.append(line)

    if current_section and current_content:
        result[current_section] = "\n".join(current_content).strip()

    return result
