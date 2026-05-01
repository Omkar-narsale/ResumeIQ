"""Quick test to verify parsing works"""

from utils.features import parse_resume_analysis

# Test 1: Proper response
good_response = """Score: 8/10

Strengths:
* Strong Python skills
* Good project experience
* Clear communication

Weaknesses:
* Limited SQL knowledge
* Need more system design
* Weak presentation skills

Suggestions:
* Learn SQL fundamentals
* Study system design patterns
* Practice public speaking"""

result1 = parse_resume_analysis(good_response)
print("Test 1 (Good Response):")
print(f"  Score: {result1['score']}")
print(f"  Strengths: {result1['strengths'][:50]}...")
print(f"  Status: {'✓ PASS' if result1['score'] != '0/10' else '✗ FAIL'}\n")

# Test 2: Empty response
empty_response = ""
result2 = parse_resume_analysis(empty_response)
print("Test 2 (Empty Response):")
print(f"  Score: {result2['score']}")
print(f"  Strengths: {result2['strengths'][:50]}...")
print(f"  Status: {'✓ PASS - Has defaults' if result2['strengths'] else '✗ FAIL'}\n")

# Test 3: Malformed response
bad_response = "</div>\n</div>"
result3 = parse_resume_analysis(bad_response)
print("Test 3 (Malformed HTML):")
print(f"  Score: {result3['score']}")
print(f"  Strengths: {result3['strengths'][:50]}...")
print(f"  Status: {'✓ PASS - Has defaults' if result3['strengths'] != '• Information not available' else '✗ FAIL'}\n")

print("All tests completed. Check results above.")
