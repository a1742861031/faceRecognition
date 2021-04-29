from . import db, models

class Face(db.Model):
    __tablename__ = "face"
    face_id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)  # 人脸编号
    state = db.Column(db.Boolean, nullable=False, default=False)  # 人脸状态
    reg_time = db.Column(db.DateTime, nullable=False)  # 注册时间
    name = db.Column(db.String(50), nullable=False)  # 人脸对应的姓名


class Inentify_Record(db.Model):
    __tablename__ = "record"
    face_id = db.Column(db.INTEGER, db.ForeignKey('face.face_id'), primary_key=True, )
    time = db.Column(db.DateTime, nullable=False)
    isSuccess = db.Column(db.Boolean, nullable=False)
