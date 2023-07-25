from pathlib import Path

from pydantic import DirectoryPath, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_name: str = 'service_name'
    database_url: PostgresDsn = 'postgresql+asyncpg://postgres:0509@localhost:5432/talknaw'
    port: int = 8000
    debug: bool = True
    secret_key: str = 'insecure-wuylv9a5lfgi*@vlk1ij75uvepq21s8k-cb549*&iuvgjui95s'
    base_dir: DirectoryPath = Path(__file__).resolve().parent.parent.parent
    reload: bool = True
    factory: bool = True
    db_echo: bool = False
    host: str = "localhost"
    workers_count: int = 4 

    class Config:
        env_prefix = ""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
