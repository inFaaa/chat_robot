from . import web
from . import robot
from app.models.base import db
from app.models.query_pair import QueryPair


@robot.text
def test_func(message):
    #query数据库
    query_string = str(message.content)
    qp = QueryPair()
    # with db.auto_commit():
    answer = qp.get_answer_by_query(query_string).answer
    return answer


#感觉不能这样做
# from werobot.contrib.flask import make_view
# web.add_url_rule(rule=
#
# )

