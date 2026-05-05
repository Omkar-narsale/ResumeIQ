# 🚀 ResumeIQ - AI-Powered Resume & Career Coach

> Production-ready React + FastAPI application for resume analysis, job matching, and career guidance powered by **local Ollama LLM** (100% free, no API keys needed!)

![React](https://img.shields.io/badge/React-19+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![Python](https://img.shields.io/badge/Python-3.8+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## ✨ Features Overview

ResumeIQ includes **5 core features** for resume analysis, job matching, and career development:

| Feature | Description |
|---------|-------------|
| **📄 Resume Upload & Analysis** | Upload PDF resume, get AI-powered feedback with score (0-10), strengths, weaknesses, and suggestions |
| **🎯 Job Matching** | Compare resume to job description, get match score (%), see matched/missing skills and improvement suggestions |
| **✍️ Resume Rewriter** | Professionally rewrite resume for target role with stronger action verbs, metrics, and ATS optimization |
| **📈 Learning Paths** | Get personalized 6-month career development roadmap for your target role with structured learning goals |
| **📊 Dashboard** | Track all analyses, view metrics, and see your resume analysis history |

---

## 🎯 Quick Start

### Prerequisites
- Node.js 16+ (for React frontend)
- Python 3.8+ (for FastAPI backend)
- Ollama installed and running locally ([https://ollama.ai](https://ollama.ai))
- ~2GB free disk space

### Installation (3 minutes)

#### Option 1: Automated Start (Windows)
```bash
# Clone repository
git clone https://github.com/Omkar-narsale/ResumeIQ.git
cd ResumeIQ/resumeiq

# Run start script
start.bat
```

#### Option 2: Manual Setup

**Backend Setup:**
```bash
cd resumeiq/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Run FastAPI server
python main.py
```

**Frontend Setup (in new terminal):**
```bash
cd resumeiq/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Setup Ollama

```bash
# 1. Install Ollama from https://ollama.ai

# 2. Start Ollama service
ollama serve

# 3. Pull a model (in another terminal)
ollama pull mistral
# or
ollama pull neural-chat

# 4. Verify it's running
curl http://localhost:11434/api/tags
```

### Access the App

- **Frontend**: `http://localhost:5173` (React dev server)
- **Backend API**: `http://localhost:8000` (FastAPI)
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)

---

## 📖 Usage Guide

### 🔐 Authentication
1. **Sign Up**: Create account with email & password
2. **Login**: Access your saved analyses and dashboard
3. **Profile**: View account info in navbar

### 📄 Resume Upload & Analysis
1. Go to "📄 Analyzer" page
2. Upload your PDF resume
3. (Optional) Enter target job role for role-aware analysis
4. Click "Analyze"
5. View results:
   - **Score** (0-10 scale)
   - **Strengths** (skills & experiences detected)
   - **Weaknesses** (areas to improve)
   - **Suggestions** (actionable recommendations)

### 🎯 Job Matching
1. Go to "🎯 Job Matcher" page
2. Upload resume
3. Paste job description
4. Click "Analyze Match"
5. View:
   - **Match Score** (percentage)
   - **Matched Skills** ✅ (skills you have)
   - **Missing Skills** ❌ (skills needed)
   - **Improvement Tips** (how to strengthen application)

### ✍️ Resume Rewriter
1. Go to "✍️ Rewriter" page
2. Upload your resume
3. Enter target role (optional)
4. Click "Rewrite Resume"
5. Get improved version with:
   - Stronger action verbs
   - Quantified achievements
   - Better ATS optimization
   - Professional formatting

### 📈 Learning Paths
1. Go to "📈 Learning" page
2. Enter your target role
3. Click "Generate Learning Path"
4. Get 6-month roadmap:
   - **Months 1-2**: Foundation skills
   - **Months 3-4**: Intermediate mastery
   - **Months 5-6**: Advanced level
5. Includes resources and milestones for each phase

### 📊 Dashboard
1. Go to "📊 Dashboard" page after logging in
2. View:
   - **Analysis History**: List of all resumes analyzed
   - **Scores**: Latest and average analysis scores
   - **Trends**: How your resumes are improving
   - **Job Matches**: Recent job matching results

---

## 📊 Supported Roles (10+)

Optimized analysis for:
- 📊 Data Analyst
- 💻 Software Engineer
- 🤖 ML Engineer
- 🎨 Frontend Developer
- ⚙️ Backend Developer
- 🐳 DevOps Engineer
- 📦 Product Manager
- 🔬 Data Scientist
- 📢 Marketing Manager
- 💼 Sales Engineer

---

## 🏗️ Project Structure

```
ResumeIQ/
├── resumeiq/
│   ├── frontend/                    # React.js application
│   │   ├── src/
│   │   │   ├── components/          # Reusable React components
│   │   │   ├── pages/               # Page components
│   │   │   │   ├── Analyzer.jsx     # Resume analysis
│   │   │   │   ├── Dashboard.jsx    # Analysis dashboard
│   │   │   │   ├── JobMatcher.jsx   # Job matching
│   │   │   │   ├── Learning.jsx     # Learning paths
│   │   │   │   ├── Rewriter.jsx     # Resume rewriter
│   │   │   │   └── Login.jsx        # Authentication
│   │   │   ├── context/             # Auth & Resume context
│   │   │   ├── hooks/               # Custom React hooks
│   │   │   ├── styles/              # Global CSS & Tailwind
│   │   │   └── App.jsx              # Main App component
│   │   ├── package.json             # Node dependencies
│   │   ├── vite.config.js           # Vite configuration
│   │   └── tailwind.config.js       # Tailwind CSS config
│   │
│   ├── backend/                     # FastAPI application
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── models.py                # Data models & schemas
│   │   ├── database.py              # SQLite setup & ORM
│   │   ├── inference.py             # Ollama LLM calls
│   │   ├── extract_text.py          # PDF text extraction
│   │   ├── requirements.txt         # Python dependencies
│   │   └── .env.example             # Environment template
│   │
│   └── start.bat                    # Windows startup script
│
├── README.md                        # This file
└── RESUME_ANALYZER_DOCS.md         # Technical documentation
```

---

## 🔧 Technical Stack

### Frontend
- **React 19** - UI framework with hooks & context API
- **Vite** - Lightning-fast build tool & dev server
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API calls

### Backend
- **FastAPI** (0.100+) - Modern async Python framework
- **Python** (3.8+) - Core language
- **Ollama** - Local LLM (mistral, neural-chat, etc.)
- **SQLAlchemy** - ORM for database
- **SQLite** - Database for persistence
- **Pydantic** - Data validation & schemas

### Libraries Used
| Category | Libraries |
|----------|-----------|
| Frontend | react-router-dom, axios, tailwindcss |
| Backend | fastapi, uvicorn, requests, PyPDF2, sqlalchemy |

---

## 🔒 Security Features

- ✅ **Password Security**: Industry-standard hashing (bcrypt)
- ✅ **Session Management**: User authentication & sessions
- ✅ **Data Isolation**: Users only see their own data
- ✅ **Input Validation**: PDF file validation
- ✅ **No API Keys**: All processing local (Ollama)
- ✅ **Environment Variables**: Sensitive config in .env

---

## 📊 Database Schema

### Users Table
```sql
- id (TEXT, PRIMARY KEY)
- email (TEXT, UNIQUE)
- password_hash (TEXT)
- created_at (DATETIME)
- last_login (DATETIME)
```

### Analysis History Table
```sql
- id (INTEGER, PRIMARY KEY)
- user_id (TEXT, FOREIGN KEY)
- timestamp (DATETIME)
- analysis_type (TEXT) - 'resume_analysis', 'job_match', 'rewrite'
- score (FLOAT)
- target_role (TEXT)
- filename (TEXT)
- content (TEXT, JSON)
```

---

## ⚙️ Environment Setup

Create `.env` file in `resumeiq/backend/`:
```env
# Ollama configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Optional settings
DEBUG=false
DATABASE_URL=sqlite:///./resumeiq.db
```

---

## 🐛 Troubleshooting

### Ollama Issues
| Problem | Solution |
|---------|----------|
| "Ollama server not running" | Run `ollama serve` in terminal |
| "Model not found" | Run `ollama pull mistral` or `ollama pull neural-chat` |
| Connection timeout | Verify `http://localhost:11434` is accessible |
| Slow responses | Close other apps, check available RAM (8GB+ recommended) |

### PDF Upload Issues
| Problem | Solution |
|---------|----------|
| "Cannot read PDF" | Ensure PDF is text-based, not image scan |
| "Invalid file" | Only PDF files are supported |
| "File too large" | Limit resume to 5 pages |

### Authentication Issues
| Problem | Solution |
|---------|----------|
| "Email already exists" | Use different email or login |
| "Login failed" | Check email and password |
| "Data not saving" | Ensure you're logged in |

### API Issues
| Problem | Solution |
|---------|----------|
| "Backend not responding" | Verify FastAPI is running on port 8000 |
| "CORS errors" | Restart both frontend and backend |
| "Database locked" | Restart the application |

---

## 📝 Usage Tips

### For Best Resume Analysis
1. **Use clear PDFs** - Single column format works best
2. **Include target role** - Enables more accurate, role-specific analysis
3. **Highlight experience** - More detailed experience = better suggestions
4. **Review suggestions** - Implement recommended improvements

### For Job Matching
1. **Use full job description** - Copy complete JD for accurate matching
2. **Include target role** - Helps system understand role level
3. **Review missing skills** - Prioritize gap-closing
4. **Save results** - Track multiple job applications

### For Resume Rewriting
1. Start with your best resume version
2. Specify target role for specific improvements
3. Compare before/after versions
4. Implement suggested action verbs

---

## 📈 Performance Notes

- **Resume Analysis**: 3-4 seconds (Ollama inference)
- **Job Matching**: 2-3 seconds (skill extraction + LLM)
- **Frontend Load**: <500ms (React bundle)
- **Database Queries**: <50ms (SQLite)
- **Model Loading**: ~2-3s first request, then instant
- **Concurrent Users**: Supported via FastAPI async

---

## 🚀 Future Enhancements (Planned)

- 🎤 Mock Interview Practice
- 💰 Salary Guide by Role & Experience
- 📥 Resume Export (PDF/DOCX formats)
- 🔍 Resume Scoring Trends
- 📧 Email Notifications
- 🎯 Interview Question Library
- 💼 Company Research Tool

---

## 💡 Contributing

Contributions welcome! Areas for improvement:
- Additional role templates and career paths
- Enhanced PDF parsing
- More interactive UI features
- Performance optimizations
- Multi-language support

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🤝 Support & Feedback

For issues, questions, or suggestions:
1. **GitHub Issues**: [Report a bug](https://github.com/Omkar-narsale/ResumeIQ/issues)
2. **Troubleshooting**: Check the section above
3. **Ollama Help**: Visit [https://ollama.ai](https://ollama.ai)

---

## ✨ Credits

Built with ❤️ using:
- React for the modern UI framework
- FastAPI for the robust backend
- Ollama for local LLM capabilities
- The open-source community

---

## 🎯 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 5 core features |
| **Supported Roles** | 10+ |
| **Analysis Time** | 3-4 seconds |
| **Security** | Bcrypt + Session isolation |
| **Cost** | 100% FREE |
| **Model** | Local Ollama (no API costs) |
| **Database** | SQLite (local) |

---

**Start improving your resume and career today! 🚀**

```bash
cd resumeiq
start.bat
```
