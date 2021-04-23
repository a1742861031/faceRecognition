from . import api
from .. import Utils
from .. import redis_store
from flask import current_app, jsonify, make_response


@api.route("/image_codes/<image_code_id>")
def get_img_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id:图片验证码的编号
    :return: 验证码图片
    """
    # 生成图片验证码
    # 名字 文本 图片数据
    name, text, image_data = Utils.captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中 设置有效期
    redis_store.set("image_code_%s" % image_code_id, text)
    # 设计redis有效期
    try:
        redis_store.expire("image_code_%s" % image_code_id, 180)
    except Exception as e:
        # 捕获异常
        return jsonify(errno=4001, errmsg="保存图片验证码信息失败")
    # 返回图片数据
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
