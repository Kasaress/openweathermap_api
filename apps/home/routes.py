from apps import db
from apps.config import config
from apps.home import blueprint
from flask import current_app as app
from flask import jsonify


@blueprint.route("/index", methods=["GET"])
def profile():
    return jsonify({'status': 'success'})