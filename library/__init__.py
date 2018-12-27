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
    from util import get_entity, get_target_sentenses_index

    from library.knowledge.models import Knowledge
    all_results = Knowledge.query.all()#这里还要针对查询进行改进
    indexs_weight_pair = get_target_sentenses_index(message.content,[i.k_title for i in all_results])
    data = []
    if indexs_weight_pair:
        for i in range(len(indexs_weight_pair)):
            data.append(all_results[indexs_weight_pair[i][0]].to_json())
    else:
        return "没听懂，可以再说清楚一点吗？"
    # print(answers)
    answer = "你想问的是不是：" + data[0]['k_title'] + "\n---\n" + data[0]['k_detail']
    return answer
    
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



