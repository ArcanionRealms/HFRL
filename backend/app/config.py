"""
Application configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://localhost:5501",
        "http://localhost:5502",
        "file://",
    ]
    
    # Database Settings (for future use)
    DATABASE_URL: str = "sqlite:///./hfrl.db"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # AI Provider API Keys (should be set via environment variables)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    KIMI_API_KEY: str = ""
    
    # Request Timeouts
    REQUEST_TIMEOUT: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

