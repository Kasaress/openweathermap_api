from apps import db
from apps.config import config
from apps.home import blueprint
from flask import current_app as app
from flask import jsonify
from modules.geo_manager import GeoManager
from modules.weather_manager import WeatherManager


@blueprint.route("/", methods=["GET"])
def index():
    geo_manager = GeoManager(config.get('api_key'))
    lat, lon = geo_manager.get_coordinates('London')
    weater_manager = WeatherManager(config.get('api_key'))
    temperature = weater_manager.get_temperature(lat, lon)

    return jsonify({
        'lat': lat,
        'lon': lon,
        'temp': temperature,
        })
