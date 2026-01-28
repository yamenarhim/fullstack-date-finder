Here is the complete package. I have created **setup scripts** for you to add to the root folder, and a **comprehensive README** that references them.

### 1️⃣ The Scripts (Create these in the root folder)

These scripts handle the boring work: creating the virtual environment, installing Python dependencies, and installing Node modules.

**Option A: For Windows (`setup.bat`)**
Create a file named `setup.bat` in the root:
```batch
@echo off
echo ==========================================
echo 🚀 DATE CALCULATOR APP - ONE-CLICK SETUP
echo ==========================================

echo.
echo [1/4] Setting up Backend Virtual Environment...
cd backend
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/4] Installing Backend Dependencies...
pip install -r requirements\dev.txt

echo.
echo [3/4] Installing Frontend Dependencies (pnpm)...
cd ..\frontend
call pnpm install

echo.
echo ==========================================
echo ✅ SETUP COMPLETE!
echo ==========================================
echo.
echo To run the app:
echo 1. Open Terminal 1 (Backend): cd backend, activate venv, run uvicorn
echo 2. Open Terminal 2 (Frontend): cd frontend, run pnpm dev
echo.
echo (See README.md for exact commands)
pause
```

**Option B: For Mac / Linux (`setup.sh`)**
Create a file named `setup.sh` in the root:
```bash
#!/bin/bash
echo "=========================================="
echo "🚀 DATE CALCULATOR APP - ONE-CLICK SETUP"
echo "=========================================="

echo ""
echo "[1/4] Setting up Backend Virtual Environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo ""
echo "[2/4] Installing Backend Dependencies..."
pip install -r requirements/dev.txt

echo ""
echo "[3/4] Installing Frontend Dependencies (pnpm)..."
cd ../frontend
pnpm install

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
```
*(Run `chmod +x setup.sh` to make it executable)*

---

### 2️⃣ The README.md

Copy this exactly into your `README.md`.

```markdown
# 📅 Date Calculator App (Monorepo)

A professional full-stack application designed to perform high-performance date calculations.
It features a **FastAPI** backend with in-memory caching and SQLite logging, paired with a modern **Vue 3** frontend.

### 🌟 Features
*   **Saturday Counter:** Calculates the number of Saturdays falling on the 15th of the month between two dates.
*   **Weekday Calculator:** Instantly determines the weekday for any given date.
*   **Performance:** Uses `fastapi-cache` to store calculation results.
*   **Logging:** Asynchronous SQLite logging for all API requests.
*   **Security:** Rate limiting and Input Validation enabled.

---

## ⚡ Quick Start (The Easy Way)

We have provided a script to automate the installation of all Python and Node.js dependencies.

### Prerequisites
*   **Python 3.10+**
*   **Node.js 18+**
*   **pnpm** (Install via `npm install -g pnpm`)

### 1. Run the Setup Script
**Windows:**
Double-click `setup.bat` or run:
```cmd
.\setup.bat
```

**Mac / Linux:**
```bash
./setup.sh
```

### 2. Start the Servers
You need two terminal windows running simultaneously.

**Terminal 1: The Backend**
```bash
cd backend
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
# Run Server:
# Windows:
set PYTHONPATH=src && uvicorn app.main:app --reload
# Mac/Linux:
PYTHONPATH=src uvicorn app.main:app --reload
```

**Terminal 2: The Frontend**
```bash
cd frontend
pnpm dev
```

🚀 **Open your browser:** [http://localhost:3000](http://localhost:3000)

---

## 🛠️ Manual Installation (No Scripts)

If you prefer to install things manually or verify the steps, follow this guide.

### 1. Backend Setup
Navigate to the `backend` folder, create a virtual environment, and install dependencies.

```bash
cd backend
python -m venv venv

# Windows Activate:
.\venv\Scripts\activate
# Mac/Linux Activate:
source venv/bin/activate

# Install Deps
pip install -r requirements/dev.txt
```

To run the backend:
```bash
# Windows
set PYTHONPATH=src && uvicorn app.main:app --reload

# Mac/Linux
PYTHONPATH=src uvicorn app.main:app --reload
```
*Server runs at: http://127.0.0.1:8000*

### 2. Frontend Setup
Navigate to the `frontend` folder and use pnpm.

```bash
cd frontend
pnpm install
```

To run the frontend:
```bash
pnpm dev
```
*App runs at: http://localhost:3000*

---

## 📂 Project Structure

This project is a **Monorepo**.

```text
date-calculator-app/
├── setup.bat / setup.sh       # One-click installation scripts
├── backend/                   # 🐍 Python / FastAPI
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/           # Endpoints
│   │   │   ├── core/          # Config & DB
│   │   │   ├── middleware/    # Logging Logic
│   │   │   └── services/      # Date Calculation Logic
│   ├── requirements/          # Dependency lists
│   └── tests/                 # Pytest suite
└── frontend/                  # ⚡ Vue 3 / Vite
    ├── src/                   # Vue Components
    └── vite.config.ts         # Proxy Configuration
```

## 🧪 Testing

The backend includes a comprehensive test suite.

**Unit & API Tests:**
```bash
cd backend
# Ensure venv is active
PYTHONPATH=src pytest tests/
```

**Load/Stress Tests:**
```bash
cd backend
# Ensure venv is active
locust -f locustfile.py
```

## 🔍 Logging
The application automatically logs every request to a local SQLite database.
To view logs:
1.  Use a tool like **DB Browser for SQLite**.
2.  Open the file `backend/logs.db`.
3.  Browse the `api_logs` table.
```