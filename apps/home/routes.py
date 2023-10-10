from apps import collector
from apps.home import blueprint
from flask import jsonify
from modules.exceptions import NotFoundCityException


@blueprint.route("/<city_name>", methods=["GET"])
def index(city_name):
    try:
        collector.update_temperature(city_name)
        return jsonify({
            'city': city_name,
            })
    except NotFoundCityException as error:
        return jsonify({
            'error': str(error),
            })
