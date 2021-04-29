from . import api

from .. import db, models
from flask import current_app, jsonify, make_response, request, session, g

import base64


@api.route("/index")
def index():

    return "hhh"

