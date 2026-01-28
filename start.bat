@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo 🚀 DATE CALCULATOR APP - QUICK START
echo ==========================================

:: Use the current directory (where the batch file is run from)
echo Current directory: %cd%
echo.

:: Quick check for required directories
if not exist "backend\" (
    echo ❌ ERROR: Backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

if not exist "frontend\" (
    echo ❌ ERROR: Frontend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ Directories found. Launching servers...
echo.

:: Launch Backend - Using a different approach to avoid path issues
echo Starting Backend (port 8000)...
cmd /c start "📅 Date Calculator - Backend" cmd /k "pushd "%~dp0backend" && call venv\Scripts\activate && set PYTHONPATH=src && echo === BACKEND === && echo URL: http://localhost:8000 && echo. && uvicorn app.main:app --reload"

echo Waiting 2 seconds for backend...
timeout /t 2 /nobreak >nul

:: Launch Frontend
echo Starting Frontend (port 5173)...
cmd /c start "📅 Date Calculator - Frontend" cmd /k "pushd "%~dp0frontend" && echo === FRONTEND === && echo URL: http://localhost:5173 && echo. && pnpm dev"

echo.
echo ==========================================
echo ✅ SERVERS LAUNCHED!
echo ==========================================
echo Check the new terminal windows for outputs.
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
pause