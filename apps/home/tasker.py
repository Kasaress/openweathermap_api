from flask import current_app as app

from apps import geo_manager, scheduler, weather_manager
from modules.collector import Collector

from .largest_cities import cities


def _weather_job():
    collector = Collector(geo_manager, weather_manager)
    for city in cities:
        collector.update_temp(city)


def weather_job():
    """Запускает задачу обновления температуры."""
    with scheduler.app.app_context():
        _weather_job()
        app.logger.info('Выполнена задача "weather_job"')
