import pandas as pd
from sqlalchemy import create_engine
from pandas.io.sql import read_sql

class data(object):

    def __init__(self):
        self.lines = pd.DataFrames(columns=['name','recipe','rate'],
                        index=['name','recipe'])
        self.store = pd.DataFrame(columns=['name','product','initial','limit'],
                        index=['name','product'])
        self.recipes = pd.DataFrame(columns=['name','product','amount','ratio',
                        'output'],index=['name','product'])
        self.conns = pd.DataFrame(columns=['name','output','product','rate',
                        'workers'],index=['input','output','product'])

class sql(object):

    def __init__(self):
        self.eng = self.engine()
        self.db = {}

    def engine(self):
        eng = create_engine('sqlite:///fsb.db')
        return eng

    def load(self):
        db = {}
        tables = ['lines','stores','recipes','connections']
        for table in tables:
            db[table] = read_sql(tables, self.eng)
        return db

    def create(self):
        self.lines = pd.DataFrames(columns=['name','recipe','rate'],
                        index=['name','recipe'])
        self.store = pd.DataFrame(columns=['name','product','initial','limit'],
                        index=['name','product'])
        self.recipes = pd.DataFrame(columns=['name','product','amount','ratio',
                        'output'],index=['name','product'])
        self.conns = pd.DataFrame(columns=['name','output','product','rate',
                        'workers'],index=['input','output','product'])
