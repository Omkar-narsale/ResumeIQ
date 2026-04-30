"""
Interview Module
Handles interview question generation and answer evaluation
"""

from utils.llm_handler import get_llm_handler


def generate_question(role: str, question_count: int = 1) -> str:
    """
    Generate an interview question for a given role

    Args:
        role: Job role/position
        question_count: Number of questions asked so far (for variety)

    Returns:
        Generated interview question
    """
    llm = get_llm_handler()

    prompt = f"""Generate a professional interview question for a {role} position.

This is question #{question_count}.
Make it specific to the role, not generic.
Return ONLY the question, nothing else."""

    system_prompt = "You are an experienced technical interviewer. Generate thoughtful, challenging interview questions."

    return llm.ask_claude(prompt, system_prompt)


def evaluate_answer(answer: str, question: str, role: str) -> dict:
    """
    Evaluate an interview answer and provide feedback

    Args:
        answer: User's answer to the interview question
        question: The interview question asked
        role: Job role context

    Returns:
        Dictionary with feedback and improved answer
    """
    llm = get_llm_handler()

    prompt = f"""Evaluate this interview answer for a {role} position.

Question: {question}

Answer: {answer}

Provide structured feedback in this exact format:
SCORE: [score out of 10]
FEEDBACK: [specific, constructive feedback]
IMPROVED_ANSWER: [an example of a better response]"""

    system_prompt = "You are an expert technical interviewer and mentor. Evaluate answers fairly and provide constructive feedback."

    response = llm.ask_claude(prompt, system_prompt)

    # Parse the response
    feedback_dict = parse_evaluation_response(response)
    return feedback_dict


def parse_evaluation_response(response: str) -> dict:
    """
    Parse the structured evaluation response from Claude

    Args:
        response: Raw response from Claude

    Returns:
        Dictionary with parsed feedback components
    """
    result = {
        "score": "N/A",
        "feedback": "",
        "improved_answer": ""
    }

    lines = response.split("\n")
    current_section = None
    current_content = []

    for line in lines:
        if line.startswith("SCORE:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            result["score"] = line.replace("SCORE:", "").strip()
            current_section = None
            current_content = []
        elif line.startswith("FEEDBACK:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "feedback"
            current_content = [line.replace("FEEDBACK:", "").strip()]
        elif line.startswith("IMPROVED_ANSWER:"):
            if current_section and current_content:
                result[current_section] = "\n".join(current_content).strip()
            current_section = "improved_answer"
            current_content = [line.replace("IMPROVED_ANSWER:", "").strip()]
        elif current_section and line.strip():
            current_content.append(line)

    # Add remaining content
    if current_section and current_content:
        result[current_section] = "\n".join(current_content).strip()

    return result
