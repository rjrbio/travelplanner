from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Travel Planner"
    environment: str = "development"
    ollama_url: str = "http://localhost:11434"
    vector_store_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

settings = Settings()
