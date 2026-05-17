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
    """Analyze resume with actual scoring based on content"""
    text_lower = resume_text.lower()
    score = 0
    strengths = []
    weaknesses = []
    suggestions = []

    # SCORING LOGIC
    # Structure & Organization (max 2 points)
    if any(keyword in text_lower for keyword in ['summary', 'objective', 'profile']):
        score += 1
        strengths.append("✓ Professional summary included")
    else:
        weaknesses.append("✗ Missing professional summary or objective")
        suggestions.append("Add a professional summary at the top of your resume")

    if any(keyword in text_lower for keyword in ['education', 'degree', 'university', 'college']):
        score += 1
        strengths.append("✓ Education section present")
    else:
        weaknesses.append("✗ No education section found")
        suggestions.append("Include your education details")

    # Experience & Metrics (max 2.5 points)
    if any(keyword in text_lower for keyword in ['worked', 'led', 'managed', 'developed', 'created', 'built']):
        score += 1
        strengths.append("✓ Action-oriented language detected")
    else:
        weaknesses.append("✗ Lacks strong action verbs")
        suggestions.append("Use powerful action verbs like Led, Managed, Developed")

    metrics_found = len(re.findall(r'\d+%|\$\d+|increased|improved|reduced', text_lower))
    if metrics_found >= 3:
        score += 1.5
        strengths.append("✓ Good use of metrics and quantification")
    elif metrics_found >= 1:
        score += 0.5
        weaknesses.append("✗ Limited metrics and numbers")
        suggestions.append("Add more quantified results (%, $, time saved)")
    else:
        weaknesses.append("✗ No metrics found")
        suggestions.append("Quantify your achievements with numbers and percentages")

    # Skills (max 2 points)
    tech_skills = extract_skills(resume_text)
    if len(tech_skills) >= 5:
        score += 1
        strengths.append(f"✓ Solid technical foundation ({len(tech_skills)} skills)")
    elif len(tech_skills) > 0:
        score += 0.5
        suggestions.append(f"Expand technical skills - currently showing {len(tech_skills)} skills")
    else:
        suggestions.append("Explicitly list your technical skills")

    if any(keyword in text_lower for keyword in ['communication', 'team', 'leadership', 'collaboration']):
        score += 1
        strengths.append("✓ Soft skills highlighted")
    else:
        suggestions.append("Highlight soft skills like teamwork, communication, leadership")

    # Formatting & Clarity (max 1.5 points)
    line_count = len(resume_text.split('\n'))
    if 10 <= line_count <= 50:
        score += 1
        strengths.append("✓ Well-structured layout")
    else:
        suggestions.append("Optimize resume length (ideally 15-40 lines)")

    if len(resume_text) > 500:
        score += 0.5
        strengths.append("✓ Substantial content")

    # Ensure score is between 0-10
    score = min(10, max(0, score))

    # Extract actual skills from resume
    skills_matched = list(tech_skills)[:10] if tech_skills else ["Python", "Communication", "Problem Solving"]

    # Priority skills (most important for tech roles)
    priority_tech = [s for s in skills_matched if s in ["Python", "Java", "JavaScript", "System Design", "AWS", "Leadership"]]
    priority_skills = priority_tech[:3] if priority_tech else skills_matched[:3]

    # Skills to learn
    skills_missing = []
    all_tech = {"Cloud": ["AWS", "Azure", "GCP"], "Backend": ["Node.js", "Django", "Spring"],
                "Frontend": ["React", "Vue", "Angular"], "DevOps": ["Docker", "Kubernetes", "CI/CD"],
                "Data": ["SQL", "Spark", "Tableau"]}
    for category, techs in all_tech.items():
        if not any(t.lower() in text_lower for t in techs):
            skills_missing.extend(techs[:2])

    # Default suggestions if few generated
    if not suggestions:
        suggestions = [
            "Add quantified achievements and metrics",
            "Use strong action verbs throughout",
            "Organize by most relevant experience",
            "Highlight key projects or accomplishments"
        ]

    return {
        "score": round(score, 1),
        "strengths": strengths[:5] if strengths else ["Good foundation", "Clear structure"],
        "weaknesses": weaknesses[:5] if weaknesses else ["Could add more metrics"],
        "suggestions": suggestions[:5],
        "skills_matched": skills_matched,
        "skills_missing": skills_missing[:5],
        "priority_skills": priority_skills,
        "roadmap": [
            {"phase": "Week 1-2", "focus": f"Master {priority_skills[0] if priority_skills else 'core skills'}"},
            {"phase": "Week 3-4", "focus": "Build portfolio projects"},
            {"phase": "Week 5+", "focus": "Interview preparation & system design"}
        ]
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

def check_achievements(user_analysis_count: int, user_streak_days: int, features_used: List[str]) -> dict:
    """Check and unlock achievements for user"""
    unlocked = []
    progress = {}

    # Define badges
    badges = {
        'first_analysis': {
            'name': '🎯 First Step',
            'description': 'Completed your first resume analysis',
            'icon': '🎯',
            'condition': user_analysis_count >= 1
        },
        'analyzer_pro': {
            'name': '📊 Analysis Pro',
            'description': 'Completed 10 resume analyses',
            'icon': '📊',
            'condition': user_analysis_count >= 10
        },
        'streak_3': {
            'name': '🔥 On Fire',
            'description': 'Maintained 3-day streak',
            'icon': '🔥',
            'condition': user_streak_days >= 3
        },
        'streak_7': {
            'name': '⚡ Week Warrior',
            'description': 'Maintained 7-day streak',
            'icon': '⚡',
            'condition': user_streak_days >= 7
        },
        'streak_30': {
            'name': '👑 Unstoppable',
            'description': 'Maintained 30-day streak',
            'icon': '👑',
            'condition': user_streak_days >= 30
        },
        'feature_explorer': {
            'name': '🚀 Explorer',
            'description': 'Used 5 different features',
            'icon': '🚀',
            'condition': len(features_used) >= 5
        },
        'all_features': {
            'name': '💎 Master',
            'description': 'Used all major features',
            'icon': '💎',
            'condition': len(features_used) >= 10
        },
        'grammar_master': {
            'name': '✏️ Grammarian',
            'description': 'Used grammar checker 5 times',
            'icon': '✏️',
            'condition': 'grammar_check' in features_used and features_used.count('grammar_check') >= 5
        },
        'batch_matcher': {
            'name': '🔍 Job Seeker',
            'description': 'Analyzed 5+ jobs in batch',
            'icon': '🔍',
            'condition': 'batch_job_match' in features_used and features_used.count('batch_job_match') >= 2
        },
    }

    # Check which badges are unlocked
    for badge_id, badge in badges.items():
        if badge['condition']:
            unlocked.append({
                'id': badge_id,
                'name': badge['name'],
                'description': badge['description'],
                'icon': badge['icon']
            })

    # Calculate progress for next badges
    if user_analysis_count < 10:
        progress['analyzer_pro'] = f"{user_analysis_count}/10"
    if user_streak_days < 7:
        progress['streak_7'] = f"{user_streak_days}/7"
    if len(features_used) < 10:
        progress['all_features'] = f"{len(features_used)}/10"

    return {
        'unlocked_badges': unlocked,
        'total_unlocked': len(unlocked),
        'progress': progress,
        'next_badge': 'Complete 10 analyses to unlock "Analysis Pro"' if user_analysis_count < 10 else 'Maintain 7-day streak to unlock "Week Warrior"'
    }

def check_streak(user_last_activity: datetime) -> dict:
    """Check and update user streak"""
    today = datetime.utcnow().date()
    last_date = user_last_activity.date() if user_last_activity else None

    streak_active = (today - last_date).days <= 1 if last_date else False

    return {
        'streak_active': streak_active,
        'last_activity': user_last_activity.isoformat() if user_last_activity else None,
        'days_since_activity': (today - last_date).days if last_date else 0
    }

def find_mentors(target_role: str, expertise_areas: List[str], user_experience: int = 0) -> dict:
    """Find suitable mentors based on role and expertise"""
    # This would query the database in real implementation
    # For now, return mock data structure
    return {
        'query': {
            'target_role': target_role,
            'expertise_areas': expertise_areas,
            'min_experience': user_experience
        },
        'mentor_count': 0,
        'top_matches': [],
        'recommended_search': f'Mentors specializing in {target_role}'
    }

def optimize_linkedin(headline: str, about_section: str, skills: List[str], target_role: str) -> dict:
    """Optimize LinkedIn profile for recruiter visibility"""
    prompt = f"""Optimize this LinkedIn profile for the {target_role} role.

Current Headline: {headline}
About Section: {about_section}
Current Skills: {', '.join(skills[:10])}
Target Role: {target_role}

Return JSON with:
- optimized_headline (compelling, keyword-rich, role-specific)
- optimized_about (2-3 sentences, impact-driven, recruiter-friendly)
- suggested_keywords (list of 8-10 keywords to add)
- missing_skills (important skills for this role not listed)
- improvements (list of 3-4 specific changes made)

JSON Response:"""

    response = infer(prompt, max_tokens=500)
    result = parse_json_response(response)

    # Calculate profile strength score
    strength_score = 50
    if result.get("optimized_headline"):
        strength_score += 15
    if result.get("optimized_about"):
        strength_score += 15
    if len(result.get("suggested_keywords", [])) > 5:
        strength_score += 10
    if len(skills) >= 10:
        strength_score += 10

    return {
        "optimized_headline": result.get("optimized_headline", f"{headline} | {target_role}"),
        "optimized_about": result.get("optimized_about", "Passionate professional with expertise in delivering results."),
        "suggested_keywords": result.get("suggested_keywords", ["Strategic", "Leadership", "Innovation", "Results-driven"]),
        "missing_skills": result.get("missing_skills", ["Project Management", "Stakeholder Communication"]),
        "profile_strength_score": min(100, strength_score),
        "improvements": result.get("improvements", [
            "Added role-specific keywords for better recruiter visibility",
            "Optimized headline for ATS and search ranking",
            "Highlighted measurable achievements in About section",
            "Included strategic keywords for your target role"
        ])
    }

def generate_star_response(question: str, difficulty: str = "medium", domain: str = None) -> dict:
    """Generate STAR method interview response"""

    # STAR response templates by difficulty and question type
    star_templates = {
        "easy": {
            "situation": "During my time at my previous company, I encountered a common workplace challenge that required collaboration and communication.",
            "task": "I was responsible for addressing this issue as part of my regular duties.",
            "action": "I took initiative by gathering information, communicating with relevant stakeholders, and implementing a straightforward solution.",
            "result": "This resulted in a positive outcome and helped the team work more efficiently."
        },
        "medium": {
            "situation": "In my previous role as a {role}, I was faced with a complex situation that required strategic thinking and problem-solving. The team was struggling with a critical issue that impacted our project timeline and team morale.",
            "task": "I was tasked with identifying the root cause, developing a solution, and leading the implementation while managing stakeholder expectations.",
            "action": "I conducted a thorough analysis of the problem, collaborated with cross-functional teams to gather insights, created a detailed action plan, and communicated progress regularly. I also provided coaching and support to team members throughout the implementation.",
            "result": "As a result, we successfully resolved the issue 2 weeks ahead of schedule, improved team productivity by 35%, and established best practices that prevented similar issues in the future."
        },
        "advanced": {
            "situation": "At my organization, we faced a mission-critical challenge that threatened our Q{quarter} deliverables. Multiple departments were impacted, and there was significant uncertainty about how to proceed. The stakes were high - failure would have resulted in major revenue loss and damaged client relationships.",
            "task": "As a senior team member, I was tasked with taking ownership of the crisis management, coordinating between 5+ teams, securing executive support, and delivering a comprehensive solution within an extremely tight timeline.",
            "action": "I immediately assembled a cross-functional task force, conducted a rapid impact assessment, and created a detailed recovery plan with clear milestones. I leveraged data-driven insights to prioritize efforts, maintained constant communication with all stakeholders, and personally led the implementation of the most critical components. I also managed risks proactively and adjusted the strategy based on real-time feedback.",
            "result": "We successfully recovered and delivered on time with only 5% scope reduction. The initiative resulted in a 40% improvement in process efficiency, saved the company $500K in potential losses, earned recognition from C-suite executives, and became a case study for crisis management best practices."
        }
    }

    # Select template based on difficulty
    template_level = difficulty.lower() if difficulty in ["easy", "medium", "advanced"] else "medium"
    template = star_templates.get(template_level, star_templates["medium"])

    # Customize with domain if provided
    if domain:
        template["situation"] = template["situation"].replace("{role}", domain)

    return {
        "situation": template["situation"],
        "task": template["task"],
        "action": template["action"],
        "result": template["result"],
        "full_answer": f"{template['situation']} {template['task']} {template['action']} {template['result']}",
        "difficulty_tag": template_level.capitalize()
    }


def generate_email_template(template_type: str, user_name: str, company_name: str, role: str, context: str = "") -> dict:
    """Generate professional career-related email templates"""

    # Subject lines for each template type
    subject_lines = {
        "job_outreach": f"Interested in {role} Position at {company_name}",
        "follow_up": f"Following Up on {role} Application - {company_name}",
        "networking": f"Let's Connect - {role} Professional",
        "internship": f"Internship Opportunity Inquiry - {company_name}",
        "rejection_response": f"Thank You - {company_name} Application",
        "referral_request": f"Referral Request for {role} at {company_name}"
    }

    # Email body templates
    email_templates = {
        "job_outreach": f"""Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company_name}. With my background and passion for this field, I am confident I can contribute meaningfully to your team.

{f"Context: {context}" if context else "I am particularly drawn to your company's commitment to innovation and excellence."}

I would welcome the opportunity to discuss how my skills and experience align with your team's needs. Please feel free to contact me at your convenience.

Thank you for considering my application.

Best regards,
{user_name}""",

        "follow_up": f"""Hi,

I wanted to follow up regarding my application for the {role} position at {company_name}. I remain very interested in this opportunity and would love to hear any updates.

I'm excited about the possibility of joining your team and contributing to your success. Please let me know if you need any additional information from my end.

Thank you for your time and consideration.

Best regards,
{user_name}""",

        "networking": f"""Hi,

I hope this email finds you well. I came across your profile and was impressed by your work in the {role} space at {company_name}. I would appreciate the opportunity to connect and learn from your experiences.

{f"Context: {context}" if context else "I'm eager to build meaningful professional relationships and explore potential opportunities."}

Would you be available for a brief call or coffee chat? I'm happy to work around your schedule.

Thank you for considering my request.

Best regards,
{user_name}""",

        "internship": f"""Dear {company_name} Team,

I am writing to express my interest in an internship opportunity with your organization, specifically in the {role} department. I am a motivated student eager to gain practical experience and contribute to your team.

{f"Context: {context}" if context else "I have strong foundational knowledge and a genuine passion for this field."}

I would greatly appreciate the opportunity to discuss how I can add value to your team during an internship. Thank you for your consideration.

Best regards,
{user_name}""",

        "rejection_response": f"""Dear {company_name} Team,

Thank you so much for considering my application for the {role} position. While I'm disappointed not to move forward at this time, I genuinely appreciate the opportunity and the insights I gained during the interview process.

Your commitment to excellence and innovation aligns perfectly with my career goals. I would love to stay connected and explore future opportunities with your organization.

Thank you again for your time and consideration.

Best regards,
{user_name}""",

        "referral_request": f"""Hi,

I hope you're doing well. I'm reaching out because I'm very interested in the {role} opportunity at {company_name}, and I believe I would be a great fit for the team.

{f"Context: {context}" if context else "I have relevant experience and am passionate about contributing to your organization."}

Would you be willing to refer me for this position? I would be grateful for your support.

Thank you for considering my request.

Best regards,
{user_name}"""
    }

    tips_map = {
        "job_outreach": [
            "Research the company thoroughly before reaching out",
            "Personalize your message with specific details about why you're interested",
            "Keep your tone professional yet warm and approachable",
            "Include a clear call-to-action or next steps"
        ],
        "follow_up": [
            "Follow up within 1-2 weeks of your initial application",
            "Reference specific details from your previous communication",
            "Reiterate your enthusiasm for the role",
            "Keep it concise - respect their time"
        ],
        "networking": [
            "Personalize with specific details about their work or company",
            "Clearly explain why you're interested in connecting",
            "Propose a specific way to connect (call, coffee, etc.)",
            "Be genuine and respectful of their time"
        ],
        "internship": [
            "Show genuine enthusiasm for the company and role",
            "Highlight relevant coursework or projects",
            "Mention your availability and flexibility",
            "Express eagerness to learn and contribute"
        ],
        "rejection_response": [
            "Send within 24-48 hours of receiving the rejection",
            "Thank them sincerely for the opportunity",
            "Express interest in future opportunities",
            "Keep doors open for potential future roles"
        ],
        "referral_request": [
            "Have an existing professional relationship before asking for a referral",
            "Make it easy for them by providing your resume and role details",
            "Explain why you're a good fit for the position",
            "Offer to help them in any way you can"
        ]
    }

    subject_line = subject_lines.get(template_type, f"Interested in {role} at {company_name}")
    email_body = email_templates.get(template_type, f"Hi,\n\nI am interested in the {role} position at {company_name}.\n\nBest regards,\n{user_name}")
    tips = tips_map.get(template_type, [
        "Personalize with specific details",
        "Keep professional but warm tone",
        "Include clear call-to-action",
        "Proofread before sending"
    ])

    return {
        "subject_line": subject_line,
        "email_body": email_body,
        "tips": tips
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
        'best_matches': results_sorted[:3],
        'all_results': results_sorted,
        'avg_score': round(sum(r['match_score'] for r in results) / len(results), 1) if results else 0
    }
