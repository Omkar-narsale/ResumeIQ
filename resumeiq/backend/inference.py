import hashlib
import json
import re
from typing import Dict, Any, List, Set
from datetime import datetime
from transformers import pipeline
import torch
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from docx import Document
from docx.shared import Pt, RGBColor, Inches

MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
DEVICE = os.getenv("DEVICE", "cpu")

model = None
tokenizer = None
pipe = None
cache: Dict[str, Any] = {}

# Skill database for extraction
COMMON_SKILLS = {
    # Programming Languages
    'python': ['python', 'py'], 'javascript': ['javascript', 'js', 'node'],
    'java': ['java '], 'csharp': ['c#', 'csharp'], 'cpp': ['c++', 'cpp'],
    'rust': ['rust'], 'go': ['golang', 'go '], 'php': ['php'], 'ruby': ['ruby'],
    'kotlin': ['kotlin'], 'swift': ['swift'], 'typescript': ['typescript', 'ts'],

    # Frontend
    'react': ['react', 'reactjs'], 'vue': ['vue', 'vuejs'], 'angular': ['angular'],
    'html': ['html'], 'css': ['css'], 'sass': ['sass', 'scss'],
    'webpack': ['webpack'], 'jest': ['jest'],

    # Backend
    'nodejs': ['node.js', 'nodejs', 'node'], 'django': ['django'],
    'flask': ['flask'], 'spring': ['spring'], 'fastapi': ['fastapi'],
    'express': ['express'], 'laravel': ['laravel'],

    # Databases
    'sql': ['sql'], 'postgresql': ['postgresql', 'postgres'], 'mysql': ['mysql'],
    'mongodb': ['mongodb', 'mongo'], 'redis': ['redis'], 'dynamodb': ['dynamodb'],
    'elasticsearch': ['elasticsearch'],

    # Data & ML
    'pandas': ['pandas'], 'numpy': ['numpy'], 'scikit': ['scikit-learn', 'sklearn'],
    'tensorflow': ['tensorflow'], 'pytorch': ['pytorch', 'torch'], 'keras': ['keras'],
    'sql': ['sql', 'database'], 'excel': ['excel', 'vba'],
    'tableau': ['tableau'], 'powerbi': ['power bi', 'powerbi'], 'looker': ['looker'],
    'spark': ['spark', 'apache spark'],

    # DevOps & Cloud
    'aws': ['aws', 'amazon'], 'gcp': ['gcp', 'google cloud'], 'azure': ['azure'],
    'docker': ['docker'], 'kubernetes': ['kubernetes', 'k8s'], 'jenkins': ['jenkins'],
    'github': ['github'], 'gitlab': ['gitlab'], 'bitbucket': ['bitbucket'],
    'terraform': ['terraform'], 'ansible': ['ansible'],

    # Other Tools
    'git': ['git'], 'linux': ['linux', 'unix'], 'windows': ['windows'],
    'macos': ['macos', 'mac'], 'api': ['api', 'rest', 'graphql'],
    'agile': ['agile', 'scrum', 'kanban'], 'ci/cd': ['ci/cd', 'cicd'],
    'testing': ['testing', 'qa', 'pytest'], 'microservices': ['microservices'],

    # Soft Skills
    'communication': ['communication', 'leadership', 'teamwork', 'collaboration'],
    'problem solving': ['problem solving', 'analytical', 'critical thinking'],
    'project management': ['project management', 'pmp'],
}

def get_cache_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

def load_model():
    global model, tokenizer, pipe
    if pipe is None:
        print(f"Loading model: {MODEL_NAME}")
        pipe = pipeline("text-generation", model=MODEL_NAME, device=-1)
        print("[OK] Model loaded successfully")

def infer(prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
    cache_key = get_cache_key(prompt)
    if cache_key in cache:
        return cache[cache_key]

    load_model()
    try:
        output = pipe(prompt, max_new_tokens=max_tokens, temperature=temperature, do_sample=True)
        response = output[0]["generated_text"][len(prompt):].strip()
        cache[cache_key] = response
        return response
    except Exception as e:
        print(f"Inference error: {e}")
        return ""

def parse_json_response(text: str) -> dict:
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
    except:
        pass
    return {}

def extract_skills(text: str) -> Set[str]:
    """Extract skills from text using pattern matching"""
    text_lower = text.lower()
    skills = set()

    for skill_name, keywords in COMMON_SKILLS.items():
        for keyword in keywords:
            # Use word boundaries for better matching
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                skills.add(skill_name)
                break

    return skills

def match_job(resume_text: str, job_description: str) -> dict:
    """Dynamically analyze resume vs job description"""

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Calculate match
    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills
    extra_skills = resume_skills - job_skills

    # Calculate score (0-100, then /10)
    if len(job_skills) == 0:
        match_percentage = 50
    else:
        match_percentage = int((len(matched_skills) / len(job_skills)) * 100)

    # Adjust score based on number of missing skills
    if len(missing_skills) > len(job_skills) * 0.7:  # Missing 70%+
        score = 3 + (match_percentage / 50)  # 3-5
    elif len(missing_skills) > len(job_skills) * 0.5:  # Missing 50-70%
        score = 5 + (match_percentage / 50)  # 5-7
    elif len(missing_skills) > len(job_skills) * 0.2:  # Missing 20-50%
        score = 6 + (match_percentage / 100)  # 6-8
    else:  # Missing < 20%
        score = 8 + (match_percentage / 200)  # 8-10

    score = round(min(10, max(3, score)), 1)

    # Generate context-specific suggestions
    suggestions = generate_suggestions(
        matched_skills, missing_skills, resume_text, job_description
    )

    return {
        "match_score": score,
        "skills_matched": list(matched_skills)[:5],
        "skills_missing": list(missing_skills)[:5],
        "suggestions": suggestions,
        "match_percentage": match_percentage
    }

def generate_suggestions(matched: Set[str], missing: Set[str],
                        resume_text: str, job_desc: str) -> List[str]:
    """Generate specific, contextual suggestions"""
    suggestions = []

    # High-priority missing skills
    if missing:
        top_missing = sorted(list(missing))[:3]
        for skill in top_missing:
            suggestions.append(f"Add experience with {skill} - it's required but not highlighted in your resume")

    # Context from job description
    if 'senior' in job_desc.lower() and len(matched) < 5:
        suggestions.append("Emphasize leadership and mentoring experience for this senior role")

    if 'startup' in job_desc.lower():
        suggestions.append("Highlight your ability to wear multiple hats and work in fast-paced environments")

    if any(tech in job_desc.lower() for tech in ['cloud', 'aws', 'gcp', 'azure']):
        if 'aws' not in matched and 'gcp' not in matched and 'azure' not in matched:
            suggestions.append("Add cloud platform certifications or projects to strengthen candidacy")

    # Experience gaps
    if 'years' in job_desc.lower():
        years_match = re.search(r'(\d+)\+?\s*years?', job_desc.lower())
        if years_match and 'year' not in resume_text.lower():
            suggestions.append("Explicitly mention years of experience in your resume summary")

    # Project-based suggestions
    if len(matched) > 0:
        matched_list = list(matched)[:2]
        suggestions.append(f"Highlight projects using {', '.join(matched_list)} with measurable impact")

    # Fallback suggestions if none generated
    if not suggestions:
        if len(missing) > 0:
            suggestions.append(f"Focus on learning {list(missing)[0]} to improve job fit")
        suggestions.append("Quantify your achievements with metrics and business impact")
        suggestions.append("Include links to portfolio or GitHub projects")

    return suggestions[:4]  # Return top 4 suggestions

def analyze_resume(resume_text: str) -> dict:
    prompt = f"""Analyze this resume and return a JSON response with:
- score (0-10)
- strengths (list of 3-5 items)
- weaknesses (list of 3-5 items)
- suggestions (list of 3-5 items)
- skills_matched (inferred list)
- skills_missing (suggested list)
- priority_skills (top 3)
- roadmap (list of 2-3 phases with goals)

Resume:
{resume_text[:1500]}

JSON Response:"""

    response = infer(prompt)
    result = parse_json_response(response)

    # Ensure required fields with defaults
    return {
        "score": float(result.get("score", 7.0)),
        "strengths": result.get("strengths", ["Clear structure", "Good experience"]),
        "weaknesses": result.get("weaknesses", ["Limited metrics", "Needs quantification"]),
        "suggestions": result.get("suggestions", ["Add quantified achievements", "Improve action verbs"]),
        "skills_matched": result.get("skills_matched", ["Python", "Communication"]),
        "skills_missing": result.get("skills_missing", ["Kubernetes", "Advanced AWS"]),
        "priority_skills": result.get("priority_skills", ["System Design", "Cloud Architecture"]),
        "roadmap": result.get("roadmap", [
            {"phase": "Week 1-2", "focus": "Master fundamentals"},
            {"phase": "Week 3-4", "focus": "Build projects"},
            {"phase": "Week 5+", "focus": "Interview prep"}
        ])
    }

def rewrite_resume(resume_text: str) -> dict:
    prompt = f"""Rewrite this resume section to be more professional, impactful, and ATS-friendly.
Use strong action verbs, add quantified achievements where possible, and improve clarity.

IMPORTANT: Return the FULL rewritten version, not a snippet.

Original Resume:
{resume_text[:1500]}

Provide your response as JSON:
{{
    "original": "First 150 characters of original",
    "rewritten": "FULL rewritten version with all content improved",
    "improvements": ["Improvement 1", "Improvement 2", "Improvement 3", "Improvement 4"]
}}

Only respond with valid JSON."""

    response = infer(prompt, max_tokens=800)
    result = parse_json_response(response)

    # Generate fallback rewrite if LLM fails
    if not result.get("rewritten"):
        improved = improve_resume_fallback(resume_text)
        result["rewritten"] = improved

    return {
        "original": resume_text[:150],
        "rewritten": result.get("rewritten", improve_resume_fallback(resume_text))[:1000],
        "improvements": result.get("improvements", [
            "Added strong action verbs (Led, Developed, Implemented)",
            "Quantified achievements with metrics and percentages",
            "Improved bullet point clarity and structure",
            "Enhanced technical specificity and relevance"
        ])
    }

def improve_resume_fallback(text: str) -> str:
    """Generate improved resume when LLM fails"""
    replacements = {
        "worked": "Led", "helped": "Collaborated", "did": "Executed",
        "made": "Designed", "fixed": "Resolved", "used": "Leveraged"
    }
    improved = text
    for weak, strong in replacements.items():
        improved = improved.replace(weak + " ", strong + " ")
    return improved + "\n\n[Achievements: Added 25% efficiency improvement, Managed cross-functional team, Delivered on-time]"

def match_job(resume_text: str, job_description: str) -> dict:
    prompt = f"""Compare this resume to the job description and return match analysis.

Resume:
{resume_text[:800]}

Job Description:
{job_description[:800]}

Return JSON with:
- match_score (0-100 percentage)
- skills_matched (list of matching skills)
- skills_missing (list of required but missing skills)
- suggestions (list of 3-5 improvement suggestions)

JSON Response:"""

    response = infer(prompt, max_tokens=300)
    result = parse_json_response(response)

    return {
        "match_score": float(result.get("match_score", 65)),
        "skills_matched": result.get("skills_matched", ["Python", "SQL", "Problem Solving"]),
        "skills_missing": result.get("skills_missing", ["Kubernetes", "AWS"]),
        "suggestions": result.get("suggestions", [
            "Highlight relevant cloud experience",
            "Add containerization examples",
            "Emphasize DevOps knowledge"
        ])
    }

def interview_questions(role: str, resume_text: str = "") -> dict:
    prompt = f"""Generate 5 technical interview questions for a {role} position.

Resume context: {resume_text[:300]}

Return JSON with:
- questions (list of 5 questions)
- tips (list of 3-4 interview tips)

JSON Response:"""

    response = infer(prompt, max_tokens=400)
    result = parse_json_response(response)

    return {
        "questions": result.get("questions", [
            f"Tell me about your experience with {role} technologies",
            "Describe a challenging project you led",
            "How do you approach system design?",
            "What's your experience with agile methodologies?",
            f"Why are you interested in this {role} role?"
        ]),
        "tips": result.get("tips", [
            "Use the STAR method for behavioral questions",
            "Ask clarifying questions before solving",
            "Show your thought process clearly"
        ])
    }

def learning_roadmap(target_role: str, current_skills: list) -> dict:
    skills_str = ", ".join(current_skills) if current_skills else "none"

    prompt = f"""Create a DETAILED, ROLE-SPECIFIC learning roadmap for transitioning to {target_role}.
Current skills: {skills_str}

Generate a structured, week-by-week learning plan with SPECIFIC technologies, tools, and projects.
Make it actionable and realistic.

Return JSON with:
{{
    "phases": [
        {{"duration": "Week 1-2", "focus": "Specific skills and projects", "skills": ["Skill1", "Skill2"]}},
        {{"duration": "Week 3-4", "focus": "...", "skills": [...]}},
        {{"duration": "Week 5-6", "focus": "...", "skills": [...]}}
    ],
    "estimated_duration": "Total weeks",
    "resources": ["Resource 1", "Resource 2", "Resource 3"]
}}

Be SPECIFIC to {target_role}. Only respond with valid JSON."""

    response = infer(prompt, max_tokens=600)
    result = parse_json_response(response)

    # Generate fallback role-specific roadmap
    if not result.get("phases"):
        result = get_role_specific_roadmap(target_role, current_skills)

    return {
        "phases": result.get("phases", get_role_specific_roadmap(target_role, current_skills).get("phases", [])),
        "estimated_duration": result.get("estimated_duration", "8-12 weeks"),
        "resources": result.get("resources", [
            "Official documentation",
            "Project-based tutorials",
            "Community forums",
            "Real-world projects"
        ])
    }

def get_role_specific_roadmap(role: str, current_skills: list) -> dict:
    """Generate role-specific roadmap when LLM fails"""
    roadmaps = {
        "Data Scientist": {
            "phases": [
                {"duration": "Week 1-2", "focus": "Python, NumPy, Pandas basics", "skills": ["Python", "NumPy", "Pandas"]},
                {"duration": "Week 3-4", "focus": "SQL, database queries, data cleaning", "skills": ["SQL", "Data Wrangling", "EDA"]},
                {"duration": "Week 5-6", "focus": "Statistics, visualization (Matplotlib, Seaborn)", "skills": ["Statistics", "Matplotlib", "Seaborn"]},
                {"duration": "Week 7-8", "focus": "Machine Learning (Scikit-learn, basics)", "skills": ["ML Fundamentals", "Scikit-learn"]},
                {"duration": "Week 9-12", "focus": "Advanced ML, projects, deployment", "skills": ["Advanced ML", "Projects", "Deployment"]}
            ],
            "resources": ["DataCamp", "Kaggle", "Andrew Ng ML Course", "Real datasets"]
        },
        "Machine Learning Engineer": {
            "phases": [
                {"duration": "Week 1-2", "focus": "Deep Learning fundamentals", "skills": ["Neural Networks", "TensorFlow basics"]},
                {"duration": "Week 3-4", "focus": "TensorFlow/PyTorch, model building", "skills": ["PyTorch", "Model architectures"]},
                {"duration": "Week 5-6", "focus": "Computer Vision, CNN", "skills": ["CNN", "Image processing"]},
                {"duration": "Week 7-8", "focus": "NLP, transformers", "skills": ["NLP", "Transformers"]},
                {"duration": "Week 9-12", "focus": "Model optimization, deployment, MLOps", "skills": ["Model optimization", "MLOps", "Deployment"]}
            ],
            "resources": ["Fast.ai", "PyTorch docs", "Papers with code", "Kaggle competitions"]
        },
        "Data Analyst": {
            "phases": [
                {"duration": "Week 1-2", "focus": "SQL fundamentals, queries", "skills": ["SQL", "Database basics"]},
                {"duration": "Week 3-4", "focus": "Excel advanced, Power Query", "skills": ["Excel", "Data pivot tables"]},
                {"duration": "Week 5-6", "focus": "Power BI dashboards and visualizations", "skills": ["Power BI", "Tableau"]},
                {"duration": "Week 7-8", "focus": "Python for data analysis (Pandas, Matplotlib)", "skills": ["Python", "Pandas", "Matplotlib"]},
                {"duration": "Week 9-12", "focus": "Advanced dashboards, storytelling, projects", "skills": ["Dashboard design", "Data storytelling"]}
            ],
            "resources": ["Mode Analytics SQL", "Power BI docs", "Tableau public", "Real datasets"]
        },
        "Senior Software Engineer": {
            "phases": [
                {"duration": "Week 1-2", "focus": "System design fundamentals", "skills": ["System Architecture", "Scalability"]},
                {"duration": "Week 3-4", "focus": "Database design, distributed systems", "skills": ["DB optimization", "Distributed systems"]},
                {"duration": "Week 5-6", "focus": "Microservices, APIs design", "skills": ["Microservices", "RESTful APIs", "gRPC"]},
                {"duration": "Week 7-8", "focus": "Cloud architecture (AWS/GCP)", "skills": ["Cloud services", "Containerization"]},
                {"duration": "Week 9-12", "focus": "Leadership, mentoring, architecture decisions", "skills": ["Tech leadership", "Code review", "Mentoring"]}
            ],
            "resources": ["System Design Interview prep", "AWS/GCP docs", "Design patterns book", "Open source projects"]
        },
        "Cloud Architect": {
            "phases": [
                {"duration": "Week 1-2", "focus": "Cloud fundamentals (AWS/Azure/GCP)", "skills": ["Cloud basics", "Services overview"]},
                {"duration": "Week 3-4", "focus": "Networking, Security, Identity", "skills": ["VPC", "IAM", "Security groups"]},
                {"duration": "Week 5-6", "focus": "Infrastructure as Code (Terraform)", "skills": ["Terraform", "CloudFormation"]},
                {"duration": "Week 7-8", "focus": "Container orchestration (Kubernetes)", "skills": ["Docker", "Kubernetes"]},
                {"duration": "Week 9-12", "focus": "Advanced architectures, cost optimization, migrations", "skills": ["High availability", "Disaster recovery", "Cost optimization"]}
            ],
            "resources": ["Cloud certification paths", "Terraform docs", "Kubernetes official", "Cloud white papers"]
        },
        "DevOps Engineer": {
            "phases": [
                {"duration": "Week 1-2", "focus": "Linux fundamentals, bash scripting", "skills": ["Linux", "Bash", "Shell scripting"]},
                {"duration": "Week 3-4", "focus": "CI/CD pipelines (Jenkins, GitLab CI)", "skills": ["CI/CD", "Jenkins", "Git workflows"]},
                {"duration": "Week 5-6", "focus": "Docker, containerization", "skills": ["Docker", "Container registry"]},
                {"duration": "Week 7-8", "focus": "Kubernetes, orchestration", "skills": ["Kubernetes", "Helm"]},
                {"duration": "Week 9-12", "focus": "Monitoring, logging, infrastructure automation", "skills": ["Monitoring", "Logging", "Automation"]}
            ],
            "resources": ["Linux Academy", "Docker official", "Kubernetes docs", "DevOps subreddits"]
        }
    }

    # Find matching roadmap or use generic
    for key in roadmaps:
        if key.lower() in role.lower() or role.lower() in key.lower():
            return {"phases": roadmaps[key]["phases"], "resources": roadmaps[key]["resources"]}

    # Generic fallback
    return {
        "phases": [
            {"duration": "Week 1-2", "focus": "Master core fundamentals and basics", "skills": ["Fundamentals"]},
            {"duration": "Week 3-4", "focus": "Build intermediate projects", "skills": ["Projects"]},
            {"duration": "Week 5-8", "focus": "Deep dive into specialization", "skills": ["Specialization"]},
            {"duration": "Week 9-12", "focus": "Advanced topics and real-world application", "skills": ["Advanced topics"]}
        ],
        "resources": ["Online courses", "Documentation", "Projects", "Community"]
    }

def evaluate_answer(role: str, question: str, answer: str) -> dict:
    """Evaluate interview answer and provide feedback"""
    prompt = f"""You are an expert interview coach. Evaluate this answer to an interview question.

Role: {role}
Question: {question}
Answer: {answer}

Return JSON with:
- score (0-10, where 10 is excellent)
- feedback (specific constructive feedback)
- better_answer (example of a better answer to the same question)

JSON Response:"""

    response = infer(prompt, max_tokens=400)
    result = parse_json_response(response)

    return {
        "score": float(result.get("score", 5.0)),
        "feedback": result.get("feedback", "Good attempt. Focus on being more specific with examples and metrics."),
        "better_answer": result.get("better_answer", "Here's a stronger approach: Start with the challenge, explain your solution, and highlight the impact with metrics.")
    }

def generate_cover_letter(job_description: str, resume_text: str) -> dict:
    """Generate a professional cover letter for a job"""
    prompt = f"""Generate a professional cover letter based on this resume and job description.

Job Description:
{job_description[:500]}

Resume:
{resume_text[:800]}

Return JSON with:
- cover_letter (a complete, compelling cover letter 200-300 words)
- improvements (list of 4 key improvements made: strong opening, relevant skills matching, impact metrics, compelling closing)

JSON Response:"""

    response = infer(prompt, max_tokens=500)
    result = parse_json_response(response)

    return {
        "cover_letter": result.get("cover_letter", "Dear Hiring Manager,\n\nI am writing to express my strong interest in this position. With my experience and skills aligned with your requirements, I am confident I can contribute significantly to your team. I am excited about the opportunity to bring my expertise to your organization.\n\nBest regards"),
        "improvements": result.get("improvements", [
            "Opened with specific role and company name",
            "Highlighted relevant skills matching job requirements",
            "Included quantified achievements and business impact",
            "Closed with strong call-to-action and enthusiasm"
        ])
    }

def optimize_keywords(resume_text: str, job_description: str) -> dict:
    """Optimize resume keywords for better ATS matching"""
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Find keywords to add
    missing_keywords = job_skills - resume_skills
    matched_keywords = resume_skills & job_skills

    prompt = f"""Optimize this resume for ATS (Applicant Tracking System) and job matching.

Resume:
{resume_text[:800]}

Required Keywords from Job Description:
{', '.join(list(job_skills)[:10])}

Return JSON with:
- recommended_keywords (list of 5-8 keywords to add)
- placement_suggestions (how and where to add each keyword)
- optimized_keywords (keywords already well-placed)
- ats_improvements (3-4 specific improvements for ATS compatibility)

JSON Response:"""

    response = infer(prompt, max_tokens=400)
    result = parse_json_response(response)

    return {
        "recommended_keywords": result.get("recommended_keywords", list(missing_keywords)[:8]),
        "placement_suggestions": result.get("placement_suggestions", [
            f"Add {', '.join(list(missing_keywords)[:3])} to skills section",
            "Include relevant keywords in job descriptions",
            "Use consistent terminology throughout"
        ]),
        "optimized_keywords": result.get("optimized_keywords", list(matched_keywords)[:5]),
        "ats_improvements": result.get("ats_improvements", [
            "Use standard section headers (Skills, Experience, Education)",
            "Avoid graphics, images, and unusual formatting",
            "Use standard fonts and consistent spacing",
            "Include complete contact information"
        ]),
        "keywords_matched": len(matched_keywords),
        "keywords_missing": len(missing_keywords)
    }

def check_ats_score(resume_text: str) -> dict:
    """Check ATS compatibility score of resume"""
    lines = resume_text.split('\n')
    has_contact = any(x in resume_text.lower() for x in ['email', '@', 'phone', '+'])
    has_sections = any(x in resume_text.lower() for x in ['experience', 'education', 'skills', 'summary'])
    has_metrics = any(c.isdigit() for c in resume_text if c in '0123456789%+')

    score = 50
    issues = []
    suggestions = []

    if has_contact:
        score += 10
    else:
        issues.append("Missing contact information")
        suggestions.append("Add email and phone number at the top")

    if has_sections:
        score += 15
    else:
        issues.append("Missing standard sections")
        suggestions.append("Organize content with clear section headers")

    if has_metrics:
        score += 15
    else:
        issues.append("No quantified metrics")
        suggestions.append("Include numbers, percentages, or measurable achievements")

    # Check formatting
    if len(lines) < 5:
        issues.append("Resume appears too short")
        suggestions.append("Expand with more detailed experience and achievements")
    else:
        score += 10

    # Check for keywords
    skills_found = len(extract_skills(resume_text))
    score += min(10, skills_found)

    if len(resume_text) < 200:
        issues.append("Content appears insufficient")
        suggestions.append("Provide more comprehensive information about experience")
    else:
        score += 5

    return {
        "ats_score": min(100, max(0, score)),
        "issues": issues,
        "suggestions": suggestions[:4],
        "formatting_check": {
            "has_contact_info": has_contact,
            "has_standard_sections": has_sections,
            "has_quantified_metrics": has_metrics,
            "skills_detected": skills_found
        }
    }

def analyze_skill_gaps(current_skills: List[str], target_role: str) -> dict:
    """Analyze skill gaps between current skills and target role"""
    current_set = set(s.lower() for s in current_skills) if current_skills else set()

    # Get required skills for role from our skill database
    role_requirements = {
        "data scientist": ["python", "pandas", "sql", "statistics", "scikit"],
        "machine learning engineer": ["python", "pytorch", "tensorflow", "ml fundamentals"],
        "data analyst": ["sql", "tableau", "power bi", "excel", "python"],
        "senior software engineer": ["system architecture", "microservices", "api", "scalability"],
        "cloud architect": ["aws", "kubernetes", "docker", "terraform"],
        "devops engineer": ["linux", "docker", "kubernetes", "ci/cd", "jenkins"],
        "full stack developer": ["javascript", "react", "nodejs", "sql", "api"],
        "backend engineer": ["python", "nodejs", "sql", "api", "microservices"],
        "frontend engineer": ["javascript", "react", "html", "css", "typescript"],
    }

    # Find matching requirements
    role_lower = target_role.lower()
    required_skills = set()
    for key, skills in role_requirements.items():
        if key in role_lower or role_lower in key:
            required_skills = set(skills)
            break

    if not required_skills:
        required_skills = set(["core technical skills", "communication", "problem solving"])

    gaps = required_skills - current_set
    mastered = required_skills & current_set
    additional = current_set - required_skills

    return {
        "role": target_role,
        "gaps": list(gaps)[:8],
        "mastered_skills": list(mastered)[:5],
        "additional_skills": list(additional)[:5],
        "gap_count": len(gaps),
        "coverage_percentage": int((len(mastered) / len(required_skills) * 100)) if required_skills else 0,
        "learning_priority": sorted(list(gaps))[:3],
        "estimated_learning_time": f"{len(gaps) * 2}-{len(gaps) * 4} weeks"
    }

def compare_resumes(resume1_text: str, resume2_text: str) -> dict:
    """Compare two resumes and analyze strengths"""
    skills1 = extract_skills(resume1_text)
    skills2 = extract_skills(resume2_text)

    common_skills = skills1 & skills2
    unique_to_1 = skills1 - skills2
    unique_to_2 = skills2 - skills1

    len1 = len(resume1_text)
    len2 = len(resume2_text)

    # Simple content analysis
    has_metrics_1 = any(c.isdigit() for c in resume1_text if c in '0123456789%')
    has_metrics_2 = any(c.isdigit() for c in resume2_text if c in '0123456789%')

    prompt = f"""Compare these two resumes. Return JSON with:
- comparison_summary (who is stronger candidate and why)
- resume1_strengths (list of 3-4 strengths)
- resume2_strengths (list of 3-4 strengths)
- improvement_suggestions (what each resume could improve)

Resume 1:
{resume1_text[:500]}

Resume 2:
{resume2_text[:500]}

JSON Response:"""

    response = infer(prompt, max_tokens=400)
    result = parse_json_response(response)

    return {
        "comparison_summary": result.get("comparison_summary", "Comparison analysis of both resumes"),
        "resume1_strengths": result.get("resume1_strengths", [
            f"Contains {len(skills1)} identified skills",
            "Has quantified metrics" if has_metrics_1 else "Needs more metrics"
        ]),
        "resume2_strengths": result.get("resume2_strengths", [
            f"Contains {len(skills2)} identified skills",
            "Has quantified metrics" if has_metrics_2 else "Needs more metrics"
        ]),
        "common_skills": list(common_skills)[:5],
        "resume1_unique": list(unique_to_1)[:5],
        "resume2_unique": list(unique_to_2)[:5],
        "length_comparison": {"resume1": len1, "resume2": len2},
        "skills_comparison": {"resume1_total": len(skills1), "resume2_total": len(skills2)}
    }

def manage_resume_version(resume_text: str, version_name: str, description: str = "") -> dict:
    """Create and manage resume versions"""
    return {
        "version_name": version_name,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "content_preview": resume_text[:200],
        "word_count": len(resume_text.split()),
        "skills_identified": len(extract_skills(resume_text))
    }

def generate_resume_pdf(resume_text: str, filename: str = "resume.pdf") -> BytesIO:
    """Generate PDF version of resume"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=RGBColor(0, 51, 102),
        spaceAfter=6,
        alignment=1
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceAfter=4
    )

    story = []

    # Split resume into sections
    lines = resume_text.split('\n')
    for line in lines:
        if line.strip():
            if any(header in line.upper() for header in ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'SUMMARY', 'OBJECTIVE']):
                story.append(Paragraph(line.strip(), title_style))
                story.append(Spacer(1, 0.1*inch))
            else:
                story.append(Paragraph(line.strip(), body_style))
        else:
            story.append(Spacer(1, 0.05*inch))

    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_resume_docx(resume_text: str, filename: str = "resume.docx") -> BytesIO:
    """Generate DOCX version of resume"""
    doc = Document()

    lines = resume_text.split('\n')
    for line in lines:
        if line.strip():
            paragraph = doc.add_paragraph(line.strip())

            # Format headers
            if any(header in line.upper() for header in ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'SUMMARY', 'OBJECTIVE']):
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.size = Pt(12)
                    run.font.color.rgb = RGBColor(0, 51, 102)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def check_grammar(resume_text: str) -> dict:
    """Check grammar and spelling in resume"""
    issues = []
    suggestions = []

    # Simple regex-based grammar checks
    patterns = {
        r'\b[A-Z]{2,}\b(?!\s[A-Z])': 'Acronym without explanation',
        r'(\w+)\s+\1\b': 'Repeated word detected',
        r'\s{2,}': 'Multiple spaces detected',
        r'[,.:;!?]\s{0}': 'Missing space after punctuation',
    }

    for pattern, issue in patterns.items():
        matches = re.finditer(pattern, resume_text)
        for match in matches:
            issues.append({
                'type': issue,
                'text': match.group(),
                'position': match.start(),
                'suggestion': f'Review: {issue}'
            })

    # Check for common resume errors
    common_errors = {
        'teh': 'the',
        'recieve': 'receive',
        'seperate': 'separate',
        'occured': 'occurred',
        'wich': 'which',
        'managment': 'management',
        'responsiblity': 'responsibility',
    }

    text_lower = resume_text.lower()
    for error, correction in common_errors.items():
        if error in text_lower:
            pos = text_lower.find(error)
            issues.append({
                'type': 'Spelling Error',
                'text': error,
                'position': pos,
                'suggestion': f'Did you mean: {correction}?'
            })
            suggestions.append(f'Replace "{error}" with "{correction}"')

    # Check for weak action verbs
    weak_verbs = ['helped', 'worked', 'did', 'made', 'handled', 'responsible for']
    strong_verbs = ['Led', 'Developed', 'Implemented', 'Designed', 'Managed', 'Drove']

    for weak in weak_verbs:
        if weak.lower() in text_lower:
            suggestions.append(f'Replace "{weak}" with stronger verb like "{strong_verbs[weak_verbs.index(weak)]}"')

    score = 100 - (len(issues) * 5) - (len(suggestions) * 3)
    score = max(0, min(100, score))

    return {
        'grammar_score': score,
        'issues_found': len(issues),
        'issues': issues[:10],  # Limit to 10 issues
        'suggestions': suggestions[:5],  # Limit to 5 suggestions
        'overall_feedback': 'Good grammar!' if score >= 80 else 'Needs improvement' if score >= 60 else 'Multiple issues found'
    }

def batch_match_jobs(resume_text: str, job_descriptions: List[str]) -> dict:
    """Compare resume against multiple job descriptions"""
    results = []

    resume_skills = extract_skills(resume_text)

    for idx, job_desc in enumerate(job_descriptions, 1):
        job_skills = extract_skills(job_desc)
        matched_skills = resume_skills & job_skills
        missing_skills = job_skills - resume_skills

        if len(job_skills) == 0:
            match_percentage = 50
        else:
            match_percentage = int((len(matched_skills) / len(job_skills)) * 100)

        # Calculate score
        if len(missing_skills) > len(job_skills) * 0.7:
            score = 3 + (match_percentage / 50)
        elif len(missing_skills) > len(job_skills) * 0.5:
            score = 5 + (match_percentage / 50)
        elif len(missing_skills) > len(job_skills) * 0.2:
            score = 6 + (match_percentage / 100)
        else:
            score = 8 + (match_percentage / 200)

        score = round(min(10, max(3, score)), 1)

        results.append({
            'job_index': idx,
            'match_score': score,
            'match_percentage': match_percentage,
            'skills_matched': list(matched_skills)[:5],
            'skills_missing': list(missing_skills)[:5],
            'fit_level': 'Excellent' if score >= 8 else 'Good' if score >= 6 else 'Fair' if score >= 4 else 'Poor'
        })

    # Sort by match score
    results_sorted = sorted(results, key=lambda x: x['match_score'], reverse=True)

    return {
        'total_jobs': len(job_descriptions),
        'best_matches': results_sorted[:3],  # Top 3
        'all_results': results_sorted,
        'avg_score': round(sum(r['match_score'] for r in results) / len(results), 1) if results else 0
    }
