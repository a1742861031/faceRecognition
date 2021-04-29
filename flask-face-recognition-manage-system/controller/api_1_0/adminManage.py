from . import api
from flask import current_app, jsonify, make_response, request, session, g
from .. import redis_store
from .. import models, db
from sqlalchemy.exc import IntegrityError
from .. import Utils
import base64
import json
import os


@api.route("/admins", methods=["GET"])
def getAllAdmins():
    """查询所有的管理员信息
        参数：无 或者管理员的姓名
        返回值
        id,mobile,state,name,isSuperAdmin
    """
    if len(request.args) == 0:
        users = models.User.query.all()
    else:
        users = models.User.query.filter(
            models.User.Name.like(("%" + request.args["name"] + "%")) if request.args["name"] is not None else "").all()
    data = []
    for user in users:
        data.append({'id': user.id, 'mobile': user.mobile, 'state': user.state, 'isSuperAdmin': user.isSuperAdmin,
                     'name': user.Name})
    return jsonify(code=200, msg="获取管理员列表成功", data=data)


@api.route("/admin", methods=["GET"])
def getAdmin():
    """
    通过id获取管理员信息
    :return: id,mobile,state,name,isSuperAdmin
    """
    user = models.User.query.filter_by(id=request.args["id"]).first()
    return jsonify(code=200, msg="获取管理员信息成功",
                   data={'id': user.id, 'mobile': user.mobile, 'state': user.state, 'isSuperAdmin': user.isSuperAdmin,
                         'name': user.Name})


@api.route("/admin", methods=["POST"])
def editAdmin():
    """
    修改管理员信息
    :return: {code,msg}
    """
    req_dict = request.get_json()
    user = models.User.query.filter_by(id=req_dict.get("id")).first()
    user.state = req_dict.get("state")
    user.Name = req_dict.get("name")
    user.mobile = req_dict.get("mobile")
    user.isSuperAdmin = req_dict.get("isSuperAdmin")
    if req_dict.get("pwd") != "":
         user.password = req_dict.get("pwd")
    db.session.commit()
    return jsonify(code=201, msg="提交修改成功")


@api.route('/admin', methods=["DELETE"])
def deleteAdmin():
    """
    删除该管理员
    :return:
    """
    user = models.User.query.filter_by(id=request.args["id"]).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify(code=201, msg="删除成功")