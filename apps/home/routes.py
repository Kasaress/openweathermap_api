from apps import geo_manager, weather_manager, db
from apps.home import blueprint
from flask import jsonify
from apps.home.models import City
import uuid


@blueprint.route("/", methods=["GET"])
def index():
    
    lat, lon = geo_manager.get_coordinates('London')
    temperature = weather_manager.get_temperature(lat, lon)
    london = City(
        uuid=str(uuid.uuid4()),
        name='London',
        latitude=lat,
        longitude=lon
    )
    db.session.add(london)
    db.session.commit()
    return jsonify({
        'lat': lat,
        'lon': lon,
        'temp': temperature,
        })
