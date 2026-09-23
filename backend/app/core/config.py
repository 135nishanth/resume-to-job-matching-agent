from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "Intelligent Resume-to-Job Matching Agent"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = "sqlite:///./resume_matcher.db"

    # NLP & Embedding Model
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Matching Thresholds
    EXACT_MATCH_THRESHOLD: float = 0.88
    SEMANTIC_MATCH_THRESHOLD: float = 0.50

    # Configurable Scoring Weights (Must sum to 1.0)
    WEIGHT_REQUIRED_SKILLS: float = 0.50
    WEIGHT_PREFERRED_SKILLS: float = 0.15
    WEIGHT_EXPERIENCE: float = 0.20
    WEIGHT_EDUCATION: float = 0.05
    WEIGHT_PROJECTS: float = 0.10

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
