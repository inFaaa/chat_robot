from . import web
from app.models.query_pair import QueryPair
import urllib.parse

@web.route('/<query_string>')
def func(query_string):
    query_string = str(query_string)
    qp = QueryPair()
    # with db.auto_commit():
    answer = qp.get_answer_by_query(query_string).answer

    return answer

