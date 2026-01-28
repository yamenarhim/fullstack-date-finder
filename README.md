# 📅 Date Calculator App 
A full-stack application designed to perform high-performance date calculations.
It features a **FastAPI** backend with in-memory caching and SQLite logging, paired with a modern **Vue 3** frontend.

### 🌟 Features
*   **Saturday Counter:** Calculates the number of Saturdays falling on the 15th of the month between two dates.
*   **Date Pattern Finder:** Finds specific weekdays and days of the month within a year range.
*   **Performance:** Uses `fastapi-cache` to store calculation results (In-Memory).
*   **Logging:** Asynchronous SQLite logging for all API requests.
*   **Security:** Rate limiting and Input Validation enabled.

---

## ⚡ Quick Start (The Easy Way)

We have provided scripts to automate the installation and running of the project.

### Prerequisites
*   **Python 3.10+**
*   **Node.js 18+**
*   **pnpm** (Install via `npm install -g pnpm`)

### 1. Run the Setup Script
This installs the virtual environment and all dependencies for both Backend and Frontend.

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

**Option A: Windows (One-Click)**
Double-click `start.bat` or run:
```cmd
.\start.bat
```
*This will automatically open two terminal windows: one for the Backend and one for the Frontend.*

**Option B: Mac / Linux (Manual)**
You need two terminal windows running simultaneously.

**Terminal 1: The Backend**
```bash
cd backend
source venv/bin/activate
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
├── setup.bat / setup.sh       # Installation scripts
├── start.bat                  # Windows launch script
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
