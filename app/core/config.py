from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI RAG"
    debug: bool = True

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
