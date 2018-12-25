from flask_restful import Resource
from flask import request

from library.knowledge.models import Knowledge
from util import get_entity, get_target_sentenses_index
   
class QueryAllKnowledge(Resource):
    def get(self):
        k = Knowledge()
        data = Knowledge.query.all()

        if data:
            return data
        else:
            return {'message': 'Error!'}, 500

class QueryKnowledge(Resource):
    def post(self):
        data = request.form['data']
        # 数据库中以空格划分
        all_results = Knowledge.query.all() 
        # print(all_results)
        # 这里还要针对查询进行改进
        indexs_weight_pair = get_target_sentenses_index(data,[i.k_title for i in all_results])
        # print(indexs_weight_pair)
        answers = []
        for i in range(len(indexs_weight_pair)):
            answers.append(all_results[indexs_weight_pair[i][0]].k_detail)
        print(answers)# 用于测试

        if answers:
            return answers[0]
        else:
            return {'message': 'Error!'}, 500