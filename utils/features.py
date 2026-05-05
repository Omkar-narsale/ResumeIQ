"""
Career Coaching Features Module
Job matching, resume rewriting, interview prep, and career guidance
"""

from utils.llm_handler import get_llm_handler
from utils.local_analyzer import analyze_resume_locally


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
    """Analyze resume using local text analysis (no LLM)"""

    # Use local analyzer instead of LLM
    result = analyze_resume_locally(resume_text, target_role)

    # Define priority skills by role
    role_priority = {
        "data analyst": ["SQL", "Python", "Excel", "Power BI", "Statistics"],
        "software engineer": ["Python", "Java", "System Design", "DSA", "Git"],
        "ml engineer": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Statistics"],
        "frontend developer": ["React", "JavaScript", "CSS", "HTML", "UI/UX"],
        "backend developer": ["Python", "Java", "SQL", "API", "Database Design"],
        "devops engineer": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
    }

    # Get priority skills for role
    priority_skills = []
    role_lower = target_role.lower() if target_role else "general"
    for key in role_priority:
        if key in role_lower:
            priority_skills = role_priority[key]
            break

    if not priority_skills:
        priority_skills = ["Communication", "Problem Solving", "Teamwork", "Time Management"]

    # Extract strengths/weaknesses as lists
    strengths_list = result["strengths"].split("\n") if result["strengths"] else []
    weaknesses_list = result["weaknesses"].split("\n") if result["weaknesses"] else []
    suggestions_list = result["suggestions"].split("\n") if result["suggestions"] else []

    # Create learning roadmap
    roadmap_beginner = suggestions_list[0] if suggestions_list else "Start with fundamentals"
    roadmap_intermediate = f"Master the top {len(priority_skills)} skills for {target_role or 'your role'}"
    roadmap_advanced = "Lead projects and mentor others"

    return {
        "score": result["score"],
        "strengths": result["strengths"],
        "weaknesses": result["weaknesses"],
        "suggestions": result["suggestions"],
        "matched_skills": strengths_list[:3],
        "missing_skills": weaknesses_list[:3],
        "priority_skills": priority_skills[:3],
        "learning_roadmap": {
            "beginner": roadmap_beginner,
            "intermediate": roadmap_intermediate,
            "advanced": roadmap_advanced
        }
    }


def generate_generic_roadmap(target_role: str, resume_text: str = None) -> dict:
    """
    Generate roadmap for roles not in the predefined map
    Uses resume skills to determine learning path
    """
    import re

    # Generic skill categories
    generic_skills = {
        "technical": ["SQL", "Python", "JavaScript", "APIs", "Databases", "Git"],
        "business": ["Communication", "Project Management", "Leadership", "Strategy", "Analytics"],
        "creative": ["Design", "Content", "Copywriting", "Storytelling", "Visual Communication"],
        "data": ["Excel", "Python", "SQL", "Data Analysis", "Statistics", "Tableau"]
    }

    detected_skills = []
    if resume_text:
        text_lower = resume_text.lower()
        for skill_set in generic_skills.values():
            for skill in skill_set:
                if skill.lower() in text_lower:
                    detected_skills.append(skill)

    strong_skills_text = ", ".join(list(dict.fromkeys(detected_skills))[:5]) if detected_skills else "Analyze your resume to discover skills"

    return {
        "strong_skills": strong_skills_text,
        "missing_skills": "Review role requirements and identify skill gaps",
        "roadmap": f"""MONTH 1-2 (Foundation):
• Research {target_role} role requirements and responsibilities
• Identify key skills needed for {target_role}

MONTH 3-4 (Development):
• Build foundational skills in priority areas
• Complete relevant courses or certifications

MONTH 5-6 (Advanced):
• Create projects demonstrating {target_role} capabilities
• Network with professionals in {target_role} field""",
        "focus_areas": f"• Understanding {target_role} responsibilities\n• Identifying transferable skills\n• Building relevant experience",
        "next_actions": f"• Research job descriptions for {target_role}\n• Identify required skills from job postings\n• Create action plan based on skill gaps",
        "timeline": "6 months to transition or advancement"
    }


def generate_career_roadmap_fast(target_role: str, resume_text: str = None) -> dict:
    """
    Generate FAST role-specific learning roadmap without LLM (local analysis only)

    Args:
        target_role: Desired career position
        resume_text: Optional resume text for skill analysis

    Returns:
        Dictionary with roadmap, missing_skills, focus_areas, next_actions
    """
    from utils.local_analyzer import analyze_resume_locally
    import re

    role_lower = target_role.lower()

    # Role-specific skill mappings
    role_skills_map = {
        "data analyst": {
            "required": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Statistics", "Data Visualization", "Pandas", "R"],
            "focus": "SQL, Python, Excel, Power BI, Statistics",
            "month1": ["Learn SQL joins and window functions", "Master Excel pivot tables and VLOOKUP"],
            "month2": ["Python pandas for data manipulation", "Create Power BI dashboards"],
            "month3": ["Statistical analysis", "Tableau visualization"]
        },
        "software engineer": {
            "required": ["Python", "Java", "JavaScript", "C++", "System Design", "DSA", "Git", "Docker", "SQL"],
            "focus": "DSA, System Design, APIs, Database, Git",
            "month1": ["Master data structures and algorithms", "Learn Git workflows"],
            "month2": ["Build REST APIs", "Database design basics"],
            "month3": ["System design principles", "Code review skills"]
        },
        "ml engineer": {
            "required": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "Statistics", "SQL", "Deep Learning"],
            "focus": "Python, Machine Learning, Deep Learning, MLOps",
            "month1": ["Advanced Python and NumPy", "Scikit-learn machine learning"],
            "month2": ["Deep learning with PyTorch or TensorFlow", "Model evaluation"],
            "month3": ["MLOps and model deployment", "A/B testing"]
        },
        "frontend developer": {
            "required": ["React", "JavaScript", "TypeScript", "CSS", "HTML", "UI/UX", "Jest", "Redux", "Git"],
            "focus": "React, JavaScript, CSS, UI/UX, Testing",
            "month1": ["React hooks and component design", "JavaScript ES6+ features"],
            "month2": ["CSS Grid and Flexbox mastery", "Redux or state management"],
            "month3": ["Testing frameworks (Jest, React Testing)", "Performance optimization"]
        },
        "backend developer": {
            "required": ["Python", "Java", "Node.js", "SQL", "APIs", "Database", "Docker", "Git", "Authentication"],
            "focus": "APIs, Databases, System Design, Authentication",
            "month1": ["RESTful API design", "SQL optimization"],
            "month2": ["Database indexing and scaling", "Authentication & security"],
            "month3": ["Microservices patterns", "Message queues"]
        },
        "devops engineer": {
            "required": ["Docker", "Kubernetes", "AWS", "Linux", "Git", "CI/CD", "Jenkins", "Terraform", "Monitoring"],
            "focus": "Docker, Kubernetes, CI/CD, AWS, Linux",
            "month1": ["Docker containers and images", "Kubernetes basics"],
            "month2": ["CI/CD pipelines (GitHub Actions, Jenkins)", "AWS services"],
            "month3": ["Infrastructure as code (Terraform)", "Monitoring and logging"]
        },
        "digital marketing": {
            "required": ["SEO", "SEM", "Google Analytics", "Content Marketing", "Social Media", "Email Marketing", "Marketing Automation", "Data Analysis", "CRM"],
            "focus": "SEO, Google Analytics, Social Media, Content Strategy",
            "month1": ["Master Google Analytics fundamentals", "Learn SEO best practices"],
            "month2": ["Social media strategy and campaigns", "Email marketing automation"],
            "month3": ["Data-driven marketing analysis", "Campaign optimization techniques"]
        },
        "product manager": {
            "required": ["Product Strategy", "User Research", "Data Analysis", "Roadmapping", "Stakeholder Management", "Design Thinking", "SQL", "Metrics"],
            "focus": "Product Strategy, User Research, Data Analysis, Roadmapping",
            "month1": ["User research and discovery methods", "Product thinking fundamentals"],
            "month2": ["OKR framework and metrics", "Roadmapping techniques"],
            "month3": ["Data-driven decision making", "Stakeholder management"]
        },
        "ux designer": {
            "required": ["Figma", "User Research", "Prototyping", "Wireframing", "Design Systems", "CSS", "JavaScript", "User Testing", "Accessibility"],
            "focus": "Figma, User Research, Prototyping, Design Systems",
            "month1": ["Master Figma tools and workflows", "Learn design systems basics"],
            "month2": ["User research and testing methods", "Create interactive prototypes"],
            "month3": ["Design accessibility standards", "Build design systems"]
        },
        "data scientist": {
            "required": ["Python", "Machine Learning", "Statistics", "SQL", "Data Visualization", "TensorFlow", "scikit-learn", "Pandas", "Deep Learning"],
            "focus": "Python, Machine Learning, Statistics, Data Visualization",
            "month1": ["Advanced Python for data science", "Statistics and probability"],
            "month2": ["Machine learning algorithms and scikit-learn", "Data visualization techniques"],
            "month3": ["Deep learning and neural networks", "Production ML deployment"]
        }
    }

    # Find matching role
    matched_role = None
    for key in role_skills_map:
        if key in role_lower:
            matched_role = key
            break

    if not matched_role:
        # Create generic roadmap for unknown roles based on resume skills
        return generate_generic_roadmap(target_role, resume_text)

    role_data = role_skills_map[matched_role]
    required_skills = role_data["required"]

    # Extract actual skills from resume
    detected_skills = []
    missing_skills = list(required_skills)  # Start with all required

    if resume_text:
        # Extract skills using regex patterns
        skill_patterns = {
            "SQL": r"\bsql\b",
            "Python": r"\bpython\b",
            "Java": r"\bjava\b",
            "JavaScript": r"\bjavascript|js\b",
            "TypeScript": r"\btypescript\b",
            "React": r"\breact\b",
            "Vue": r"\bvue\b",
            "Angular": r"\bangular\b",
            "Node.js": r"\bnode\.?js\b",
            "Express": r"\bexpress\b",
            "Django": r"\bdjango\b",
            "Flask": r"\bflask\b",
            "C++": r"\bc\+\+|cpp\b",
            "C#": r"\bc#|csharp\b",
            "R": r"\br\b",
            "Excel": r"\bexcel\b",
            "Power BI": r"\bpower\s?bi\b",
            "Tableau": r"\btableau\b",
            "Statistics": r"\bstatistics|statistical\b",
            "Data Visualization": r"\bdata\s?visualization|visualization\b",
            "Pandas": r"\bpandas\b",
            "NumPy": r"\bnumpy\b",
            "Scikit-learn": r"\bscikit-learn|sklearn\b",
            "TensorFlow": r"\btensorflow\b",
            "PyTorch": r"\bpytorch\b",
            "Machine Learning": r"\bmachine\s?learning|ml\b",
            "Deep Learning": r"\bdeep\s?learning\b",
            "System Design": r"\bsystem\s?design\b",
            "DSA": r"\bdsa|data\s?structures|algorithms\b",
            "Docker": r"\bdocker\b",
            "Kubernetes": r"\bkubernetes|k8s\b",
            "AWS": r"\baws\b",
            "Git": r"\bgit\b",
            "Linux": r"\blinux\b",
            "CI/CD": r"\bci/cd|ci\s?cd\b",
            "Jenkins": r"\bjenkins\b",
            "Terraform": r"\bterraform\b",
            "MongoDB": r"\bmongodb\b",
            "PostgreSQL": r"\bpostgresql\b",
            "MySQL": r"\bmysql\b",
            "APIs": r"\bapi|rest\b",
            "Authentication": r"\bauthentication|auth\b",
            "UI/UX": r"\bui/ux|ux/ui\b",
            "Jest": r"\bjest\b",
            "Redux": r"\bredux\b"
        }

        text_lower = resume_text.lower()
        for skill_name, pattern in skill_patterns.items():
            if re.search(pattern, text_lower):
                detected_skills.append(skill_name)
                # Remove from missing if it was there
                if skill_name in missing_skills:
                    missing_skills.remove(skill_name)

    # Format output
    strong_skills_text = ", ".join(detected_skills[:5]) if detected_skills else "None detected in resume"
    missing_skills_text = ", ".join(missing_skills[:5]) if missing_skills else "All required skills present"

    return {
        "strong_skills": strong_skills_text,
        "missing_skills": missing_skills_text,
        "roadmap": f"""MONTH 1-2 (Foundation):
• {role_data['month1'][0]}
• {role_data['month1'][1]}

MONTH 3-4 (Intermediate):
• {role_data['month2'][0]}
• {role_data['month2'][1]}

MONTH 5-6 (Advanced):
• {role_data['month3'][0]}
• {role_data['month3'][1]}""",
        "focus_areas": f"• {role_data['focus'].split(',')[0]}\n• {role_data['focus'].split(',')[1]}\n• {role_data['focus'].split(',')[2]}",
        "next_actions": f"• Focus on: {missing_skills_text.split(',')[0] if missing_skills else 'Advanced skills'}\n• Join relevant communities\n• Build portfolio project",
        "timeline": "6 months for intermediate level"
    }


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

    # START WITH EMPTY - FORCE LLM TO PROVIDE REAL DATA
    result = {
        "score": "0/10",
        "strengths": "",
        "weaknesses": "",
        "suggestions": ""
    }

    if not response or len(response.strip()) < 10:
        # LLM didn't return valid response
        print(f"⚠️ WARNING: LLM returned empty/short response: {repr(response[:50])}")
        result["score"] = "ERROR"
        result["strengths"] = "❌ No LLM response received"
        result["weaknesses"] = "Check if Ollama is running: ollama serve"
        result["suggestions"] = "Restart Ollama and try again"
        return result

    lines = response.split("\n")
    current_section = None
    current_content = []
    has_score = False

    for line in lines:
        line_upper = line.upper()
        line_clean = line.strip()

        if not line_clean or "<" in line_clean:
            continue

        if "SCORE:" in line_upper:
            try:
                score_part = line.split(":")[-1].strip()
                if "/" in score_part:
                    score_num = score_part.split("/")[0].strip()
                    result["score"] = f"{score_num}/10"
                    has_score = True
                elif score_part and score_part[0].isdigit():
                    num = ''.join(c for c in score_part.split()[0] if c.isdigit())
                    if num:
                        result["score"] = f"{num}/10"
                        has_score = True
            except:
                pass
            current_section = None
            current_content = []

        elif "STRENGTHS:" in line_upper:
            if current_section and current_content:
                result[current_section] = "\n".join(current_content)
            current_section = "strengths"
            current_content = []

        elif "WEAKNESSES:" in line_upper:
            if current_section and current_content:
                result[current_section] = "\n".join(current_content)
            current_section = "weaknesses"
            current_content = []

        elif "SUGGESTIONS:" in line_upper:
            if current_section and current_content:
                result[current_section] = "\n".join(current_content)
            current_section = "suggestions"
            current_content = []

        elif current_section and line_clean:
            # Handle bullet points
            if line_clean.startswith("*"):
                bullet_text = line_clean[1:].strip()
            elif line_clean.startswith("-"):
                bullet_text = line_clean[1:].strip()
            else:
                bullet_text = line_clean

            if bullet_text:
                # Ensure bullet format
                if not bullet_text.startswith("•"):
                    bullet_text = f"• {bullet_text}"
                current_content.append(bullet_text)

    if current_section and current_content:
        result[current_section] = "\n".join(current_content)

    # Validate we got real data
    if not has_score:
        print(f"⚠️ WARNING: No score found in response")
        result["score"] = "ERROR"

    if not result["strengths"] or not result["weaknesses"] or not result["suggestions"]:
        print(f"⚠️ WARNING: Missing sections in response")
        print(f"   Strengths: {bool(result['strengths'])}")
        print(f"   Weaknesses: {bool(result['weaknesses'])}")
        print(f"   Suggestions: {bool(result['suggestions'])}")

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
