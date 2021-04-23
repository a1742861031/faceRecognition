# 配置信息
import redis
import os
from datetime import timedelta


class Config(object):
    SECRET_KEY = os.urandom(24)
    # 数据库
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/facerec"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    # flask-session 配置
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期


class DevlopmentConfig(Config):
    # 开发环境配置信息
    DEBUG = True
    pass


class ProductionConfig(Config):
    pass


config_map = {
    "develop": DevlopmentConfig,
    "product": ProductionConfig
}