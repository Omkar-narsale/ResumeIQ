# Career Toolkit - Quick Start & Testing Guide

## Prerequisites
- Node.js & npm (for frontend)
- Python 3.8+ (for backend)
- FastAPI and dependencies installed
- React and Tailwind configured

## Getting Started

### 1. Start Backend Server
```bash
cd resumeiq/backend
python main.py
# Server will run on http://localhost:8000
```

### 2. Start Frontend Dev Server
```bash
cd resumeiq/frontend
npm run dev
# App will run on http://localhost:5173
```

### 3. Access ResumeIQ
Open browser to `http://localhost:5173`

---

## API Endpoints Reference

### LinkedIn Optimizer
**Endpoint:** `POST /api/linkedin-optimizer`

**Request:**
```json
{
  "headline": "Senior Software Engineer",
  "about_section": "Passionate about building scalable systems...",
  "skills": ["Python", "JavaScript", "AWS"],
  "target_role": "Engineering Manager"
}
```

**Response:**
```json
{
  "optimized_headline": "Engineering Manager | Tech Leader | 10+ Years Building Scalable Systems",
  "optimized_about": "Results-driven technology leader...",
  "suggested_keywords": ["Strategic", "Leadership", "Innovation"],
  "missing_skills": ["Team Management", "Budget Planning"],
  "profile_strength_score": 78.5,
  "improvements": ["Added role-specific keywords...", "Optimized headline for ATS..."]
}
```

### STAR Responses
**Endpoint:** `POST /api/star-response`

**Request:**
```json
{
  "question": "Tell me about a challenge you overcame",
  "difficulty": "medium",
  "domain": "Software Engineering"
}
```

**Response:**
```json
{
  "situation": "In my previous role as a backend engineer...",
  "task": "I was tasked with optimizing our database queries...",
  "action": "I implemented connection pooling, added caching with Redis...",
  "result": "We achieved 40% query performance improvement...",
  "full_answer": "[Complete STAR response combined]",
  "difficulty_tag": "Medium"
}
```

### Email Templates
**Endpoint:** `POST /api/email-template`

**Request:**
```json
{
  "template_type": "job_outreach",
  "user_name": "John Doe",
  "company_name": "TechCorp",
  "role": "Senior Engineer",
  "additional_context": "Recently read about their new AI initiative"
}
```

**Response:**
```json
{
  "subject_line": "Excited to Join TechCorp's AI Innovation Team",
  "email_body": "Hi [Hiring Manager],\n\nI am writing to express...",
  "tips": [
    "Personalize with specific company details",
    "Keep subject line clear and action-oriented",
    "Use professional but warm tone",
    "Include clear call-to-action"
  ]
}
```

---

## Frontend Components

### CareerToolkit.jsx Structure
```
CareerToolkit (Main Container)
├── Tab Navigation (4 tabs)
├── LinkedInOptimizer
│   ├── Form (headline, about, skills, target role)
│   └── Results (optimized content, keywords, score)
├── StarResponses
│   ├── Form (question, difficulty, domain)
│   └── Results (STAR breakdown, full answer)
├── EmailTemplates
│   ├── Form (type, user info, company, role)
│   └── Results (subject, body, tips)
└── PortfolioShowcase
    ├── Filter (by domain)
    ├── Add Project Form
    └── Portfolio Grid
```

---

## Testing Scenarios

### Test 1: LinkedIn Profile Optimization
**Steps:**
1. Navigate to Career Toolkit → LinkedIn Optimizer
2. Fill form:
   - Headline: "Software Engineer at Tech Company"
   - About: "I build web applications using React and Node.js"
   - Skills: "JavaScript, React, Node.js, MongoDB, Git"
   - Target Role: "Senior Frontend Engineer"
3. Click "Optimize Profile"
4. Verify results show optimized content
5. Test copy buttons for each section

**Expected:**
- Optimized headline includes role-specific keywords
- About section sounds more professional
- Suggested keywords match the target role
- Profile strength score is between 50-100

### Test 2: STAR Response Generation
**Steps:**
1. Navigate to Career Toolkit → STAR Responses
2. Select a common question or enter custom
3. Set difficulty to "Medium"
4. Enter domain: "Software Engineering"
5. Click "Generate Response"
6. Review STAR breakdown (Situation, Task, Action, Result)
7. Copy individual sections

**Expected:**
- Each STAR section has 1-3 sentences
- Answer is realistic and interview-ready
- Full answer combines all sections coherently
- Copy buttons work for each section

### Test 3: Email Template Generation
**Steps:**
1. Navigate to Career Toolkit → Email Templates
2. Select template type: "Job Application Outreach"
3. Fill form:
   - Your Name: "Jane Smith"
   - Company: "Acme Corp"
   - Role: "Product Manager"
   - Context: "Passionate about your mobile app redesign"
4. Click "Generate Email"
5. Review subject line and body
6. Copy and test in email client

**Expected:**
- Subject line is concise and compelling
- Body is 150-250 words
- Email is personalized
- Professional tone maintained
- Tips section provides actionable guidance

### Test 4: Portfolio Showcase
**Steps:**
1. Navigate to Career Toolkit → Portfolio Showcase
2. Click "+ Add Project"
3. Fill form:
   - Title: "AI Resume Analyzer"
   - Description: "Built an AI-powered resume analyzer..."
   - Technologies: "React, Python, TensorFlow, FastAPI"
   - GitHub: "https://github.com/example/resume-analyzer"
   - Demo: "https://resumeiq.app"
   - Domain: "AI/ML"
4. Click "Add Project"
5. Filter by different domains
6. Verify card displays all information

**Expected:**
- Project appears in grid
- Technologies display as tags
- Links are clickable
- Filtering works correctly
- Cards have hover animations

---

## Troubleshooting

### Issue: "Failed to optimize" Error
**Solution:**
- Check backend is running on http://localhost:8000
- Verify token is valid
- Check browser console for full error message

### Issue: Loading State Never Completes
**Solution:**
- Check network tab in DevTools
- Verify API endpoint URL is correct
- Check backend logs for errors
- Ensure CORS is configured correctly

### Issue: Copy to Clipboard Not Working
**Solution:**
- Check browser permissions for clipboard access
- Verify HTTPS or localhost (required for Clipboard API)
- Use alternative copy method if needed

### Issue: Form Validation Errors
**Solution:**
- Ensure all required fields are filled
- Check for proper formatting (URLs, email, etc.)
- Verify no special characters cause issues

---

## Performance Tips

1. **Batch Operations** - If generating multiple items, space requests 1-2 seconds apart
2. **Caching** - Results are cached in browser, refresh to see new results
3. **Networking** - Use efficient networks for faster API response times
4. **Memory** - Portfolio showcase handles 100+ projects smoothly

---

## Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

---

## Keyboard Shortcuts

- `Tab` - Navigate between form fields
- `Enter` - Submit form
- `Shift+Tab` - Navigate backwards
- `Escape` - Close modals/forms

---

## Demo Accounts

For testing, use these credentials (if already registered):
- Email: `test@example.com`
- Password: `Test123!`

---

## Support & Documentation

- Component Docs: See CAREER_TOOLKIT_IMPLEMENTATION.md
- API Reference: See this file above
- Code: `resumeiq/frontend/src/pages/CareerToolkit.jsx`
- Backend: `resumeiq/backend/main.py`, `inference.py`, `models.py`

---

## Next Steps After Setup

1. ✅ Start both backend and frontend servers
2. ✅ Login to ResumeIQ
3. ✅ Navigate to Career Toolkit from sidebar
4. ✅ Test each of the 4 features
5. ✅ Copy content and customize as needed
6. ✅ Share feedback or report issues

---

Happy career building! 🚀
