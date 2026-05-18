from fastapi import FastAPI, Depends, HTTPException, status, Header, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
import os
from dotenv import load_dotenv

from database import get_db, init_db, User, Analysis, Resume, InterviewSession, Achievement, UserStreak, ChatMessage
from models import (
    UserSignup, UserLogin, Token, UserResponse, AnalysisRequest, AnalysisResult,
    RewriteRequest, RewriteResult, MatchRequest, MatchResult, InterviewRequest,
    InterviewResult, InterviewAnswerRequest, InterviewAnswerResult, RoadmapRequest, RoadmapResult, CoverLetterRequest, CoverLetterResult, AnalysisHistory, ResumeInfo, CurrentResume,
    KeywordOptimizerRequest, KeywordOptimizerResult, ATSScoreRequest, ATSScoreResult,
    SkillGapRequest, SkillGapResult, ResumeComparisonRequest, ResumeComparisonResult,
    ResumeVersionRequest, ResumeVersionResult,
    BatchJobMatchRequest, BatchJobMatchResult, ResumeDownloadRequest, AchievementRequest, AchievementResult,
    LinkedInOptimizerRequest, LinkedInOptimizerResult, StarResponseRequest, StarResponseResult,
    EmailTemplateRequest, EmailTemplateResult, ChatRequest, ChatResponse, ChatHistory
)
from extract_text import extract_text_from_pdf
import inference

load_dotenv()

app = FastAPI(title="ResumeIQ API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(token: str, db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.on_event("startup")
async def startup_event():
    init_db()
    inference.load_model()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/auth/signup", response_model=Token)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    return user

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze(req: AnalysisRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.analyze_resume(req.text)

    analysis = Analysis(
        user_id=user.id,
        type="analyze",
        input_text=req.text[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/rewrite", response_model=RewriteResult)
async def rewrite(req: RewriteRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.rewrite_resume(req.text)

    analysis = Analysis(
        user_id=user.id,
        type="rewrite",
        input_text=req.text[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/generate-cover-letter", response_model=CoverLetterResult)
async def generate_cover_letter(req: CoverLetterRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.generate_cover_letter(req.job_description, req.resume)

    analysis = Analysis(
        user_id=user.id,
        type="cover_letter",
        input_text=req.job_description[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/match", response_model=MatchResult)
async def match(req: MatchRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.match_job(req.resume, req.job_description)

    analysis = Analysis(
        user_id=user.id,
        type="match",
        input_text=f"{req.resume[:250]}__{req.job_description[:250]}",
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/interview", response_model=InterviewResult)
async def interview(req: InterviewRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.interview_questions(req.role, req.resume or "")

    analysis = Analysis(
        user_id=user.id,
        type="interview",
        input_text=req.role,
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/interview/answer", response_model=InterviewAnswerResult)
async def evaluate_interview_answer(req: InterviewAnswerRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.evaluate_answer(req.role, req.question, req.answer)

    session = InterviewSession(
        user_id=user.id,
        role=req.role,
        question=req.question,
        answer=req.answer,
        score=int(result["score"]),
        feedback=result["feedback"]
    )
    db.add(session)
    db.commit()

    return result

@app.post("/api/roadmap", response_model=RoadmapResult)
async def roadmap(req: RoadmapRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.learning_roadmap(req.target_role, req.current_skills)

    analysis = Analysis(
        user_id=user.id,
        type="roadmap",
        input_text=f"{req.target_role}_{','.join(req.current_skills)}",
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.get("/api/history", response_model=list[AnalysisHistory])
async def get_history(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    analyses = db.query(Analysis).filter(Analysis.user_id == user.id).order_by(Analysis.timestamp.desc()).limit(50).all()
    return analyses

@app.post("/api/resumes/upload")
async def upload_resume(file: UploadFile = File(...), authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_bytes = await file.read()

    try:
        extracted_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text: {str(e)}")

    # Deactivate other resumes for this user
    db.query(Resume).filter(Resume.user_id == user.id).update({"is_active": False})

    # Create new resume
    resume = Resume(
        user_id=user.id,
        filename=file.filename,
        file_data=file_bytes,
        extracted_text=extracted_text,
        is_active=True
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"id": resume.id, "filename": resume.filename, "extracted_text": extracted_text[:200]}

@app.get("/api/resumes", response_model=list[ResumeInfo])
async def list_resumes(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    resumes = db.query(Resume).filter(Resume.user_id == user.id).order_by(Resume.created_at.desc()).all()
    return resumes

@app.get("/api/current-resume", response_model=Optional[CurrentResume])
async def get_current_resume(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)
    resume = db.query(Resume).filter(Resume.user_id == user.id, Resume.is_active == True).first()
    if not resume:
        return None
    return resume

@app.post("/api/resumes/{resume_id}/select")
async def select_resume(resume_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.query(Resume).filter(Resume.user_id == user.id).update({"is_active": False})
    resume.is_active = True
    db.commit()

    return {"success": True, "resume_id": resume.id}

@app.delete("/api/resumes/{resume_id}")
async def delete_resume(resume_id: int, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    db.delete(resume)
    db.commit()

    return {"success": True}

@app.post("/api/optimize-keywords", response_model=KeywordOptimizerResult)
async def optimize_keywords(req: KeywordOptimizerRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.optimize_keywords(req.resume, req.job_description)

    analysis = Analysis(
        user_id=user.id,
        type="keyword_optimizer",
        input_text=req.job_description[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/ats-score", response_model=ATSScoreResult)
async def check_ats_score(req: ATSScoreRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.check_ats_score(req.resume)

    analysis = Analysis(
        user_id=user.id,
        type="ats_score",
        input_text=req.resume[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/skill-gaps", response_model=SkillGapResult)
async def analyze_skill_gaps(req: SkillGapRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.analyze_skill_gaps(req.current_skills, req.target_role)

    analysis = Analysis(
        user_id=user.id,
        type="skill_gap_analyzer",
        input_text=req.target_role,
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/compare-resumes", response_model=ResumeComparisonResult)
async def compare_resumes(req: ResumeComparisonRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.compare_resumes(req.resume1, req.resume2)

    analysis = Analysis(
        user_id=user.id,
        type="resume_comparison",
        input_text="resume_comparison",
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/batch-match-jobs", response_model=BatchJobMatchResult)
async def batch_match_jobs(req: BatchJobMatchRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.batch_match_jobs(req.resume, req.job_descriptions)

    analysis = Analysis(
        user_id=user.id,
        type="batch_job_match",
        input_text=f"{req.resume[:200]}__{len(req.job_descriptions)}_jobs",
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/download-resume")
async def download_resume(req: ResumeDownloadRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    if req.format.lower() == 'pdf':
        pdf_buffer = inference.generate_resume_pdf(req.resume)
        return StreamingResponse(
            iter([pdf_buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=resume.pdf"}
        )
    elif req.format.lower() == 'docx':
        docx_buffer = inference.generate_resume_docx(req.resume)
        return StreamingResponse(
            iter([docx_buffer.getvalue()]),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=resume.docx"}
        )
    elif req.format.lower() == 'txt':
        txt_content = req.resume.encode('utf-8')
        return StreamingResponse(
            iter([txt_content]),
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=resume.txt"}
        )
    else:
        raise HTTPException(status_code=400, detail="Format must be 'pdf', 'docx', or 'txt'")

@app.post("/api/achievements", response_model=AchievementResult)
async def get_achievements(req: AchievementRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.check_achievements(req.analysis_count, req.streak_days, req.features_used)

    return result

@app.post("/api/linkedin-optimizer", response_model=LinkedInOptimizerResult)
async def optimize_linkedin(req: LinkedInOptimizerRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.optimize_linkedin(req.headline, req.about_section, req.skills, req.target_role)

    analysis = Analysis(
        user_id=user.id,
        type="linkedin_optimizer",
        input_text=req.target_role,
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/star-response", response_model=StarResponseResult)
async def generate_star_response(req: StarResponseRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.generate_star_response(req.question, req.difficulty, req.domain)

    analysis = Analysis(
        user_id=user.id,
        type="star_response",
        input_text=req.question[:500],
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/email-template", response_model=EmailTemplateResult)
async def generate_email_template(req: EmailTemplateRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    result = inference.generate_email_template(req.template_type, req.user_name, req.company_name, req.role, req.additional_context or "")

    analysis = Analysis(
        user_id=user.id,
        type="email_template",
        input_text=f"{req.template_type}_{req.company_name}",
        result=result
    )
    db.add(analysis)
    db.commit()

    return result

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    resume_context = {}
    if req.resume_context:
        resume_context = req.resume_context
    else:
        resume = db.query(Resume).filter(Resume.user_id == user.id, Resume.is_active == True).first()
        if resume:
            resume_context = {
                "extracted_text": resume.extracted_text,
                "filename": resume.filename
            }

    response = inference.career_copilot_chat(
        req.user_message,
        req.mode,
        resume_context,
        req.conversation_history or []
    )

    user_message = ChatMessage(
        user_id=user.id,
        mode=req.mode,
        role="user",
        content=req.user_message
    )
    db.add(user_message)

    assistant_message = ChatMessage(
        user_id=user.id,
        mode=req.mode,
        role="assistant",
        content=response["response"]
    )
    db.add(assistant_message)
    db.commit()

    return response

@app.get("/api/chat/history")
async def get_chat_history(mode: str, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id,
        ChatMessage.mode == mode
    ).order_by(ChatMessage.created_at).all()

    return {
        "mode": mode,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            }
            for m in messages
        ],
        "total_messages": len(messages)
    }

@app.delete("/api/chat/{mode}")
async def clear_chat_history(mode: str, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    db.query(ChatMessage).filter(
        ChatMessage.user_id == user.id,
        ChatMessage.mode == mode
    ).delete()
    db.commit()

    return {"success": True, "message": f"Chat history cleared for {mode}"}

@app.get("/api/user-badges")
async def get_user_badges(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    badges = db.query(Achievement).filter(Achievement.user_id == user.id).all()

    return {
        "total_badges": len(badges),
        "badges": [
            {
                "badge_name": b.badge_name,
                "description": b.description,
                "icon": b.icon,
                "unlocked_at": b.unlocked_at
            }
            for b in badges
        ]
    }

@app.get("/api/user-streak")
async def get_user_streak(authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    streak = db.query(UserStreak).filter(UserStreak.user_id == user.id).first()

    if not streak:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "total_activities": 0
        }

    return {
        "current_streak": streak.current_streak,
        "longest_streak": streak.longest_streak,
        "total_activities": streak.total_activities
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
