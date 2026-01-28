from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Date Calculator API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # React Default Port
        "http://localhost:5173",  # Vite/Vue Default Port
        "http://localhost:8000",
    ]

    # NEW WAY: Use SettingsConfigDict instead of class Config
    model_config = SettingsConfigDict(
        case_sensitive=True,
        # env_file=".env"  # Optional: logic to read from .env file
    )

    

settings = Settings()