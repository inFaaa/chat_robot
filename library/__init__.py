from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
# robot
from werobot import WeRoBot
import jieba

robot = WeRoBot(token='tokenhere')

@robot.handler
def processer(message):
    seg_list = jieba.cut(message.content)
    return "|".join(seg_list) 
    
from werobot.contrib.flask import make_view

FATH_TO_CONFIG = '../instance/config.py' # 需要修改

app = Flask(__name__)
#app.config.from_object('config')
app.config.from_pyfile(FATH_TO_CONFIG)

app.add_url_rule(rule='/', # WeRoBot 挂载地址
                 endpoint='werobot', # Flask 的 endpoint
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])

CORS(app, supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"])
db = SQLAlchemy(app)

import library.question.resources
import library.knowledge.resources

api = Api(app)

# api.add_resource(library.question.resources.QueryQuestionByID, '/api/quesiton/<string: q_id>')
# api.add_resource(library.question.resources.QueryQuestionByTitle, '/api/quesiton/<string: q_title>')
api.add_resource(library.question.resources.QueryAllQuestion, '/api/quesiton/all')
# api.add_resource(library.knowledge.resources.QueryKnowledgeByID, '/api/knowledge/<string: k_id>')
# api.add_resource(library.knowledge.resources.QueryKnowledgeByTitle, '/api/knowledge/<string: k_title>')
api.add_resource(library.knowledge.resources.QueryAllKnowledge, '/api/knowledge/all')


