
import datetime

from flask import current_app as app

from apps import db
from apps.home.models import City, Weather

from .exceptions import NotFoundCityException
from .managers import GeoManager, WeatherManager


class Collector:
    def __init__(
        self,
        geo_manager: GeoManager,
        weather_manager: WeatherManager
    ) -> None:
        self.geo_manager = geo_manager
        self.weather_manager = weather_manager

    def _get_city(self, city_name: str) -> City:
        name = city_name.lower()
        city = City.query.filter_by(name=name).first()
        if not city:
            app.logger.error(f'Город {city_name} не найден.')
            raise NotFoundCityException
        return city

    def _get_or_create_weather(self, city) -> Weather:
        weater = Weather.query.filter_by(city_id=city.id).first()
        if not weater:
            new_weather = Weather(
                city_id=city.id,
            )
            db.session.add(new_weather)
            db.session.commit()
            app.logger.info(
                f'Создана новая запись погоды для города {city}'
            )
            return new_weather
        return weater

    def _update_temp(self, city, temp: float) -> None:
        weater = self._get_or_create_weather(city)
        weater.temperature = temp
        weater.edited_at = datetime.datetime.utcnow()
        db.session.add(weater)
        db.session.commit()

    def update_temp(self, name: str) -> None:
        city = self._get_city(name)
        lat, lon = self.geo_manager.get_coordinates(city.name)
        if not lat or not lon:
            app.logger.warning(f'Невозможно определить координаты {city.name}.')
            return
        temp = self.weather_manager.get_temperature(lat, lon)
        self._update_temp(city, temp)
        app.logger.info(f'Обновление {city.name}, температура: {temp}')
