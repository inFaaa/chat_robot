from flask_restful import reqparse, Resource
from flask import request

from library.question.models import Question
import json

"""
PUT to add a new question
Request body:: { "question": { "q_title": "", "q_type": "", "q_option": "", "q_answer": "" }}
---
POST to query some questions with arguments
Request body: { "keyword": "", "q_type": "", "q_scope": "" }
Response body: { "1": { "q_title": "", "q_type": "", "q_option": "", "q_answer": "" }, "2", {"q_title": "", "q_type": "", "q_option": "", "q_answer": "" }}
"""
class QuestionResolver(Resource):
    def put(self):
        q = Question()
        parser = reqparse.RequestParser()
        parser.add_argument('question')
        args = parser.parse_args()
        try:
            q.save(args)
            return {"message": "Save a new question."}
        except:
            return {"message": "Error: Failed to save a new question."}, 500
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', required=False)
        parser.add_argument('q_type', required=False)
        parser.add_argument('q_scope', required=False)
        args = parser.parse_args()
        data = []
        # 1. select questions by type
        if args['q_type']:
            res = Question.query.filter_by(q_type=args['q_type']).all()
            for x in res:
                data.append(x.to_json())
                
        # 2. select question by keyword
        if args['keyword']:
            # print(args['keyword'])
            # 使用列表推导来生成 title 中包含 keyword 的问题列表
            data = [ q for q in data if q['q_title'].find(args['keyword']) != -1]

        # TODO: 3. select question by keyword
        # if args['scope']:
            
        if data:
            return data
        else:
            return {'message': 'Error!'}, 500