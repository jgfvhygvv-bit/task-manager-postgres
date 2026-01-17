# app/config.py
import os
from pathlib import Path

basedir = Path(__file__).parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-123")

    # PostgreSQL конфигурация
    POSTGRES_USER = os.getenv("POSTGRES_USER", "taskuser")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "taskpassword")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "taskmanager")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Для тестов используем SQLite
    SQLALCHEMY_DATABASE_URI_TEST = "sqlite:///:memory:"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI_TEST


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
