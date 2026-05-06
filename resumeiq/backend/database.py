from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, ForeignKey, Index, Text, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resumeiq.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("Analysis", back_populates="user")
    resumes = relationship("Resume", back_populates="user")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # analyze, match, rewrite, interview
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    input_text = Column(String)
    result = Column(JSON)

    user = relationship("User", back_populates="analyses")

    __table_args__ = (
        Index("idx_user_timestamp", "user_id", "timestamp"),
    )

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_data = Column(LargeBinary)  # PDF bytes stored as BLOB
    extracted_text = Column(Text)    # Extracted text from PDF
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="resumes")

    __table_args__ = (
        Index("idx_user_active", "user_id", "is_active"),
    )

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)
    question = Column(String)
    answer = Column(Text)
    score = Column(Integer)  # 0-10
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User")

    __table_args__ = (
        Index("idx_user_interview", "user_id", "created_at"),
    )

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_type = Column(String)  # first_analysis, streak_7, all_features, etc
    badge_name = Column(String)
    description = Column(String)
    icon = Column(String)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class UserStreak(Base):
    __tablename__ = "user_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    total_activities = Column(Integer, default=0)

    user = relationship("User")

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    expertise = Column(String)  # JSON-like string of expertise areas
    bio = Column(Text)
    years_experience = Column(Integer)
    hourly_rate = Column(Integer, default=0)  # 0 = free
    availability = Column(String)  # available_now, weekends, etc
    is_verified = Column(Boolean, default=False)
    rating = Column(Integer, default=0)  # 0-5
    total_mentees = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class MentorConnection(Base):
    __tablename__ = "mentor_connections"

    id = Column(Integer, primary_key=True, index=True)
    mentee_id = Column(Integer, ForeignKey("users.id"))
    mentor_id = Column(Integer, ForeignKey("mentors.id"))
    status = Column(String, default="pending")  # pending, connected, completed
    goal = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    messages_count = Column(Integer, default=0)

    mentee = relationship("User")
    mentor = relationship("Mentor")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("[OK] Database initialized")
