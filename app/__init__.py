# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config

db = SQLAlchemy()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Импортируем модели чтобы они зарегистрировались
    from . import models

    # Создаем таблицы при запуске
    with app.app_context():
        db.create_all()

    return app
