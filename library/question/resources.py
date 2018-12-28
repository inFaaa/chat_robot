from flask_restful import reqparse, Resource
from flask import request

from library.question.models import Question

"""
PUT to add a new question
Request body:: { "q_title": "", "q_type": "", "q_option": "", "q_answer": "", "q_scope": "" }
---
POST to query some questions with arguments
Request body: { "keyword": "", "q_type": "", "q_scope": "" }
Response body: { "1": { "q_title": "", "q_type": "", "q_option": "", "q_answer": "" }, "2", {"q_title": "", "q_type": "", "q_option": "", "q_answer": "" }}
"""
class QuestionResolver(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('q_id', required=False)
    parser.add_argument('q_title', required=False)
    parser.add_argument('q_type', required=False)
    parser.add_argument('q_option', required=False)
    parser.add_argument('q_answer', required=False)
    parser.add_argument('keyword', required=False)
    parser.add_argument('q_type', required=False)
    parser.add_argument('q_scope', required=False)
    def put(self):
        q = Question()
        args = self.parser.parse_args()
        try:
            q.save(args)
            return {"message": "Save a new question."}
        except:
            return {"message": "Error: Failed to save a new question."}, 500
    
    def get(self):
        args = self.parser.parse_args()
        if args['q_id']:
            res = Question.query.filter_by(q_id=args['q_id']).first()
            return res.to_json()
        else:
            return {'message': 'Error on get!'}, 500

    def post(self):
        args = self.parser.parse_args()
        data = []
        # 1. select questions by type
        if args['q_type']:
            res = Question.query.filter_by(q_type=args['q_type']).all()
        else:
            res = Question.query.filter(Question.q_title != None).all()
            
        for x in res:
            data.append(x.to_json())    
        # 2. select question by keyword
        if args['keyword']:
            # print(args['keyword'])
            # 使用列表推导来生成 title 中包含 keyword 的问题列表
            data = [ q for q in data if q['q_title'].find(args['keyword']) != -1]

        # TODO: 3. select question by scope
        # if args['scope']:
        
        if data:
            return data
        else:
            return {'message': 'Error on post!'}, 500

    