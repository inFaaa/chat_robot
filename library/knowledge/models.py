from library import db

class Knowledge(db.Model):
    __tablename__ = 'knowledge'

    k_id = db.Column(db.Integer, primary_key=True, nullable=True)
    k_title = db.Column(db.String(100), nullable=True)
    k_detail = db.Column(db.String(200))
    k_entity = db.Column(db.String(100))
    k_scope = db.Column(db.String(100))
    clicks = db.Column(db.Integer, default=0, nullable=True)

    def save(self, args):
        self.k_title = args['k_title']
        self.k_detail = args['k_detail']
        self.k_entity = args['k_entity']
        self.k_scope = args['k_scope']

        db.session.add(self)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    def click(self):
        self.clicks = self.clicks + 1
        db.session.commit()
        
    def to_json(self):
        return {
            'k_id': self.k_id,
            'k_title': self.k_title,
            'k_detail': self.k_detail,
            'k_entity': self.k_entity,
            'k_scope': self.k_scope,
            'clicks' : self.clicks
        }