from flask import Flask
from app.models.base import db
import werobot

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')

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
    robot.config['HOST'] = '0.0.0.0'
    robot.config['POST'] = 8889
    return robot
