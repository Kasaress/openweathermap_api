from apps import geo_manager, weather_manager
from apps.home import blueprint
from flask import jsonify


@blueprint.route("/", methods=["GET"])
def index():
    lat, lon = geo_manager.get_coordinates('London')
    temperature = weather_manager.get_temperature(lat, lon)
    return jsonify({
        'lat': lat,
        'lon': lon,
        'temp': temperature,
        })
