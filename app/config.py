"""
Database configuration and environment variables
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database configuration - use either DATABASE_URL or AWS RDS parameters
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", None)
    
    # AWS RDS Configuration (alternative to DATABASE_URL)
    USE_AWS_RDS: bool = os.getenv("USE_AWS_RDS", "false").lower() == "true"
    RDS_HOST: str = os.getenv("RDS_HOST", "")
    RDS_PORT: int = int(os.getenv("RDS_PORT", "5432"))
    RDS_USERNAME: str = os.getenv("RDS_USERNAME", "postgres")
    RDS_PASSWORD: str = os.getenv("RDS_PASSWORD", "")
    RDS_DATABASE: str = os.getenv("RDS_DATABASE", "postgres")
    AWS_REGION: str = os.getenv("AWS_REGION", "eu-north-1")
    USE_IAM_AUTH: bool = os.getenv("USE_IAM_AUTH", "true").lower() == "true"
    RDS_SSL_CERT_PATH: str = os.getenv("RDS_SSL_CERT_PATH", "")
    
    # API configuration
    API_TITLE: str = "Pramith Python API"
    API_VERSION: str = "0.1.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
