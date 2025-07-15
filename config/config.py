import os
from dataclasses import dataclass
from dotenv import load_dotenv  # pip install python-dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


@dataclass
class DatabaseConfig:
    name: str
    host: str
    user: str
    password: str


@dataclass
class TgBot:
    token: str
    log: str


@dataclass
class Config:
    bot: TgBot
    # db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    if path:
        load_dotenv(dotenv_path=path)

    return Config(
        bot=TgBot(
            token=os.getenv("BOT_TOKEN", ""),
            log=os.getenv("LOG_LEVEL", "INFO"),
        )
        # db=DatabaseConfig(
        #     name=os.getenv("DB_NAME", ""),
        #     host=os.getenv("DB_HOST", ""),
        #     user=os.getenv("DB_USER", ""),
        #     password=os.getenv("DB_PASSWORD", "")
        # )
    )
