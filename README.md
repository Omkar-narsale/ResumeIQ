# AI Resume & Interview Coach - Setup Guide

## Overview
This is a production-ready Streamlit application that helps users improve their resumes and interview skills using AI-powered feedback powered by **Google Gemini (Free)**.

## Features
- 📄 **Resume Analysis**: Upload a PDF resume and get AI-powered feedback including score, strengths, weaknesses, and improvement suggestions
- 🎤 **Mock Interview**: Practice with AI-generated interview questions tailored to your target role and get detailed feedback on your answers

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Google API key (free at https://aistudio.google.com/apikey)

### 2. Installation

```bash
# Clone or navigate to project directory
cd ai-coach

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get Your Free Google API Key

1. Go to: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy your API key (looks like: `AIza...`)
4. Create `.env` file in project root:
   ```
   GOOGLE_API_KEY=YOUR_KEY_HERE
   ```
5. Done! No payment required, completely free.

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Project Structure

```
ai-coach/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
└── utils/
    ├── __init__.py
    ├── llm_handler.py    # Google Gemini API integration
    ├── resume_parser.py  # PDF parsing utilities
    └── interview.py      # Interview logic
```

## Usage Guide

### Resume Review Tab
1. Click "Upload your resume (PDF only)"
2. Select your PDF resume file
3. Click "🔍 Evaluate Resume"
4. View comprehensive feedback including:
   - Score (out of 10)
   - Key strengths
   - Areas for improvement
   - Actionable suggestions

### Mock Interview Tab
1. Enter your target job role (e.g., "Software Engineer")
2. Click "❓ Generate Question"
3. Answer the question in the text area
4. Click "✅ Submit Answer"
5. Receive feedback including:
   - Score (out of 10)
   - Specific feedback on your answer
   - Example of a better response
6. Click "➡️ Ask Another Question" to continue

## Features

### Resume Analysis
- Extracts text from PDF resumes
- Uses Google Gemini AI for intelligent analysis
- Provides structured feedback with:
  - Quantitative score
  - Strengths identification
  - Weakness analysis
  - Improvement recommendations

### Mock Interview
- Generates role-specific interview questions
- Evaluates answers with constructive feedback
- Provides improved answer examples
- Tracks question count during session
- Maintains conversation context

### UI/UX
- Clean, intuitive tabbed interface
- Real-time feedback with loading indicators
- Color-coded sections for better readability
- Session state management for seamless experience
- Responsive design for different screen sizes

## Security
- API keys are stored in environment variables, not hardcoded
- Uses `.env` file which is git-ignored
- No sensitive data is logged or stored

## Technical Details

### Models
- Uses `gemini-1.5-flash` (Fast, free, capable model)
- Max tokens per request: 1024
- Completely FREE with generous rate limits

### PDF Processing
- Extracts text from all pages
- Handles multi-page documents
- Error handling for corrupted files

### Prompt Engineering
- Structured prompts for consistent output format
- System prompts guide Gemini's behavior
- Professional formatting of responses

## Error Handling
- Graceful API error handling
- User-friendly error messages
- Validation for file types and inputs
- Environment variable validation

## Dependencies
- **streamlit**: Web UI framework
- **google-generativeai**: Google Gemini API client
- **PyPDF2**: PDF parsing library
- **python-dotenv**: Environment variable management

## Troubleshooting

### API Key Error
- Ensure `GOOGLE_API_KEY` is set in `.env`
- Get free key at: https://aistudio.google.com/apikey
- Make sure you copied the full key

### PDF Upload Issues
- Ensure file is a valid PDF
- File should not be password-protected
- Check that PDF contains extractable text (not image-based scans)

### Slow Responses
- Normal for first request
- Check your internet connection
- Gemini-1.5-flash is very fast once initialized

## Pricing
- **100% FREE** - Google Gemini has generous free tier
- No credit card required
- Unlimited requests (with fair use limits)

## Performance Notes
- First request may be slightly slower as Streamlit initializes
- Subsequent requests are very fast
- Resume parsing is instant for typical files
- Interview feedback generation takes 2-5 seconds

## Future Enhancements
- Support for other file formats (DOCX, TXT)
- Interview history tracking
- Custom interview templates
- Video answer recording
- Resume formatting suggestions
- Industry-specific recommendations

## License
This project is provided as-is for educational purposes.

## Support
For issues or questions:
1. Check the troubleshooting section
2. Verify your Google API key at https://aistudio.google.com/apikey
3. Check your internet connection
4. Review error messages carefully
