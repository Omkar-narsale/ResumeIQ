# ResumeIQ - Dynamic Resume Analyzer

## Overview

The Resume Analyzer uses **skill extraction and matching** to provide realistic, variable responses based on actual resume vs job description content.

---

## How It Works

### 1. **Skill Extraction**
Extracts skills from both resume and job description using pattern matching against 60+ common skills:

- **Programming:** Python, JavaScript, Java, C#, C++, Rust, Go, PHP, Ruby, Kotlin, Swift, TypeScript
- **Frontend:** React, Vue, Angular, HTML, CSS, Sass, Webpack, Jest
- **Backend:** Node.js, Django, Flask, Spring, FastAPI, Express, Laravel
- **Databases:** SQL, PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Elasticsearch
- **Data/ML:** Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Keras, Spark, Tableau, PowerBI
- **DevOps:** AWS, GCP, Azure, Docker, Kubernetes, Jenkins, GitHub, Terraform, Ansible
- **Soft Skills:** Communication, Leadership, Project Management, Problem Solving

### 2. **Dynamic Score Calculation**

Score is calculated based on **% match**:

```python
Job skills = 10
Resume skills matched = 7
Match percentage = 70%

Score logic:
- Missing 0-20% → 8-10
- Missing 20-50% → 6-8
- Missing 50-70% → 5-7
- Missing 70%+ → 3-5
```

### 3. **Context-Aware Suggestions**

Suggestions are generated based on:
- Job title (Senior, Startup, etc.)
- Technology stack (Cloud, ML, etc.)
- Missing critical skills
- Experience gaps

---

## Example 1: Strong Match

**Resume:**
```
Senior Python Developer with 5 years experience
Skills: Python, Django, PostgreSQL, Docker, AWS, REST APIs
Projects: Built microservices using Python and Kubernetes
```

**Job Description:**
```
Senior Backend Engineer - Python
Requirements: Python, Django, PostgreSQL, Docker, AWS, Microservices
Preferred: Kubernetes, Redis
```

**Output:**
```
Score: 8.5/10

Strengths:
• Python development expertise
• Django backend framework
• PostgreSQL database design
• Docker containerization
• AWS cloud platform
• Microservices architecture

Skills Missing:
• Redis (preferred skill)

Suggestions:
• Add Redis experience or certification to strengthen candidacy
• Highlight specific metrics from microservices projects
• Include links to GitHub projects showing Docker and Kubernetes work
• Mention team size and business impact of projects
```

---

## Example 2: Medium Match

**Resume:**
```
Junior Full-Stack Developer
Skills: JavaScript, React, HTML, CSS
Experience: Built 3 web applications, familiar with Git
```

**Job Description:**
```
Full-Stack Developer
Required: JavaScript, React, Node.js, MongoDB, SQL
Nice to have: Docker, AWS, GraphQL
```

**Output:**
```
Score: 5.2/10

Strengths:
• JavaScript programming
• React frontend framework
• Git version control

Skills Missing:
• Node.js backend framework
• MongoDB database
• SQL databases
• Docker containerization
• AWS cloud

Suggestions:
• Learn Node.js to complete full-stack capabilities
• Take courses on MongoDB and SQL for database skills
• Add backend project using Node.js and Express to resume
• Include portfolio link with full-stack project examples
```

---

## Example 3: Low Match

**Resume:**
```
Data Analyst
Skills: Excel, SQL, Tableau
Experience: 2 years in data analytics
```

**Job Description:**
```
Machine Learning Engineer (Senior)
Required: Python, TensorFlow, PyTorch, SQL, AWS, Linux
Experience: 5+ years in ML/AI
```

**Output:**
```
Score: 3.1/10

Strengths:
• SQL database querying
• Data analysis background

Skills Missing:
• Python programming language
• TensorFlow deep learning framework
• PyTorch framework
• AWS cloud services
• Linux operating system
• Machine learning fundamentals

Suggestions:
• This role requires ML expertise - consider Python bootcamp first
• Build foundational ML projects with TensorFlow/PyTorch
• Gain AWS experience through hands-on projects
• Consider ML Engineer transition path rather than direct application
```

---

## Key Features

✅ **Realistic Scoring**
- Not fixed values (7 every time)
- Based on actual skill match percentage
- Adjusts for number and criticality of missing skills

✅ **Variable Output**
- Different resume = Different analysis
- Context-aware suggestions
- Specific missing skills identified

✅ **No Generic Phrases**
- Uses extracted actual skills
- References specific job requirements
- Tailored to role and industry

✅ **Fast & Accurate**
- Regex-based skill extraction (no LLM needed)
- Instant analysis
- Highly accurate for common skills

---

## Integration

### API Endpoint

```bash
POST /api/match
Content-Type: application/json

{
  "resume": "Senior Python Developer...",
  "job_description": "Backend Engineer - Python..."
}

Response:
{
  "match_score": 8.5,
  "skills_matched": ["python", "django", "postgresql"],
  "skills_missing": ["redis"],
  "suggestions": [
    "Add Redis experience...",
    "Highlight specific metrics...",
    "Include GitHub projects..."
  ],
  "match_percentage": 85
}
```

---

## Testing

To test with your own resume and job description:

```python
from inference import match_job

result = match_job(
    resume_text="Your resume here...",
    job_description="Job description here..."
)

print(f"Score: {result['match_score']}/10")
print(f"Matched: {result['skills_matched']}")
print(f"Missing: {result['skills_missing']}")
print(f"Suggestions: {result['suggestions']}")
```

---

## Future Enhancements

- Add industry-specific skills database
- Machine learning for experience level matching
- Certification recognition
- Project complexity analysis
- Salary range estimation based on skills

