from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from sqlalchemy import and_

# robot
from werobot import WeRoBot
import jieba

robot = WeRoBot(token='tokenhere')

@robot.handler
def processer(message):
    from util import get_entity, get_target_sentenses_index, sub_similar_word

    string = sub_similar_word(message.content)
    # string = message.content
    # entitys= get_entity(message.content)
    # entitys = ' '.join(entitys)#数据库中以空格划分
    from library.knowledge.models import Knowledge
    all_results = Knowledge.query.all()#这里还要针对查询进行改进
    indexs_weight_pair = get_target_sentenses_index(string,[i.k_title for i in all_results])
    answers = []
    for i in range(len(indexs_weight_pair)):
        answers.append(all_results[indexs_weight_pair[i][0]].k_detail)
    # print(answers)
    return answers[0]
    
from werobot.contrib.flask import make_view

FATH_TO_CONFIG = '../instance/config.py'

app = Flask(__name__)
#app.config.from_object('config')
app.config.from_pyfile(FATH_TO_CONFIG)

app.add_url_rule(rule='/',
                 endpoint='werobot',
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])

CORS(app, supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"])
db = SQLAlchemy(app)

from library.question.resources import QuestionResolver
from library.knowledge.resources import KnowledgeResolver

api = Api(app)

api.add_resource(QuestionResolver, '/api/quesiton')
api.add_resource(KnowledgeResolver, '/api/knowledge', '/api/knowledge/<keyword>')



