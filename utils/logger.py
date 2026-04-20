"""
Настройка логирования для проекта
"""
import logging
import sys
from typing import Optional


def setup_logger(
        name: Optional[str] = None,
        level: int = logging.INFO,
        log_format: Optional[str] = None,
        log_file: Optional[str] = None
) -> logging.Logger:
    """
    Настройка логгера с форматированием

    Args:
        name: имя логгера (если None, возвращается root логгер)
        level: уровень логирования
        log_format: формат сообщений
        log_file: путь к файлу для логирования (опционально)

    Returns:
        Настроенный логгер
    """
    if log_format is None:
        log_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        # Цветной формат для консоли (если терминал)
        if sys.stdout.isatty():
            log_format = '\033[36m%(asctime)s\033[0m | \033[33m%(levelname)-8s\033[0m | \033[35m%(name)s\033[0m | %(message)s'

    # Создаём или получаем логгер
    logger = logging.getLogger(name) if name else logging.getLogger()
    logger.setLevel(level)

    # Очищаем существующие обработчики, чтобы не дублировать
    logger.handlers.clear()

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt='%H:%M:%S'))
    logger.addHandler(console_handler)

    # Файловый обработчик (если указан путь)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_format = '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
        file_handler.setFormatter(logging.Formatter(file_format, datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Получает логгер с стандартными настройками

    Args:
        name: имя логгера (обычно __name__)

    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)

    # Если логгер ещё не настроен, настраиваем его
    if not logger.handlers:
        setup_logger(name)

    return logger


# Предустановленные логгеры для разных компонентов
class Loggers:
    API = get_logger("api")
    TESTS = get_logger("tests")
    UTILS = get_logger("utils")
    MODELS = get_logger("models")


# Пример использования
if __name__ == "__main__":
    # Тестирование логгера
    test_logger = setup_logger("test_logger", level=logging.DEBUG)

    test_logger.debug("Это отладочное сообщение")
    test_logger.info("Это информационное сообщение")
    test_logger.warning("Это предупреждение")
    test_logger.error("Это ошибка")

    # Использование get_logger
    another_logger = get_logger("another")
    another_logger.info("Логгер с настройками по умолчанию")