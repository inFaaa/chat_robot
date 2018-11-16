from flask import Flask
from app.models.base import db
import werobot

def create_app():
    app = Flask(__name__)

    #写了好像没用？？还是在5000默认端口跑的
    # app.config.from_object('app.setting')
    # app.config.from_object('app.secure')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/querypair'
    register_blueprint(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    # login????
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)

def create_robot():
    robot = werobot.WeRoBot(token='token')
    robot.config['HOST'] = '127.0.0.1'
    robot.config['PORT'] = 8889
    return robot
