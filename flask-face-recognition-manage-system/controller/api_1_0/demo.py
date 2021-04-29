from . import api

from .. import db, models


@api.route("/index")
def index():
    return "index page"
