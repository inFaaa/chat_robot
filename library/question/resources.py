from flask_restful import Resource
from flask import request

from library.question.models import Question

class QueryAllQuestion(Resource):
    def get(self):
        k = Question()
        data = Question.query.all()

        if data:
            return data
        else:
            return {'message': 'Error!'}, 500