@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo 🚀 DATE CALCULATOR APP - SMART SETUP
echo ==========================================

:: Store current directory
set "CURRENT_DIR=%cd%"

:: --------------------------
:: 1. BACKEND CHECKS
:: --------------------------
echo.
echo [1/4] Checking Backend Virtual Environment...

if exist "backend\venv" (
    echo    - Virtual environment found. Skipping creation.
) else (
    echo    - Not found. Creating new virtual environment...
    pushd "backend"
    python -m venv venv
    popd
)

echo [2/4] Updating Backend Dependencies...
pushd "backend"
call venv\Scripts\activate
echo    - Checking/installing dependencies...
pip install -r requirements\dev.txt
if !errorlevel! equ 0 (
    echo    - Dependencies installed/updated successfully.
) else (
    echo    - ERROR: Failed to install backend dependencies.
)
popd

:: --------------------------
:: 2. FRONTEND CHECKS
:: --------------------------
echo.
echo [3/4] Checking Frontend...

:: Check if frontend directory exists
if not exist "frontend\" (
    echo    - ERROR: Frontend directory not found!
    goto :launch
)

pushd "frontend"

if exist "node_modules" (
    echo    - Node modules found. Skipping install.
) else (
    echo    - Installing Frontend Dependencies...
    
    :: Check if pnpm is available
    where pnpm >nul 2>&1
    if !errorlevel! equ 0 (
        echo    - Using pnpm...
        pnpm install
    ) else (
        echo    - pnpm not found. Using npm...
        npm install
    )
    
    if !errorlevel! neq 0 (
        echo    - WARNING: Package manager install failed.
    )
)
popd

:launch
:: --------------------------
:: 3. LAUNCH OPTION
:: --------------------------
echo.
echo ==========================================
echo ✅ SETUP COMPLETE!
echo ==========================================
echo.
echo Do you want to launch the app now?
echo.
choice /c YN /m "Launch app in two terminals (Y/N)?"
if errorlevel 2 goto :exit

echo.
echo Launching Backend Server...
start "Date Calculator Backend" cmd /k "cd /d "%CURRENT_DIR%\backend" && call venv\Scripts\activate && set PYTHONPATH=src && echo Backend Server Running... && echo. && uvicorn app.main:app --reload"

timeout /t 3 /nobreak >nul

echo Launching Frontend Server...
start "Date Calculator Frontend" cmd /k "cd /d "%CURRENT_DIR%\frontend" && echo Frontend Server Running... && echo. && pnpm dev"

echo.
echo ==========================================
echo 🚀 APP LAUNCHED!
echo ==========================================
echo Both servers are starting in separate windows.
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to close this setup window...
pause >nul
exit /b

:exit
echo.
echo You can launch the app manually:
echo 1. Terminal 1: cd "backend" ^& venv\Scripts\activate ^& set PYTHONPATH=src ^& uvicorn app.main:app --reload
echo 2. Terminal 2: cd "frontend" ^& pnpm dev
echo.
pause