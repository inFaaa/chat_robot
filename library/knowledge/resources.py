from flask_restful import Resource
from flask import request

from library.knowledge.models import Knowledge

class QueryAllKnowledge(Resource):
    def get(self):
        k = Knowledge()
        data = Knowledge.query.all()

        if data:
            return data
        else:
            return {'message': 'Error!'}, 500