from flask_restful import reqparse, Resource
from flask import request

from library.knowledge.models import Knowledge
from util import get_entity, get_target_sentenses_index

"""
PUT to add a new knowledge
Request body: { "k_title": "", ... }
---
GET to get knowledges by keyword
Response body: [ { "k_id": 17, ... }, { "k_id": 43, ... } ]
---
POST to test chatbot
"""
class KnowledgeResolver(Resource):
    def put(self):
        k = Knowledge()
        parser = reqparse.RequestParser()
        parser.add_argument('k_title')
        parser.add_argument('k_detail')
        parser.add_argument('k_entity')
        parser.add_argument('k_scope')
        args = parser.parse_args()
        try:
            k.save(args)
            return {"message": "Save a new knowledge."}
        except:
            return {"message": "Error: Failed to save a new knowledge."}, 500

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

    def post(self):
        # 测试chatbot
        from util import get_entity, get_target_sentenses_index
        parser = reqparse.RequestParser()
        parser.add_argument('question', required=True)
        args = parser.parse_args()

        all_results = Knowledge.query.all()
        indexs_weight_pair = get_target_sentenses_index(args['question'], [i.k_title for i in all_results])
        data = []
        if indexs_weight_pair:
            for i in range(len(indexs_weight_pair)):
                data.append(all_results[indexs_weight_pair[i][0]].to_json())
        else:
            return "没听懂，可以再说清楚一点吗？"
        # print(answers)
        answer = "你想问的是不是：" + data[0]['k_title'] + "\n---\n" + data[0]['k_detail']
        return answer
