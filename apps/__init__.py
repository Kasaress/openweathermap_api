# -*- encoding: utf-8 -*-
"""Initialise config"""
import logging
import os
from importlib import import_module

from concurrent_log_handler import ConcurrentRotatingFileHandler
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

from modules.managers import GeoManager, WeatherManager

if not os.path.exists("logs"):
    os.mkdir("logs")

# Заменяет файл после достижения 5MB, хранит 5 старых копий.
rotateHandler = ConcurrentRotatingFileHandler(
    "logs/system.log", "a", 5 * 1024 * 1024, 5, encoding="utf-8"
)
rotateHandler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
    )
)
rotateHandler.setLevel(logging.DEBUG)

db = SQLAlchemy()
geo_manager = GeoManager()
weather_manager = WeatherManager()
scheduler = APScheduler()


def register_extensions(app: Flask):
    """Регистрация расширений."""
    db.init_app(app)
    scheduler.init_app(app)
    geo_manager.init_app(app)
    weather_manager.init_app(app)


def register_blueprints(app: Flask):
    """Регистрация модулей приложения."""
    for module_name in ("home", ):
        module = import_module(f"apps.{module_name}.routes")
        app.register_blueprint(module.blueprint)


def configure_database(app: Flask):
    """Конфигурация БД."""
    def initialize_database():
        with app.app_context():
            from apps.home.models import City, Weather
            db.create_all()
            from modules.init_defaults import init_defaults
            init_defaults()

    initialize_database()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def add_scheduler_jobs(app, scheduler, config):
    from modules.init_defaults import add_jobs
    add_jobs(app, scheduler)


def create_app(config):
    """Создание приложения."""
    app = Flask(__name__)
    app.config.from_object(config)
    app.logger.addHandler(rotateHandler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("========== API START ==========")
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    scheduler.start()
    add_scheduler_jobs(app, scheduler, config)
    return app
