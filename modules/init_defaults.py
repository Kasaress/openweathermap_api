from flask import current_app as app
from sqlalchemy import select

from apps import db, geo_manager
from apps.config import config
from apps.home.largest_cities import cities
from apps.home.models import City
from apps.home.tasker import weather_job


def init_defaults():
    """Заполнить таблицу городов стартовыми данными."""
    for city in cities:
        name = city.lower()
        query = select(City).where(City.name == name)
        if not db.session.scalars(query).first():
            lat, lon = geo_manager.get_coordinates(city)
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


def add_jobs(app, scheduler):
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
            print(error)
