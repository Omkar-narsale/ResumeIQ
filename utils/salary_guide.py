"""
Salary guide and market information
"""

import json
import os

SALARY_DATA_PATH = "data/salaries.json"

def load_salary_data():
    """Load salary data from JSON"""
    if not os.path.exists(SALARY_DATA_PATH):
        return {}

    with open(SALARY_DATA_PATH, 'r') as f:
        return json.load(f)

def normalize_role(role: str) -> str:
    """Normalize role name to match data keys"""
    role_lower = role.lower()

    # Map common role variations
    role_map = {
        "data analyst": "data_analyst",
        "analyst": "data_analyst",
        "software engineer": "software_engineer",
        "engineer": "software_engineer",
        "developer": "software_engineer",
        "ml engineer": "ml_engineer",
        "machine learning engineer": "ml_engineer",
        "frontend": "frontend_developer",
        "frontend developer": "frontend_developer",
        "backend": "backend_developer",
        "backend developer": "backend_developer",
        "devops": "devops_engineer",
        "devops engineer": "devops_engineer",
        "product manager": "product_manager",
        "pm": "product_manager",
        "data scientist": "data_scientist",
        "scientist": "data_scientist",
        "marketing manager": "marketing_manager",
        "sales engineer": "sales_engineer"
    }

    # Check exact matches first
    for key in role_map:
        if key in role_lower:
            return role_map[key]

    # Return original if no match
    return role_lower.replace(" ", "_")

def get_salary_range(role: str, level: str = "mid_level") -> dict:
    """
    Get salary range for role and level

    Args:
        role: Job role (e.g., "Data Analyst", "Software Engineer")
        level: "entry_level", "mid_level", or "senior"

    Returns:
        {"min": int, "avg": int, "max": int, "level": str}
    """
    data = load_salary_data()
    normalized_role = normalize_role(role)

    if normalized_role not in data:
        return {
            "min": 0,
            "avg": 0,
            "max": 0,
            "level": level,
            "error": f"Role '{role}' not found in database"
        }

    role_data = data[normalized_role]

    if level not in role_data:
        level = "mid_level"  # Default

    salary_data = role_data[level]

    return {
        "min": salary_data.get("min", 0),
        "avg": salary_data.get("avg", 0),
        "max": salary_data.get("max", 0),
        "level": level
    }

def get_negotiation_tips(role: str) -> list:
    """Get negotiation tips for role"""
    data = load_salary_data()
    normalized_role = normalize_role(role)

    if normalized_role not in data:
        return ["Research market rates before negotiating",
                "Don't reveal previous salary",
                "Ask for 10-20% increase if you have offers"]

    role_data = data[normalized_role]
    return role_data.get("negotiation_tips", [])

def get_all_roles() -> list:
    """Get list of all available roles"""
    data = load_salary_data()
    return list(data.keys())

def get_market_trends() -> dict:
    """Get market trends by role"""
    data = load_salary_data()

    trends = {}
    for role, role_data in data.items():
        mid_salary = role_data.get("mid_level", {}).get("avg", 0)
        trends[role.replace("_", " ").title()] = mid_salary

    # Sort by salary
    return dict(sorted(trends.items(), key=lambda x: x[1], reverse=True))

def calculate_compensation_increase(current_salary: float, role: str, level: str = "mid_level") -> dict:
    """
    Calculate potential salary increase based on market rate

    Args:
        current_salary: Current salary
        role: Target role
        level: Target level

    Returns:
        {"current": float, "market_avg": float, "increase_amount": float, "increase_percent": float}
    """
    salary_range = get_salary_range(role, level)

    if salary_range.get("error"):
        return {"error": salary_range["error"]}

    market_avg = salary_range["avg"]
    increase_amount = market_avg - current_salary
    increase_percent = (increase_amount / current_salary * 100) if current_salary > 0 else 0

    return {
        "current": current_salary,
        "market_avg": market_avg,
        "increase_amount": max(0, increase_amount),
        "increase_percent": max(0, increase_percent)
    }
