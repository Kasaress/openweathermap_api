import requests
from apps.config import config
from flask import current_app as app
from .exceptions import FailGeoException


class GeoManager:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _get_url(self, city: str) -> str:
        return config.get('geo_url').format(
            city=city,
            API_key=self.api_key
        )

    def _get_geo_data(self, url: str) -> dict:
        try:
            response = requests.get(url, timeout=3)
        except Exception as error:
            app.logger.error(error)
            raise FailGeoException(error)
        else:
            return response.json()[0]

    def get_coordinates(self, city: str) -> tuple[float]:
        url = self._get_url(city)
        geo_data = self._get_geo_data(url)
        lat = geo_data.get('lat')
        lon = geo_data.get('lon')
        return lat, lon
