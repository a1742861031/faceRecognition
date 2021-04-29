# -*- coding: utf-8 -*-
# @Time    : 2021/4/26 17:19
# @Author  : bobo
# @Email   : 2460417845@qq.com
# @File    : __init__.py.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *
import pymysql
from . import controller
pymysql.install_as_MySQLdb()
# 创建数据库
db = SQLAlchemy()


def create_app():
    # 初始化app
    app = Flask(__name__)

    # 设置跨域
    CORS(app, supports_credentials=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/facerec'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['DEBUG'] = True
    db.init_app(app)
    from . import api
    app.register_blueprint(api.api, url_prefix="/api/facereg")
    return app