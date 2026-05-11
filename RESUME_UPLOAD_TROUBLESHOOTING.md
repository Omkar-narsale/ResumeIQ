# Resume Upload - Troubleshooting Guide

## ✅ What We Verified

All backend systems are working correctly:
- ✅ Database setup OK
- ✅ PDF extraction (pdfplumber) working
- ✅ All dependencies installed
- ✅ API endpoints configured
- ✅ Authentication ready

---

## ❌ Common Issues & Solutions

### Issue 1: "Upload Failed" Error
**What's happening?**
The frontend shows an upload error but backend isn't running.

**Solution:**
```bash
# Terminal 1 - Start Backend
cd "C:\Users\Omkar\Desktop\AI PROJECT\resumeiq\backend"
python main.py

# Wait for: Uvicorn running on http://127.0.0.1:8000
```

**Verify:** Check that the message says `Application startup complete` without errors.

---

### Issue 2: CORS Error in Browser Console
**What you'll see:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/resumes/upload' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Solution:**
This means the backend is running but CORS isn't configured. The code should have CORS enabled, but verify in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

If this is missing, I'll add it.

---

### Issue 3: "Not Authenticated" or Token Error
**What you'll see:**
```
Error: Invalid token or Unauthorized
```

**Solution:**
1. Make sure you're logged in (you should see username on dashboard)
2. Clear browser cache and login again
3. Check browser DevTools Console for token errors

---

### Issue 4: "PDF appears to be empty"
**What's happening?**
The PDF file was uploaded but contains no extractable text (might be a scanned image PDF).

**Solution:**
- Try a text-based PDF (not scanned/image-based)
- Or use OCR-processed PDF

---

### Issue 5: Upload Hangs/Timeout
**What you'll see:**
Loading spinner keeps spinning, then fails after ~30 seconds.

**Solution:**
1. Check backend console for errors: `python main.py` should show logs
2. Try a smaller PDF file first
3. Restart both backend and frontend

---

## 🔍 Step-by-Step Debug Process

### Step 1: Check Backend is Running
```bash
# Should return {"status": "ok"}
curl http://localhost:8000/health
```

**If you get connection refused:**
- Backend isn't running, start it with: `python main.py`

**If you get a valid response:**
- Backend is running, continue to Step 2

---

### Step 2: Check API Docs
Open browser to: **http://localhost:8000/docs**

- Look for `POST /api/resumes/upload`
- Click "Try it out"
- Select a small PDF file
- Click "Execute"

**What to look for:**
- **Response 200**: Upload succeeded - check the response body
- **Response 4xx**: Client error - check the error message
- **Response 5xx**: Server error - check backend console

---

### Step 3: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Try uploading a resume
4. Look for error messages

**Common errors you might see:**
```javascript
// 1. Connection refused
TypeError: Failed to fetch

// 2. CORS error (see Issue 2 above)
Access to XMLHttpRequest ... has been blocked by CORS policy

// 3. Auth error
{
  "detail": "Invalid token"
}

// 4. Bad request
{
  "detail": "Only PDF files are allowed"
}

// 5. Server error
{
  "detail": "Failed to extract text: ..."
}
```

---

### Step 4: Check Backend Logs
Run the backend and watch for output:
```bash
cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
python main.py
# Then try uploading from frontend
# You should see request logs
```

**Look for:**
```
POST /api/resumes/upload HTTP/1.1" 200
# OR
POST /api/resumes/upload HTTP/1.1" 400
POST /api/resumes/upload HTTP/1.1" 500
```

---

## 🧪 Manual Upload Test

### Test 1: Using Swagger UI
1. Go to http://localhost:8000/docs
2. Click "Authorize" (top right)
3. Enter token: (copy from browser localStorage if needed)
4. Scroll to `POST /api/resumes/upload`
5. Click "Try it out"
6. Select a PDF file
7. Click "Execute"

### Test 2: Using cURL (if you have it)
```bash
# Get your token first
# Then replace TOKEN and PATH_TO_PDF

curl -X POST "http://localhost:8000/api/resumes/upload" \
  -H "Authorization: Bearer TOKEN_HERE" \
  -F "file=@C:\path\to\resume.pdf"
```

---

## 🔧 Fix Common Setup Issues

### Issue: pdfplumber not installed
```bash
pip install pdfplumber
```

### Issue: Dependencies missing
```bash
cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
pip install -r requirements.txt
```

### Issue: Database corrupted
```bash
# Delete the database and restart
cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
del resumeiq.db
python main.py  # Will create fresh database
```

### Issue: Port 8000 already in use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual process ID)
taskkill /PID YOUR_PID /F
```

---

## 📋 Pre-Upload Checklist

Before uploading, verify:
- [ ] Backend running: `python main.py` in backend folder
- [ ] Frontend running: `npm run dev` in frontend folder
- [ ] Logged in to ResumeIQ (see username on screen)
- [ ] PDF file is text-based (not scanned image)
- [ ] PDF file is less than 50MB
- [ ] File has `.pdf` extension
- [ ] Browser allows file uploads (no security restrictions)

---

## 📞 Still Having Issues?

If none of these solutions work, please share:
1. **The exact error message** you see (frontend or console)
2. **Backend console output** when you try to upload
3. **Browser console errors** (F12 → Console tab)
4. **Steps to reproduce** the issue

---

## 🎯 Expected Behavior

### Successful Upload Flow:
1. Click upload area or drag-drop PDF
2. See "Uploading..." spinner
3. Resume appears in list on page
4. Current resume text shows on dashboard
5. Auto-analysis runs automatically

### Response from Backend:
```json
{
  "id": 1,
  "filename": "resume.pdf",
  "extracted_text": "[First 200 characters of resume...]"
}
```

---

## ✨ Quick Fix Checklist

Try these in order:

1. **Restart everything:**
   - Close both frontend and backend
   - Clear browser cache (Ctrl+Shift+Delete)
   - Restart both servers

2. **Delete database and reset:**
   ```bash
   cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
   del resumeiq.db
   python main.py
   ```

3. **Reinstall dependencies:**
   ```bash
   cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
   pip install -r requirements.txt --force-reinstall
   ```

4. **Test with different PDF:**
   - Try a simple, small PDF file first
   - Make sure it's not a scanned image

5. **Check network:**
   - Open DevTools (F12)
   - Network tab
   - Try uploading
   - Look for failed requests

---

If you're still stuck, run this command and share the output:
```bash
cd c:\Users\Omkar\Desktop\AI\ PROJECT\resumeiq\backend
python diagnostic.py
```
