from pydantic import BaseSettings

class Settings(BaseSettings):
    api_key: str
    api_key_secret: str
    bearer_token: str
    access_token: str
    access_token_secret: str
    django_secret_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()