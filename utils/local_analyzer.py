"""
Local Resume Analyzer - No LLM needed
Extracts and analyzes resume content using pattern matching
"""

import re

def analyze_resume_locally(resume_text: str, target_role: str = None) -> dict:
    """Analyze resume without LLM using keyword matching"""

    text = resume_text.lower()

    # Validate this is actually a resume by checking for resume keywords
    resume_keywords = [
        r'\b(education|experience|skills|project|work experience|employment|certification)\b',
        r'\b(bachelor|master|degree|diploma|b\.?s\.|m\.?s\.|b\.?a\.|m\.?a\.|phd)\b',
        r'\b(python|java|sql|javascript|react|aws|docker|kubernetes|linux|git)\b',
        r'\b(software engineer|developer|analyst|manager|director|lead|architect)\b'
    ]

    resume_matches = sum(1 for keyword in resume_keywords if re.search(keyword, text))

    # If less than 2 resume keywords found, probably not a resume
    if resume_matches < 2:
        return {
            "score": "1/10",
            "strengths": "• File structure identified",
            "weaknesses": "• This does not appear to be a resume\n• Missing key resume sections (Education, Experience, Skills)\n• No professional content detected",
            "suggestions": "• Please upload an actual resume document\n• A resume should include Education, Experience, and Skills sections\n• Ensure the PDF contains your professional information"
        }

    result = {
        "score": "7/10",
        "strengths": "",
        "weaknesses": "",
        "suggestions": ""
    }


    # Define skill keywords
    all_skills = {
        "Python": r"\bpython\b",
        "SQL": r"\bsql\b",
        "Java": r"\bjava\b",
        "JavaScript": r"\bjavascript|js\b",
        "React": r"\breact\b",
        "Machine Learning": r"\bmachine learning|ml\b",
        "Data Analysis": r"\bdata analysis|eda\b",
        "Power BI": r"\bpower bi\b",
        "Tableau": r"\btableau\b",
        "Excel": r"\bexcel\b",
        "AWS": r"\baws\b",
        "Git": r"\bgit\b",
        "Docker": r"\bdocker\b",
        "Kubernetes": r"\bkubernetes\b",
        "Linux": r"\blinux\b",
        "API": r"\bapi\b",
        "REST": r"\brest\b",
        "MongoDB": r"\bmongodb\b",
        "PostgreSQL": r"\bpostgresql\b",
        "MySQL": r"\bmysql\b",
        "CI/CD": r"\bci/cd\b",
        "Pandas": r"\bpandas\b",
        "NumPy": r"\bnumpy\b",
        "Scikit-learn": r"\bscikit-learn|sklearn\b",
        "TensorFlow": r"\btensorflow\b",
        "PyTorch": r"\bpytorch\b",
        "Matplotlib": r"\bmatplotlib\b",
        "Seaborn": r"\bseaborn\b",
    }

    # Find skills present
    found_skills = []
    for skill, pattern in all_skills.items():
        if re.search(pattern, text):
            found_skills.append(skill)

    # Count experiences/projects
    project_count = len(re.findall(r'\b(project|developed|built|created|designed)\b', text))
    has_internship = bool(re.search(r'\bintern', text))
    has_gpa = bool(re.search(r'\b\d+\.\d{2}%\b', text))
    has_quantified = len(re.findall(r'\b\d+[%x]|\d+\s*(month|year|day|week)\b', text))

    # Calculate score
    score = 5  # Base score
    score += min(len(found_skills) // 3, 2)  # +2 max for skills
    score += 1 if has_internship else 0
    score += 1 if project_count >= 2 else 0
    score += 1 if has_quantified >= 3 else 0
    score = min(score, 9)

    # Build analysis
    strengths_list = []
    if len(found_skills) >= 5:
        strengths_list.append("• Good technical skill variety")
    if project_count >= 2:
        strengths_list.append("• Multiple projects/experiences")
    if has_internship:
        strengths_list.append("• Internship/professional experience")
    if has_quantified >= 3:
        strengths_list.append("• Includes quantified achievements")

    if not strengths_list:
        strengths_list = ["• Clear structure", "• Shows initiative"]

    weaknesses_list = []
    if has_quantified < 3:
        weaknesses_list.append("• Few quantified metrics/numbers")
    if project_count < 2:
        weaknesses_list.append("• Limited projects shown")
    if len(found_skills) < 5:
        weaknesses_list.append("• Limited technical skills listed")
    if not has_gpa and "gpa" not in text and "cgpa" not in text:
        weaknesses_list.append("• Missing GPA/academic metrics")

    if not weaknesses_list:
        weaknesses_list = ["• Could add more specifics"]

    suggestions_list = []
    if has_quantified < 3:
        suggestions_list.append("• Add numbers/metrics to achievements")
    if len(found_skills) < 8:
        suggestions_list.append("• List more technical skills")
    suggestions_list.append("• Use strong action verbs")

    if not suggestions_list:
        suggestions_list = ["• Keep improving skills"]

    result["score"] = f"{score}/10"
    result["strengths"] = "\n".join(strengths_list[:3])
    result["weaknesses"] = "\n".join(weaknesses_list[:3])
    result["suggestions"] = "\n".join(suggestions_list[:3])

    return result
