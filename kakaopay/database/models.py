
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from .sqlite_database import SqliteDataBase


class Account(SqliteDataBase.db_entity):
    __tablename__ = 'Account'
    id = Column(Integer, primary_key=True)
    account_id = Column(String)
    account_pwd = Column(String)
    valid_token_time = Column(DateTime, default=datetime.utcnow)

    def __init__(self, account_id, account_pwd):
        self.account_id = account_id
        self.account_pwd = account_pwd


class Institute(SqliteDataBase.db_entity):
    __tablename__ = 'institute'
    id = Column(Integer, primary_key=True)
    institute_name = Column(String)
    institute_code = Column(String)

    def __init__(self, name, code):
        self.name = name
        self.institute_name = name
        self.institute_code = code


class Bank(SqliteDataBase.db_entity):
    __tablename__ = 'bank'
    id = Column(Integer, primary_key=True)
    institute_code = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    value = Column(Integer)

    def __init__(self, code, year, month, value):
        self.institute_code = code
        self.year = year
        self.month = month
        self.value = value
