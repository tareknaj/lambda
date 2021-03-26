import json
import logging
import os
import sqlalchemy
from sqlalchemy import Column,String,Boolean,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta,declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(String(45), primary_key=True)
    firstName = Column(String(45))
    lastName = Column(String(45))
    email = Column(String(45))
    comments = Column(String(45))
    options = Column(String(45))
    checked = Column(Boolean)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
pwd = os.getenv('DB_PWD')
db_name = os.getenv('DB_NAME')

connect_url = sqlalchemy.engine.url.URL(
    'mysql+pymysql',
    username=user,
    password=pwd,
    host=host,
    port=3306,
    database=db_name)

engine = sqlalchemy.create_engine(connect_url, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_session():
    """ Returns a new session from the db engine which can be used by the data access objects """
    return Session()


def get_engine():
    """ Returns the engine of the db connection """
    return engine


class AlchemyEncoder(json.JSONEncoder):
    """ Based on: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json/41204271 """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) 
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)