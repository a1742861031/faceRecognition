# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 20:15
# @Author  : bobo
# @Email   : 2460417845@qq.com
# @File    : __init__.py.py
# 工厂模式

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_cors import *  # 导入模块

# 创建数据库
db = SQLAlchemy()
# 创建redis连接对象
redis_store = None


def create_app(config_name):
    """
    创建flask的应用对象
     :param:conigname:str 配置模式的名字 ("develop","product")
    :return:
    """
    app = Flask(__name__)
    # 设置跨域
    CORS(app, supports_credentials=True)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)

    app.config.from_object(config_class)
    db.init_app(app)
    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)
    # 利用flask-session 将session数据保存到redis中
    Session(app)
    # 补充flask CSRF防护 过滤所有错误请求
    # 注册蓝图
    from . import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")

    return app
