import uuid
from flask import current_app as app

from apps import db
from apps.home.models import City
from apps.home.largest_cities import cities
from apps import geo_manager


def init_defaults():
    """Заполнить таблицу городов стартовыми данными."""
    for city in cities:
        name = city.lower()
        if not City.query.filter_by(name=name).first():
            lat, lon = geo_manager.get_coordinates(city)
            new_city = City(
                uuid=str(uuid.uuid4()),
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
