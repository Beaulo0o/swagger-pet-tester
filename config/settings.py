"""
Конфигурация проекта
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Основные настройки"""

    BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")

    # Таймауты (в секундах)
    CONNECTION_TIMEOUT = int(os.getenv("CONNECTION_TIMEOUT", 10))
    READ_TIMEOUT = int(os.getenv("READ_TIMEOUT", 10))

    # Заголовки по умолчанию
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Логирование запросов
    LOG_REQUESTS = os.getenv("LOG_REQUESTS", "True").lower() == "true"
    LOG_RESPONSES = os.getenv("LOG_RESPONSES", "True").lower() == "true"


config = Config()
