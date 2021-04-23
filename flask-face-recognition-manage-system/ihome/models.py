from . import db, models

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user_profile"
    id = db.Column(db.String(255), primary_key=True)  # 用户编号
    password_hash = db.Column(db.String(128), nullable=False)  # 用户密码
    mobile = db.Column(db.String(255), nullable=False)  # 手机号
    avatar_url = db.Column(db.String(255))
    state = db.Column(db.INTEGER)
    isSuperAdmin = db.Column(db.INTEGER)
    Name = db.Column(db.String(50))  # 用户的真实姓名 与后端人脸数据库的姓名应该相同
    @property
    def password(self):
        """获取password属性时调用"""
        raise AttributeError("不可读")

    @password.setter
    def password(self, passwd):
        """设置password时调用"""
        self.password_hash = generate_password_hash(passwd)

    def check_password(self, passwd):
        """检查密码正确性"""
        return check_password_hash(self.password_hash, passwd)
