from pathlib import Path

from pydantic import DirectoryPath, PostgresDsn, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = 'Authentication Service'
    database_url: str = "sqlite+aiosqlite:///./test.db"
    port: int = 8001
    debug: bool = True
    secret_key: str = 'insecure-wuylv9a5lfgi*@vlk1ij75uvepq21s8k-cb549*&iuvgjui95s'
    base_dir: DirectoryPath = Path(__file__).resolve().parent.parent.parent
    reload: bool = True
    factory: bool = True
    db_echo: bool = False
    host: str = "localhost"
    workers_count: int = 4 
    social_base_url:  AnyHttpUrl = "http://127.0.0.1:8000"  
    allowed_origins: list = ["*"]
    sentry_logger_url: AnyHttpUrl = None

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
