# -*- coding: utf-8 -*-
# @Time    : 2021/4/20 20:44
# @Author  : bobo
# @Email   : 2460417845@qq.com
# @File    : __init__.py.py
from flask import Blueprint
# 创建蓝图对象
api = Blueprint("api_1_0", __name__)
# 导入蓝图的视图函数
from . import demo
from . import verify_code
from . import passport, profile, faceManage,test,adminManage