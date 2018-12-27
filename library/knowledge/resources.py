from flask_restful import reqparse, Resource
from flask import request

from library.knowledge.models import Knowledge
from util import get_entity, get_target_sentenses_index

"""
PUT to add a new knowledge
Request body: { "knowledge": { "q_title": "", "q_type": "", "q_option": "", "q_answer": "" }}
---
GET to get knowledges by keyword
Response body: [ { "k_id": 17, ... }, { "k_id": 43, ... } ]
---
TODO: POST to query Knowledges with arguments
Request body: {}
Response body: []
"""
class KnowledgeResolver(Resource):
    def put(self):
        k = Knowledge()
        parser = reqparse.RequestParser()
        parser.add_argument('knowledge')
        args = parser.parse_args()
        try:
            k.save(args)
            return {"message": "Save a new knowledge."}
        except:
            return {"message": "Error: Failed to sace a new knowledge."}, 500

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', location='args', required=True)
        args = parser.parse_args()

        res = Knowledge.query.all() 
        data = []
        
        for x in res:
            data.append(x.to_json())

        if args['keyword']:
            print(args['keyword'])
            # 使用列表推导来生成 title 中包含 keyword 的知识点列表
            data = [ k for k in data if k['k_title'].find(args['keyword']) != -1]

        if data:
            return data
        else:
            return {'message': 'Error!'}, 500