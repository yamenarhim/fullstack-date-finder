from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

from app.core.config import settings
from app.api.v1.router import api_router

from app.core.database import init_db 
from app.middleware.logger import log_middleware 
from starlette.middleware.base import BaseHTTPMiddleware 

# 1. Define Lifespan (Startup/Shutdown logic)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the cache
    print("Starting up... Initializing Cache")
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    await init_db()
    yield
    # Shutdown: Clean up if needed (nothing for in-memory)
    print("Shutting down...")

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan  # <--- Attach the lifespan here
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    application.add_middleware(SlowAPIMiddleware)
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application

app = get_application()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Date Calculator API",
        "docs": "/docs",
        "version": settings.VERSION
    }