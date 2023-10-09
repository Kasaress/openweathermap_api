# -*- encoding: utf-8 -*-
"""init module"""

from flask import Blueprint

blueprint = Blueprint("home_blueprint", __name__, url_prefix="")
