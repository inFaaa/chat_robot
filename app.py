from flask import Flask
from bot import robot
from werobot.contrib.flask import make_view
from library import app

app.add_url_rule(rule='/robot/', # WeRoBot 挂载地址
                 endpoint='werobot', # Flask 的 endpoint
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])