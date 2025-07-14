# utils/logger.py
from loguru import logger
import sys
import logging


def setup_logger(log_level):
    # Удаляем все стандартные обработчики loguru
    logger.remove()

    # Добавляем вывод в консоль
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level=log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Класс-перехватчик стандартного logging → loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno
            logger.opt(depth=6, exception=record.exc_info).log(
                level, record.getMessage()
            )

    # Перехватываем стандартный logging и перенаправляем в loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)
