from abc import ABC
from typing import final

import requests
from flask import Flask
from flask import current_app as app

from apps.config import config

from .exceptions import ManagerRequestException


class Manager(ABC):
    def __init__(self) -> None:
        self.api_key = None

    @final
    def init_app(self, app: Flask):
        self.api_key = app.config.get('API_KEY')

    def _get_data(self, url: str):
        try:
            response = requests.get(url, timeout=3)
        except Exception as error:
            app.logger.error(error)
            raise ManagerRequestException(error)
        else:
            return response.json()


class GeoManager(Manager):
    def _get_url(self, city: str) -> str:
        return config.get('geo_url').format(
            city=city,
            API_key=self.api_key
        )

    def get_coordinates(self, city: str) -> tuple[float]:
        url = self._get_url(city)
        try:
            geo_data = self._get_data(url)[0]
            lat = geo_data.get('lat')
            lon = geo_data.get('lon')
            return lat, lon
        except ManagerRequestException as error:
            app.logger.error(
                f'Ошибка получения данных от API: {error}'
            )
        except IndexError as error:
            app.logger.error(
                f'API не содержит данные о городе {city}: {error}'
            )
        return None, None


class WeatherManager(Manager):
    def _get_url(self, lat: float, lon: float) -> str:
        return config.get('weather_url').format(
            lat=lat,
            lon=lon,
            API_key=self.api_key
        )

    def get_temperature(self, lat: float, lon: float) -> float:
        if not lat or not lon:
            app.logger.warning('Отсутствуют координаты.')
            return None
        url = self._get_url(lat, lon)
        return self._get_data(url).get('main').get('temp')
