from sqlalchemy import Column,String,Integer

from app.models.base import db,Base


class QueryPair(Base):
    __tablename__='querypair'
    id = Column(Integer, primary_key=True)
    query_string = Column(String(100),nullable=False)
    answer = Column(String(100),nullable=False)

    def get_answer_by_query(self,query):
        answer = QueryPair.query.filter_by(query_string=query).first()
        return answer

