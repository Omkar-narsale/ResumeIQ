"""
PARSING LOGIC - How One LLM Response Becomes 8 Sections
========================================================

The unified_analysis.py parser handles raw LLM text like this:

INPUT (LLM Response - Plain Text):
---
Score: 8/10

Matched_Skills: Python, SQL, Excel, Power BI

Missing_Skills: Tableau, Statistics

Priority_Skills: Statistics, Tableau

Strengths: Strong SQL foundations | Clear communication | Problem solving

Weaknesses: Limited BI tools | Need more statistics knowledge

ATS_Keywords: Pass
ATS_Verbs: Pass
ATS_Clarity: Fail

Improved_Bullet:
Original: Analyzed company data using Python
Improved: Engineered data pipelines in Python, processing 10M+ records daily, reducing query time by 45%

Learning_Roadmap:
Beginner: Master Tableau basics through LinkedIn Learning (2 weeks)
Intermediate: Build 5 interactive dashboards for real datasets
Advanced: Lead BI strategy for cross-functional product team
---

OUTPUT (Parsed Dict):
---
{
    "score": "8/10",
    "matched_skills": ["Python", "SQL", "Excel", "Power BI"],
    "missing_skills": ["Tableau", "Statistics"],
    "priority_skills": ["Statistics", "Tableau"],
    "strengths": [
        "Strong SQL foundations",
        "Clear communication",
        "Problem solving"
    ],
    "weaknesses": [
        "Limited BI tools",
        "Need more statistics knowledge"
    ],
    "ats_checks": {
        "keywords": "Pass",
        "verbs": "Pass",
        "clarity": "Fail"
    },
    "improved_bullet": {
        "original": "Analyzed company data using Python",
        "improved": "Engineered data pipelines in Python, processing 10M+ records daily, reducing query time by 45%"
    },
    "learning_roadmap": {
        "beginner": "Master Tableau basics through LinkedIn Learning (2 weeks)",
        "intermediate": "Build 5 interactive dashboards for real datasets",
        "advanced": "Lead BI strategy for cross-functional product team"
    }
}
---

PARSING RULES (in parse_unified_response):
===========================================

1. SCORE Line
   - Line: "Score: X/10"
   - Parsed: result["score"] = "X/10"

2. SKILLS Lists (Comma-Separated)
   - Lines: "Matched_Skills: skill1, skill2, skill3"
   - Parsed: Split by comma, strip whitespace, store as list

3. STRENGTHS/WEAKNESSES (Pipe-Separated)
   - Line: "Strengths: Point1 | Point2 | Point3"
   - Parsed: Split by "|", strip each item, store as list

4. ATS Checks (Pass/Fail Extraction)
   - Line: "ATS_Keywords: Pass"
   - Parsed: Check if "Pass" or "Fail" in line, store result

5. Improved Bullet (Multi-line Section)
   - Lines starting with "Original:" and "Improved:"
   - Parsed: Extract text after colon for each

6. Learning Roadmap (Multi-line Section)
   - Lines: "Beginner: ...", "Intermediate: ...", "Advanced: ..."
   - Parsed: Extract step descriptions for each level

---

ROBUST DESIGN - Handles Variations:
===================================

✓ Case-insensitive headers ("Score:" vs "SCORE:")
✓ Optional prefix removal ("Score: 8/10" → "8/10")
✓ Empty sections (gracefully ignored)
✓ Extra whitespace (stripped everywhere)
✓ Missing sections (defaults to empty list/dict)
✓ Duplicates in lists (allowed, not deduplicated)

---

EXAMPLE USAGE IN UI (app.py):
=============================

# Get parsed data
analysis = generate_unified_analysis(resume_text, "Data Analyst")

# Display score
score_num = int(analysis["score"].split("/")[0])  # "8/10" → 8
st.write(f"Score: {score_num}/10")

# Display matched skills
for skill in analysis["matched_skills"][:3]:
    st.write(f"✓ {skill}")

# Display ATS status
if analysis["ats_checks"]["keywords"] == "Pass":
    st.success("Keywords: Pass")
else:
    st.error("Keywords: Fail")

# Display improvement
original = analysis["improved_bullet"]["original"]
improved = analysis["improved_bullet"]["improved"]
st.write(f"Before: {original}")
st.write(f"After: {improved}")

# Display roadmap
st.write(f"1. {analysis['learning_roadmap']['beginner']}")
st.write(f"2. {analysis['learning_roadmap']['intermediate']}")
st.write(f"3. {analysis['learning_roadmap']['advanced']}")

---

WHY THIS DESIGN?
================

1. Plain Text (not JSON)
   - Faster LLM token generation
   - Easier for Ollama (smaller models)
   - Simpler parsing logic
   - More natural language output

2. Structured Headers
   - Predictable parsing
   - Clear section boundaries
   - Fail-safe fallbacks

3. Multiple Delimiters
   - Commas for lists (skills)
   - Pipes for emphasis (strengths)
   - Line-based for sections (roadmap)
   - Matches human writing patterns

4. Client-Side Parsing
   - Zero LLM overhead
   - Instant parsing
   - Full control over format
   - Easy to debug/modify

---

EXTENDING THE PARSER:
=====================

To add new sections:

1. Add to LLM prompt:
   "NEW_SECTION: [content]"

2. Add parsing logic in parse_unified_response():
   elif line_upper.startswith("NEW_SECTION:"):
       result["new_section"] = parse_new_section(content)

3. Add to result dict initialization:
   result["new_section"] = ""

4. Use in UI:
   analysis.get("new_section", "")

---

TESTING THE PARSER:
====================

# Save LLM response to file
with open("test_response.txt") as f:
    response = f.read()

# Parse it
from utils.unified_analysis import parse_unified_response
result = parse_unified_response(response)

# Verify
assert result["score"] == "8/10"
assert "Python" in result["matched_skills"]
assert result["ats_checks"]["keywords"] in ["Pass", "Fail"]
print("✓ Parser working correctly")
"""
