from flask import current_app as app

from apps import collector, scheduler

from .largest_cities import cities


def weather_job():
    with scheduler.app.app_context():
        for city in cities:
            collector.update_temperature(city)
        app.logger.info('Выполнена задача "weather_job"')
