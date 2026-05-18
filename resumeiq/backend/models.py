from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class AnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

class AnalysisResult(BaseModel):
    score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    skills_matched: List[str]
    skills_missing: List[str]
    priority_skills: List[str]
    roadmap: List[dict]

class RewriteRequest(BaseModel):
    text: str

class RewriteResult(BaseModel):
    original: str
    rewritten: str
    improvements: List[str]

class MatchRequest(BaseModel):
    resume: str
    job_description: str

class MatchResult(BaseModel):
    match_score: float
    skills_matched: List[str]
    skills_missing: List[str]
    suggestions: List[str]

class InterviewRequest(BaseModel):
    role: str
    resume: Optional[str] = None

class InterviewResult(BaseModel):
    questions: List[str]
    tips: List[str]

class InterviewAnswerRequest(BaseModel):
    role: str
    question: str
    answer: str

class InterviewAnswerResult(BaseModel):
    score: float
    feedback: str
    better_answer: str

class RoadmapRequest(BaseModel):
    current_skills: List[str]
    target_role: str

class RoadmapResult(BaseModel):
    phases: List[dict]
    estimated_duration: str
    resources: List[str]

class CoverLetterRequest(BaseModel):
    job_description: str
    resume: str

class CoverLetterResult(BaseModel):
    cover_letter: str
    improvements: List[str]

class AnalysisHistory(BaseModel):
    id: int
    type: str
    timestamp: datetime
    result: dict

    class Config:
        from_attributes = True

class ResumeInfo(BaseModel):
    id: int
    filename: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class CurrentResume(BaseModel):
    id: int
    filename: str
    extracted_text: str
    is_active: bool

    class Config:
        from_attributes = True

class KeywordOptimizerRequest(BaseModel):
    resume: str
    job_description: str

class KeywordOptimizerResult(BaseModel):
    recommended_keywords: List[str]
    placement_suggestions: List[str]
    optimized_keywords: List[str]
    ats_improvements: List[str]
    keywords_matched: int
    keywords_missing: int

class ATSScoreRequest(BaseModel):
    resume: str

class ATSScoreResult(BaseModel):
    ats_score: float
    issues: List[str]
    suggestions: List[str]
    formatting_check: dict

class SkillGapRequest(BaseModel):
    current_skills: List[str]
    target_role: str

class SkillGapResult(BaseModel):
    role: str
    gaps: List[str]
    mastered_skills: List[str]
    additional_skills: List[str]
    gap_count: int
    coverage_percentage: int
    learning_priority: List[str]
    estimated_learning_time: str

class ResumeComparisonRequest(BaseModel):
    resume1: str
    resume2: str

class ResumeComparisonResult(BaseModel):
    comparison_summary: str
    resume1_strengths: List[str]
    resume2_strengths: List[str]
    common_skills: List[str]
    resume1_unique: List[str]
    resume2_unique: List[str]
    length_comparison: dict
    skills_comparison: dict

class ResumeVersionRequest(BaseModel):
    resume: str
    version_name: str
    description: Optional[str] = ""

class ResumeVersionResult(BaseModel):
    version_name: str
    description: str
    created_at: str
    content_preview: str
    word_count: int
    skills_identified: int

class BatchJobMatchRequest(BaseModel):
    resume: str
    job_descriptions: List[str]

class BatchJobMatchResult(BaseModel):
    total_jobs: int
    best_matches: List[dict]
    all_results: List[dict]
    avg_score: float

class ResumeDownloadRequest(BaseModel):
    resume: str
    format: str  # 'pdf', 'docx', or 'txt'

class AchievementRequest(BaseModel):
    analysis_count: int
    streak_days: int
    features_used: List[str]

class AchievementResult(BaseModel):
    unlocked_badges: List[dict]
    total_unlocked: int
    progress: dict
    next_badge: str

class LinkedInOptimizerRequest(BaseModel):
    headline: str
    about_section: str
    skills: List[str]
    target_role: str

class LinkedInOptimizerResult(BaseModel):
    optimized_headline: str
    optimized_about: str
    suggested_keywords: List[str]
    missing_skills: List[str]
    profile_strength_score: float
    improvements: List[str]

class StarResponseRequest(BaseModel):
    question: str
    difficulty: str = "medium"
    domain: Optional[str] = None

class StarResponseResult(BaseModel):
    situation: str
    task: str
    action: str
    result: str
    full_answer: str
    difficulty_tag: str

class EmailTemplateRequest(BaseModel):
    template_type: str
    user_name: str
    company_name: str
    role: str
    additional_context: Optional[str] = None

class EmailTemplateResult(BaseModel):
    subject_line: str
    email_body: str
    tips: List[str]

class ChatRequest(BaseModel):
    user_message: str
    mode: str  # resume_expert, career_mentor, interview_coach
    resume_context: Optional[dict] = None
    conversation_history: Optional[List[dict]] = None

class ChatResponse(BaseModel):
    response: str
    mode: str
    word_count: int
    timestamp: str
    error: Optional[str] = None

class ChatMessage(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistory(BaseModel):
    mode: str
    messages: List[ChatMessage]
    total_messages: int

class PortfolioItemRequest(BaseModel):
    title: str
    description: str
    technologies: List[str]
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    domain: str

class PortfolioItemResult(BaseModel):
    id: int
    title: str
    description: str
    technologies: List[str]
    github_link: Optional[str]
    demo_link: Optional[str]
    domain: str
    created_at: datetime

class PortfolioShowcaseRequest(BaseModel):
    domain: Optional[str] = None

class PortfolioShowcaseResult(BaseModel):
    projects: List[PortfolioItemResult]
    total_count: int
    domains: List[str]
