from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "hf.co/unsloth/medgemma-1.5-4b-it-GGUF:Q4_K_M"
    REQUEST_TIMEOUT: float = 60.0
    MAX_IMAGE_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: List[str] = ["image/png", "image/jpeg", "image/webp"]
    
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
