from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"
    DB_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
