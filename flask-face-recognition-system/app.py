# 启动falsk服务端项目


from faceRec import create_app, db
from  faceRec import controller
# 创建app
app = create_app()
dododo = controller.face_rec()

if __name__ == "__main__":
    app.run()
    # manager.run()
