"""
Progress tracking for resume analyses
Stores and retrieves analysis history
"""

from db import add_analysis_record, get_analysis_history, get_latest_analysis, get_score_statistics
import json

def add_score_record(user_id: str, score: int, target_role: str, filename: str,
                     resume_text: str, analysis_data: dict):
    """
    Store analysis to database

    Args:
        user_id: User ID
        score: Resume score (1-10)
        target_role: Target job role
        filename: Resume filename
        resume_text: Full resume text
        analysis_data: Full analysis dict
    """
    resume_preview = resume_text[:500] if resume_text else ""
    return add_analysis_record(user_id, score, target_role, filename, resume_preview, analysis_data)

def get_score_history(user_id: str, limit: int = 20):
    """Get user's analysis history"""
    records = get_analysis_history(user_id, limit)

    # Parse JSON data and convert timestamps
    for record in records:
        if record.get('full_analysis'):
            try:
                record['full_analysis'] = json.loads(record['full_analysis'])
            except:
                pass

    return records

def get_improvement_percentage(user_id: str):
    """
    Calculate improvement from first to latest score

    Returns:
        {"improvement": float, "first_score": int, "latest_score": int}
    """
    records = get_analysis_history(user_id, limit=1000)  # Get all

    if not records:
        return {"improvement": 0, "first_score": 0, "latest_score": 0}

    # Reverse to get chronological order (oldest first)
    records = list(reversed(records))

    first_score = records[0]['score']
    latest_score = records[-1]['score']

    if first_score == 0:
        improvement = 0
    else:
        improvement = ((latest_score - first_score) / first_score) * 100

    return {
        "improvement": round(improvement, 1),
        "first_score": first_score,
        "latest_score": latest_score,
        "total_analyses": len(records)
    }

def get_score_trend_data(user_id: str, limit: int = 12):
    """
    Get score trend data for charting (recent scores)

    Returns:
        List of {"date": str, "score": int, "role": str}
    """
    records = get_analysis_history(user_id, limit=limit)

    trend_data = []
    for record in reversed(records):  # Oldest first
        trend_data.append({
            "date": record['timestamp'].split(' ')[0],  # Just date part
            "score": record['score'],
            "role": record.get('target_role', 'General')
        })

    return trend_data

def get_statistics(user_id: str):
    """
    Get analysis statistics

    Returns:
        {"total_analyses": int, "avg_score": float, "max_score": int, "min_score": int}
    """
    stats = get_score_statistics(user_id)

    if not stats:
        return {
            "total_analyses": 0,
            "avg_score": 0,
            "max_score": 0,
            "min_score": 0
        }

    return {
        "total_analyses": stats['total_analyses'] or 0,
        "avg_score": round(stats['avg_score'] or 0, 1),
        "max_score": stats['max_score'] or 0,
        "min_score": stats['min_score'] or 0
    }

def get_latest_analysis_data(user_id: str):
    """Get most recent analysis with parsed data"""
    record = get_latest_analysis(user_id)

    if not record:
        return None

    # Parse JSON
    if record.get('full_analysis'):
        try:
            record['full_analysis'] = json.loads(record['full_analysis'])
        except:
            pass

    return record
