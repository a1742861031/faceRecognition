# 启动falsk服务端项目


from ihome import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import session

# 创建app
app = create_app("develop")

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    app.run()
    #manager.run()
