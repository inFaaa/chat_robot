from library import db

class Question(db.Model):
    __tablename__ = "question"

    q_id = db.Column(db.Integer, primary_key=True, nullable=True)
    q_title = db.Column(db.String(200), nullable=True)
    q_type = db.Column(db.String(20))
    q_option = db.Column(db.String(200))
    q_answer = db.Column(db.String(500))
    q_scope = db.Column(db.String(100))
    clicks = db.Column(db.Integer, default=0, nullable=True)

    def save(self, args):
        self.q_title = args['q_title']
        self.q_type = args['q_type']
        self.q_option = args['q_option']
        self.q_answer = args['q_answer']
        self.q_scope = args['q_scope']

        db.session.add(self)
        db.session.commit()
    

    def to_json(self):
        return {
            'q_id': self.q_id,
            'q_title': self.q_title,
            'q_type': self.q_type,
            'q_option': self.q_option,
            'q_answer': self.q_answer,
            'q_scope': self.q_scope,
            'clicks': self.clicks
        }