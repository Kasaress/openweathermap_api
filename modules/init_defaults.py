from flask import current_app as app
from sqlalchemy import select

from apps import db, geo_manager
from apps.config import config
from apps.home.largest_cities import cities
from apps.home.models import City
from apps.home.tasker import weather_job


def init_defaults():
    """Заполняет таблицу городов стартовыми данными."""
    for city in cities:
        name = city.lower()
        query = select(City).where(City.name == name)
        if db.session.scalars(query).first():
            continue
        lat, lon = geo_manager.get_coordinates(city)
        if not lat or not lon:
            app.logger.error(f"Ошибка получения координат {name}.")
            continue
        try:
            new_city = City(
                name=name,
                latitude=lat,
                longitude=lon
            )
            db.session.add(new_city)
            app.logger.info(
                f"В таблицу 'City' добавлен город: {new_city}. "
                f"latitude: {new_city.latitude},  "
                f"longitude: {new_city.longitude}"
            )
            db.session.commit()
        except Exception as error:
            app.logger.error(f"Ошибка сохранения координат: {error}.")


def add_jobs(app, scheduler):
    """Добавляет регулярную задачу обновления температуры."""
    with app.app_context():
        try:
            scheduler.add_job(
                'Обновление температуры',
                weather_job,
                trigger="interval",
                minutes=config.get('scheduler_interval'),
                replace_existing=True,
            )
            app.logger.info("Добавлена новая задача.")
        except Exception as error:
            app.logger.error(error)
