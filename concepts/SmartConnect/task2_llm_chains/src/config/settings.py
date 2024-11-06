from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent 

class Settings(BaseSettings):
    """Application settings using Pydantic"""
    
    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR/'.env'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
    
    test_value: str  
    openai_api_key: str
    model_name: str = "gpt-3.5-turbo"

@lru_cache
def get_settings() -> Settings:
     """Cache settings to avoid loading .env file multiple times"""
     
     try:
         return Settings()
     except Exception as e:
         raise ValueError(f"Error loading settings: {str(e)}")
    