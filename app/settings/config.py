from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "File Storage API"

    # Базы
    DATABASE_URL_ASYNC: str
    DATABASE_URL_SYNC: str

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
