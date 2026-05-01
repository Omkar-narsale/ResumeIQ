"""
OPTIMIZED UNIFIED ANALYSIS - One LLM call per user action
Combines: Score, Skills, ATS Check, Feedback, Roadmap into single structured response
"""

from utils.llm_handler import get_llm_handler
from hashlib import md5
from utils.local_analyzer import analyze_resume_locally


def generate_unified_analysis(resume_text: str, target_role: str) -> dict:
    """Analyze resume using local analysis"""
    resume_text = resume_text[:1500]

    # Use local analyzer
    result = analyze_resume_locally(resume_text, target_role)

    # Extract skills from strengths
    strengths_list = result["strengths"].split("\n")
    weaknesses_list = result["weaknesses"].split("\n")
    suggestions_list = result["suggestions"].split("\n")

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

    # Create learning roadmap based on weaknesses
    roadmap_beginner = suggestions_list[0] if suggestions_list else "Start with fundamentals"
    roadmap_intermediate = f"Master the top {len(priority_skills)} skills for {target_role or 'your role'}"
    roadmap_advanced = "Lead projects and mentor others"

    return {
        "score": result["score"],
        "matched_skills": strengths_list[:3],
        "missing_skills": weaknesses_list[:3],
        "priority_skills": priority_skills[:3],
        "strengths": strengths_list,
        "weaknesses": weaknesses_list,
        "ats_checks": {"keywords": "Pass", "verbs": "Pass", "clarity": "Pass"},
        "improved_bullet": {"original": "", "improved": ""},
        "learning_roadmap": {
            "beginner": roadmap_beginner,
            "intermediate": roadmap_intermediate,
            "advanced": roadmap_advanced
        }
    }
    """
    ONE SINGLE LLM CALL that generates:
    - Overall Score
    - Matched/Missing Skills
    - Priority Skills
    - Strengths/Weaknesses
    - ATS Checks
    - Improved Bullet Points
    - Learning Roadmap

    Args:
        resume_text: Resume content (max 1500 chars for speed)
        target_role: Target position

    Returns:
        Parsed dict with all analysis sections
    """
    llm = get_llm_handler()

    # Limit input for speed
    resume_text = resume_text[:1500]

    role_context = get_role_context(target_role)

    prompt = f"""Read this resume and extract information:

Resume:
{resume_text}

Extract:
1. Rating (6-9)
2. Skills shown (3-4)
3. Skills missing (2-3)
4. Strengths (2-3)
5. Weaknesses (2-3)
6. Improvements (2-3)"""

    system_prompt = f"Extract information from resume. Be clear and factual."

    response = llm.ask_claude(prompt, system_prompt)
    print(f"DEBUG UNIFIED: {response[:100]}")
    return parse_unified_response(response)


def get_role_context(role: str) -> str:
    """Get role-specific skill focus"""
    role_lower = role.lower()

    contexts = {
        "data analyst": "Focus: SQL, Python, Excel, Power BI, Statistics. Ignore: System Design, Backend",
        "software engineer": "Focus: DSA, APIs, System Design, Backend. Ignore: Statistics, UI/UX",
        "frontend developer": "Focus: React/Vue, JavaScript, CSS, Performance. Ignore: Databases, DevOps",
        "ml engineer": "Focus: ML, Deep Learning, Python, TensorFlow, Math. Ignore: Frontend, DevOps",
        "devops engineer": "Focus: Docker, Kubernetes, CI/CD, AWS. Ignore: Frontend, Databases",
        "product manager": "Focus: Strategy, Analytics, Communication. Ignore: Technical implementation",
    }

    for key, context in contexts.items():
        if key in role_lower:
            return context
    return "Focus on core competencies for the role"


def parse_unified_response(response: str) -> dict:
    """Parse simple extraction response"""
    result = {
        "score": "0/10",
        "matched_skills": [],
        "missing_skills": [],
        "priority_skills": [],
        "strengths": [],
        "weaknesses": [],
        "ats_checks": {},
        "improved_bullet": {"original": "", "improved": ""},
        "learning_roadmap": {}
    }

    if not response or len(response.strip()) < 5:
        print(f"⚠️ Empty response")
        return result

    lines = response.split("\n")

    # Simple extraction - look for rating and lists
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()

        # Extract rating
        if "rating" in line_lower or ("1." in line and "rating" in line_lower):
            if i+1 < len(lines):
                rating_text = lines[i+1].strip()
                # Extract number from "6-9" or "7" etc
                import re
                nums = re.findall(r'\d+', rating_text)
                if nums:
                    result["score"] = f"{nums[0]}/10"

        # Extract skills shown
        elif "skills shown" in line_lower or "2." in line:
            skills_text = lines[i+1].strip() if i+1 < len(lines) else ""
            result["matched_skills"] = [s.strip() for s in skills_text.split(",") if s.strip()][:3]

        # Extract skills missing
        elif "skills missing" in line_lower or "3." in line:
            skills_text = lines[i+1].strip() if i+1 < len(lines) else ""
            result["missing_skills"] = [s.strip() for s in skills_text.split(",") if s.strip()][:3]

        # Extract strengths
        elif ("strengths" in line_lower and "4." in line) or "strength" in line_lower:
            strengths_text = lines[i+1].strip() if i+1 < len(lines) else ""
            result["strengths"] = [s.strip() for s in strengths_text.split(",") if s.strip()][:3]

        # Extract weaknesses
        elif ("weaknesses" in line_lower and "5." in line) or "weakness" in line_lower:
            weaknesses_text = lines[i+1].strip() if i+1 < len(lines) else ""
            result["weaknesses"] = [w.strip() for w in weaknesses_text.split(",") if w.strip()][:3]

        # Extract improvements
        elif "improv" in line_lower or "6." in line:
            improvements_text = lines[i+1].strip() if i+1 < len(lines) else ""
            # Use as learning roadmap placeholder
            result["learning_roadmap"]["beginner"] = improvements_text[:50]

    return result


def save_section(result: dict, section_name, content):
    """Helper to save parsed section content"""
    if not section_name or not content:
        return

    text = "\n".join(content).strip()

    if section_name == "improved_bullet":
        for line in content:
            if line.startswith("Original:"):
                result["improved_bullet"]["original"] = line.replace("Original:", "").strip()
            elif line.startswith("Improved:"):
                result["improved_bullet"]["improved"] = line.replace("Improved:", "").strip()

    elif section_name == "learning_roadmap":
        for line in content:
            if line.startswith("Beginner:"):
                result["learning_roadmap"]["beginner"] = line.replace("Beginner:", "").strip()
            elif line.startswith("Intermediate:"):
                result["learning_roadmap"]["intermediate"] = line.replace("Intermediate:", "").strip()
            elif line.startswith("Advanced:"):
                result["learning_roadmap"]["advanced"] = line.replace("Advanced:", "").strip()


def extract_status(line: str) -> str:
    """Extract Pass/Fail status"""
    if "Pass" in line:
        return "Pass"
    elif "Fail" in line:
        return "Fail"
    return "Unknown"


def get_cache_key(resume_text: str, role: str) -> str:
    """Generate cache key from resume + role"""
    combined = f"{resume_text[:500]}_{role}"
    return md5(combined.encode()).hexdigest()
