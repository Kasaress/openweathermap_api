import requests
from apps.config import config
from flask import current_app as app
from .exceptions import FailGeoException


class WeatherManager:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _get_url(self, lat: float, lon: float) -> str:
        return config.get('weather_url').format(
            lat=lat,
            lon=lon,
            API_key=self.api_key
        )

    def _get_weater_data(self, url: str) -> dict:
        try:
            response = requests.get(url, timeout=3)
        except Exception as error:
            app.logger.error(error)
            raise FailGeoException(error)
        else:
            return response.json()

    def get_weater(self, lat: float, lon: float) -> tuple[float]:
        url = self._get_url(lat, lon)
        return self._get_weater_data(url).get('main')

    def get_temperature(self, lat: float, lon: float) -> float:
        url = self._get_url(lat, lon)
        return self._get_weater_data(url).get('main').get('temp')
