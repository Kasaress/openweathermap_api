from flask import jsonify

from apps.home import blueprint


@blueprint.route("/", methods=["GET"])
def index():
    return jsonify({
        'status': 'я работаю',
        })
