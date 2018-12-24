from werobot import WeRoBot
robot = WeRoBot(token='token')
@robot.handler
def hello(message):
    return 'Hello World!'

from flask import Flask
from werobot.contrib.flask import make_view
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'


app.add_url_rule(rule='/', # WeRoBot 的绑定地址
                endpoint='werobot', # Flask 的 endpoint
                view_func=make_view(robot),
                methods=['GET', 'POST'])

app.run()