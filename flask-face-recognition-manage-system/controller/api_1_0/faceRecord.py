from . import api
from flask import current_app, jsonify, make_response, request, session, g
from .. import redis_store
from .. import models, db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc
from .. import Utils
import base64
import json
import os
import time


@api.route("/getAll", methods=["GET"])
def getAllRecord():
    rets = db.session.execute("SELECT DATE(time) AS date,count(*) AS num from record GROUP BY date ORDER BY date ASC")
    res = []
    for ret in rets:
        res.append({"time": str(ret.date)[5:], "num": ret.num})
    return jsonify(code=200, msg="获取成功", data=res)


@api.route("/getRecordById", methods=["GET"])
def getRecordByID():
    id = request.args["id"]
    name = (models.Face.query.filter_by(face_id=id).first()).name
    records = models.Inentify_Record.query.filter_by(face_id=id).order_by(models.Inentify_Record.time.desc()).all()
    path = "L:\毕设项目\keras-face-recognition-master\images\\record\\" + name
    filenames = {}
    keys = []
    values = []
    res = []
    for root, dirs, files in os.walk(path):
        for file in files:
            index = file.find(".")
            temp = file[0:index].replace('_', '')
            filenames[temp] = file
            keys.append(temp)
            values.append(file)
    for record in records:
        year = str(record.time.year)
        month = str(record.time.month)
        if len(month) == 1:
            month = '0' + month
        day = str(record.time.day)
        hour = str(record.time.hour)
        minute = str(record.time.minute)
        second = str(record.time.second)
        temp = year + month + day + hour + minute + second
        for key in keys:
            if key == temp:  # 匹配成功
                with open(path + "\\" + filenames.get(key), 'rb') as f:
                    base64_data = base64.b64encode(f.read())
                    s = base64_data.decode()
                    res.append(
                        {"face_id": record.face_id, "name": name, "time": str(record.time), "ip": record.ip, 'image': s})

    return jsonify(code=200, msg="获取刷脸记录成功", data=res)
