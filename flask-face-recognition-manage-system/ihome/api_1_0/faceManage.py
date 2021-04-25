from . import api
from flask import current_app, jsonify, make_response, request, session, g
from .. import redis_store
from .. import models, db
from sqlalchemy.exc import IntegrityError
from .. import Utils
import base64
import json
import os


@api.route('/allfaces', methods=["GET"])
def getAllFace():
    """
    ""获取所有注册过的人脸信息
    参数:通过Id 或者姓名 或者无
  path：L:\毕设项目\keras-face-recognition-master\face_dataset
    """
    if len(request.args) == 0:
        faces = models.Face.query.all()
    else:
        faces = models.Face.query.filter(models.Face.name.like(("%" + request.args["name"] + "%")) if request.args["name"] is not None else "").all()
    data = []
    for face in faces:
        try:
            f = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + face.name + '.jpg', 'rb')  # 二进制方式打开图文件
        except:
            f = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + '默认' + '.jpg', 'rb')  # 二进制方式打开图文件
        img_base64 = base64.b64encode(f.read())
        image = img_base64.decode()
        f.close()
        data.append({'id': face.face_id, 'name': face.name, 'image': image, 'state': face.state})
    return jsonify(code=200, msg="获取图片信息成功", data=data)


@api.route('/face', methods=["GET"])
# @Utils.login_required
def getFaceById():
    """
    通过id获取人脸信息
    :return:
    """
    id = request.args.get("id")
    print(id)
    face = models.Face.query.filter_by(face_id=id).first()
    try:
        f = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + face.name + '.jpg', 'rb')  # 二进制方式打开图文件
    except:
        f = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + '默认' + '.jpg', 'rb')  # 二进制方式打开图文件
    img_base64 = base64.b64encode(f.read())
    image = img_base64.decode()
    return jsonify(code=200, msg="获取单条用户信息成功",
                   data={'id': face.face_id, 'name': face.name, 'state': face.state, 'image': image})


@api.route('/face', methods=["POST"])
def editFace():
    """修改或提交人脸信息"""
    req_dict = request.get_json()

    id = req_dict.get("id")
    face = models.Face.query.filter_by(face_id=id).first()

    face.name = req_dict.get("name")
    face.state = req_dict.get("state")
    # 保存图片到本地
    image_base64 = str(req_dict.get("image"))
    imagedata = base64.b64decode(image_base64.split(',')[1])
    file = open(r'L:\毕设项目\keras-face-recognition-master\face_dataset\\' + req_dict.get("name") + '.jpg',
                "wb")
    file.write(imagedata)
    file.close()
    db.session.commit()
    return jsonify(code=201, msg="修改信息成功")


@api.route('/face', methods=["DELETE"])
def deleteFace():
    id = request.args["id"]
    face = models.Face.query.filter_by(face_id=id).first()
    db.session.delete(face)
    db.session.commit()
    return jsonify(code=200, msg="删除人脸数据成功")
