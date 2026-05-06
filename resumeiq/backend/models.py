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

class GrammarCheckRequest(BaseModel):
    resume: str

class GrammarCheckResult(BaseModel):
    grammar_score: float
    issues_found: int
    issues: List[dict]
    suggestions: List[str]
    overall_feedback: str

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
    format: str  # 'pdf' or 'docx'
