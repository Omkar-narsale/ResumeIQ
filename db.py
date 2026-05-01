"""
Database management for ResumeIQ
Handles SQLite setup and connection
"""

import sqlite3
import os
from datetime import datetime
import json

DB_PATH = "resumeiq.db"

def get_connection():
    """Get SQLite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME
        )
    """)

    # Analysis history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            score INTEGER NOT NULL,
            target_role TEXT,
            filename TEXT,
            resume_preview TEXT,
            full_analysis TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_timestamp
        ON analysis_history(user_id, timestamp DESC)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_user_email
        ON users(email)
    """)

    conn.commit()
    conn.close()

def add_user(email: str, password_hash: str) -> str:
    """
    Add new user to database

    Args:
        email: User email
        password_hash: Hashed password

    Returns:
        User ID
    """
    import uuid
    user_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (id, email, password_hash)
            VALUES (?, ?, ?)
        """, (user_id, email, password_hash))
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email: str):
    """Get user by email"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def get_user_by_id(user_id: str):
    """Get user by ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def update_last_login(user_id: str):
    """Update last login time"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET last_login = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (user_id,))
    conn.commit()
    conn.close()

def add_analysis_record(user_id: str, score: int, target_role: str,
                       filename: str, resume_preview: str, analysis_data: dict):
    """
    Store analysis in database

    Args:
        user_id: User ID
        score: Resume score (1-10)
        target_role: Target job role
        filename: Resume filename
        resume_preview: First 500 chars of resume
        analysis_data: Full analysis dict

    Returns:
        Analysis ID
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis_history
        (user_id, score, target_role, filename, resume_preview, full_analysis)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, score, target_role, filename, resume_preview[:500], json.dumps(analysis_data)))

    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()

    return analysis_id

def get_analysis_history(user_id: str, limit: int = 20):
    """Get user's analysis history"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM analysis_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, limit))

    records = cursor.fetchall()
    conn.close()

    return [dict(r) for r in records]

def get_latest_analysis(user_id: str):
    """Get most recent analysis"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM analysis_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (user_id,))

    record = cursor.fetchone()
    conn.close()

    if record:
        result = dict(record)
        # Parse JSON analysis data
        if result['full_analysis']:
            result['full_analysis'] = json.loads(result['full_analysis'])
        return result
    return None

def get_score_statistics(user_id: str):
    """Get score statistics for user"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) as total_analyses,
            AVG(score) as avg_score,
            MAX(score) as max_score,
            MIN(score) as min_score
        FROM analysis_history
        WHERE user_id = ?
    """, (user_id,))

    stats = cursor.fetchone()
    conn.close()

    return dict(stats) if stats else None

# Initialize database on import
if not os.path.exists(DB_PATH):
    init_db()
