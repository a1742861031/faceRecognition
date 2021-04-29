from . import api
from flask import current_app, jsonify, make_response, request, session, g
from .. import redis_store
from .. import models, db
from sqlalchemy.exc import IntegrityError
from .. import Utils
import base64
import json


@api.route('/profile', methods=["GET"])
@Utils.login_required
def getProfile():
    """
    获取用户的信息
    :return:
    """
    id = g.id
    user = models.User.query.filter_by(id=id).first()
    print(user)
    return jsonify(code=200, msg="获取成功",
                   data={'id': user.id,
                         'mobile': user.mobile,
                         'isSuperAdmin': user.isSuperAdmin,
                         'name': user.Name})


