from pathlib import Path
from typing import Union

from pydantic import AnyHttpUrl, DirectoryPath, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings

from app.utils.type_extra import SQLiteDsn


class Settings(BaseSettings):
    service_name: str
    database_url: Union[PostgresDsn, SQLiteDsn]
    port: int = 8001
    debug: bool = True
    secret_key: str
    base_dir: DirectoryPath = Path(__file__).resolve().parent.parent.parent
    reload: bool = True
    factory: bool = True
    db_echo: bool = False
    host: str = "localhost"
    workers_count: int = 4
    social_base_url: AnyHttpUrl
    allowed_origins: list = ["*"]
    sentry_logger_url: AnyHttpUrl
    default_from_email: EmailStr = "example@go.com"
    email_password: str = "awesomepass"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
