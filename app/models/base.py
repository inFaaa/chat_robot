from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from contextlib import contextmanager
from sqlalchemy import SmallInteger, Column, Integer
from datetime import datetime

class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class = Query)

class Base(db.Model):
    __abstract__ = True
    status = Column(SmallInteger,default=1)
    create_time = Column(Integer)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def delete(self):
        self.status = 0

    def set_attr(self,**attr_dict):
        for key,value in attr_dict.items():
                                    # not ==  ???
            if hasattr(self,key) and key != 'id':
                setattr(self, key, value)

    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None