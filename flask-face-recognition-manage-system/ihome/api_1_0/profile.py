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


@api.route('/allface', methods=["GET"])
# @Utils.login_required
def getAllFace():
    """获取所有注册过的人脸信息"""
    # path：L:\毕设项目\keras-face-recognition-master\face_dataset
    users = models.User.query.all()
    data = []
    for user in users:
        f = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + user.Name + '.jpg', 'rb')  # 二进制方式打开图文件
        img_base64 = base64.b64encode(f.read())
        image = img_base64.decode()
        f.close()
        data.append({'id': user.id, 'mobile': user.mobile, 'name': user.Name, 'image': image})
    return jsonify(code=200, msg="获取图片信息成功", data=data)
