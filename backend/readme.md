Here is a professional, production-grade `README.md` for your project. You can copy-paste this directly into the root of your repository.

***

# 📅 Date Calculator API

A high-performance, production-ready REST API built with **FastAPI**. This application performs date calculations, such as determining weekdays and counting specific Saturdays between date ranges, optimized with caching and security features.

## 🚀 Features

*   **Weekday Calculation:** Determine the weekday number and name for any given date.
*   **Saturday Counter:** Efficiently calculates how many Saturdays fall on the 15th of the month between two dates.
*   **High Performance:** Implements **In-Memory Caching** to serve repeated requests instantly.
*   **Security:**
    *   **Rate Limiting:** Protects against abuse using `slowapi`.
    *   **Input Validation:** Robust data validation using **Pydantic V2**.
    *   **CORS:** Configured to allow secure communication with frontend applications (e.g., React).
*   **Documentation:** Automatic interactive API documentation via Swagger UI and ReDoc.

## 🛠️ Tech Stack

*   **Language:** Python 3.11+
*   **Framework:** FastAPI
*   **Server:** Uvicorn (ASGI)
*   **Validation:** Pydantic
*   **Caching:** FastAPI-Cache2 (In-Memory/Redis ready)
*   **Rate Limiting:** SlowAPI
*   **Testing:** Pytest & HttpX
*   **Load Testing:** Locust

## 📂 Project Structure

```text
date-calculator-api/
├── src/
│   ├── app/
│   │   ├── api/v1/         # Route handlers
│   │   ├── core/           # Config, Security, Rate Limiter
│   │   ├── schemas/        # Pydantic Models (Input/Output)
│   │   ├── services/       # Business Logic
│   │   └── main.py         # App Entrypoint
├── tests/                  # Pytest suite
├── requirements/           # Dependency management
├── locustfile.py           # Load testing configuration
└── README.md
```

## ⚡ Getting Started

### Prerequisites

*   Python 3.10 or higher installed.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/date-calculator-api.git
cd date-calculator-api
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

We split requirements into `base`, `dev`, and `prod`. For local development, install the `dev` set:

```bash
pip install -r requirements/dev.txt
```

### 4. Run the Application 🏃

To run the server in development mode (with hot-reload enabled):

```bash
# We set PYTHONPATH to src so Python can find the 'app' module
PYTHONPATH=src uvicorn app.main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## 📖 API Documentation

Once the server is running, you can access the interactive documentation:

*   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) - Test endpoints directly in your browser.
*   **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) - Alternative documentation view.

### Key Endpoints

**1. Get Weekday**
`GET /api/v1/dates/weekday?year=2025&month=1&day=15`

**2. Count Mid-Month Saturdays**
`GET /api/v1/dates/mid-saturdays?start_date=2020-01-01&end_date=2030-12-31`

---

## 🧪 Testing

### Running Unit & API Tests
This project uses **pytest** to ensure logic integrity.

```bash
PYTHONPATH=src pytest tests/
```

### Running Load Tests
This project includes a **Locust** file to simulate high traffic (up to 1M requests/day).

1.  Start the API in production mode (multiple workers):
    ```bash
    PYTHONPATH=src uvicorn app.main:app --workers 4
    ```
2.  In a new terminal, start Locust:
    ```bash
    locust -f locustfile.py
    ```
3.  Open [http://localhost:8089](http://localhost:8089) and enter `http://localhost:8000` as the host.

---

## 🛡️ Configuration

Configuration is managed via `src/app/core/config.py`. You can customize settings using Environment Variables.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PROJECT_NAME` | Date Calculator API | Name of the API |
| `BACKEND_CORS_ORIGINS` | `["http://localhost:3000"]` | List of allowed frontend origins |

---
