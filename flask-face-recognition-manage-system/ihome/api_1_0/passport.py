from . import api
from flask import current_app, jsonify, make_response, request, session
from .. import redis_store
from .. import models, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


@api.route('/users', methods=["POST"])
def register():
    """注册
    请求的参数 id 密码 验证码 手机号
    参数格式 json
    """
    req_dict = request.get_json()
    # 判断验证码是否正确
    codeid = req_dict.get("codeid")
    code = req_dict.get("code")
    mobile = req_dict.get("mobile")
    id = req_dict.get("id")
    pwd = req_dict.get("pwd")
    name = req_dict.get("name")
    # 图片验证码错误
    if (str(redis_store.get("image_code_%s" % codeid))[2:6]).lower() != code.lower():
        return jsonify(code=4001, msg="图片验证码错误")
    # 图片验证码正确
    else:
        user = models.User(id=id, mobile=mobile, state=0, avatar_url='', Name=name, isSuperAdmin=0)
        user.password = pwd  # 这里会自动调用装饰器里的函数
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            # 数据库操作回滚
            db.session.rollback()
            # 用户id出现重复值
            return jsonify(code=4001, msg="用户id已经存在")
        except Exception as e:
            print(e)
            return jsonify(code=4001, msg="数据库异常")
        # 登录状态保存到session中
        session["id"] = id
        session["mobile"] = mobile
        return jsonify(code=201, msg="注册成功")


@api.route("/sessions", methods=["POST"])
def login():
    """
    用户登录
    参数：用户名 密码 验证码
    :return:
    """
    req_dict = request.get_json()
    codeid = req_dict.get("codeid")
    code = req_dict.get("code")
    id = req_dict.get("id")
    pwd = req_dict.get("pwd")
    # 图片验证码错误
    if (str(redis_store.get("image_code_%s" % codeid))[2:6]).lower() != code.lower():
        return jsonify(code=4001, msg="图片验证码错误")
    # 图片验证码正确
    else:
        user = models.User.query.filter_by(id=id).first()
        # 未查找到
        if user is None:
            return jsonify(code=4001, msg="用户名或密码错误")
        else:
            if user.check_password(passwd=pwd):
                # 保存登录状态
                session["id"] = user.id
                return jsonify(code=200, msg="登录成功", data={'id': user.id, 'stata': user.state, 'mobile': user.mobile})
            else:
                return jsonify(code=4001, msg="用户名或密码错误")


@api.route("/sessions", methods=["GET"])
def check_Login():
    """
    检查登录状态
    """
    """获取session的数据"""
    id = session.get("id")
    print(id)
    if id is not None:
        return jsonify(code=200, msg="用户已经登录", userid=id)
    else:
        return jsonify(code=4001, msg="用户未登录")
    # 尝试通过session获取用户id
    # 因为通过session获取用户id时要通过sessionid
    # id = session.get("id")
    # name = request.cookies.get('session')
    # print(name)
    # print(id)
    # # 如果session中数据id已经存在


@api.route("/sessions", methods=["DELETE"])
def logout():
    """登出"""
    session.clear()
    return jsonify(code=200, msg="成功登出")
