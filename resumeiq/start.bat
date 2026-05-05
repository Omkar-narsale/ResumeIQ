@echo off
echo ========================================
echo   ResumeIQ - Starting Application
echo ========================================
echo.

echo [1/3] Starting Backend (FastAPI)...
echo.
cd /d "%~dp0backend"
start cmd /k "python main.py"
timeout /t 3

echo [2/3] Starting Frontend (Vite)...
echo.
cd /d "%~dp0frontend"
start cmd /k "npm run dev"

echo.
echo ========================================
echo ✅ Application Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: First startup will download TinyLlama model (~2GB)
echo This may take 2-5 minutes on first run.
echo.
pause
