# app/logger.py
"""
Модуль логирования для Task Manager
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name="app", log_level=logging.INFO):
    """Настройка логгера с записью в файл и консоль"""

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Если уже есть обработчики, не добавляем новые
    if logger.handlers:
        return logger

    # Создаем папку для логов если ее нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Обработчик для файла (ротация по размеру)
    log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10485760, backupCount=5, encoding="utf-8"  # 10 MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Создаем логгеры для разных модулей
app_logger = setup_logger("app")
db_logger = setup_logger("database")
task_logger = setup_logger("tasks")


def log_task_creation(task_title, task_id=None):
    """Логирование создания задачи"""
    task_logger.info(
        f"Task created: '{task_title}'" + (f" (ID: {task_id})" if task_id else "")
    )


def log_task_deletion(task_title, task_id):
    """Логирование удаления задачи"""
    task_logger.info(f"Task deleted: '{task_title}' (ID: {task_id})")


def log_task_update(task_title, task_id, changes):
    """Логирование обновления задачи"""
    task_logger.info(
        f"Task updated: '{task_title}' (ID: {task_id}) - Changes: {changes}"
    )


def log_api_request(method, endpoint, status_code, duration=None):
    """Логирование API запроса"""
    app_logger.info(
        f"API {method} {endpoint} - Status: {status_code}"
        + (f" - Duration: {duration:.3f}s" if duration else "")
    )


def log_database_operation(operation, table, details=""):
    """Логирование операций с базой данных"""
    db_logger.debug(f"DB {operation} on {table}" + (f" - {details}" if details else ""))
