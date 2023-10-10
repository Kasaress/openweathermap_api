from flask import current_app as app

from apps import geo_manager, scheduler, weather_manager
from modules.collector import Collector

from .largest_cities import cities


def weather_job():
    """Запускает задачу обновления температуры."""
    with scheduler.app.app_context():
        collector = Collector(geo_manager, weather_manager)
        for city in cities:
            collector.update_temperature(city)
        app.logger.info('Выполнена задача "weather_job"')
