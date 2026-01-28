import time
from fastapi import Request
from starlette.background import BackgroundTask
from starlette.responses import Response
from app.core.database import AsyncSessionLocal, APIRequestLog

# The actual DB write function (runs in background)
async def write_log_to_db(log_data: dict):
    async with AsyncSessionLocal() as session:
        db_log = APIRequestLog(**log_data)
        session.add(db_log)
        await session.commit()

async def log_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    try:
        response = await call_next(request)
    except Exception as e:
        # If app crashes, we still want to log the error (500)
        process_time = (time.time() - start_time) * 1000
        log_data = {
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "status_code": 500,
            "process_time_ms": process_time,
            "client_ip": request.client.host if request.client else "unknown"
        }
        # Force a write immediately since we are crashing
        await write_log_to_db(log_data)
        raise e

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # Calculate processing time
    process_time = (time.time() - start_time) * 1000
    
    # Prepare log data
    log_data = {
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "status_code": response.status_code,
        "process_time_ms": process_time,
        "client_ip": request.client.host if request.client else "unknown"
    }

    # CRITICAL: Attach the DB write to the response background tasks.
    # This ensures the response is sent to the user FIRST, 
    # and the DB write happens AFTER.
    response.background = BackgroundTask(write_log_to_db, log_data)
    
    return response