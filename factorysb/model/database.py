import pandas as pd
import random as rn
from sqlalchemy import create_engine
from pandas.io.sql import read_sql

class data(object):

    def __init__(self):
        self.eng = create_engine('sqlite:///fsb.db')
        self.db = {}

    def load_sql(self):
        for table_name in ['lines','stores','recipes','conns']:
            try:
                self.db[table_name] = read_sql(table_name, self.eng)
            except:
                pass

    def update_sql(self):
        for table in self.db.keys():
            self.db[table].to_sql(table, self.eng, if_exists='replace')

    def create_csv(self, table_name):
        if table_name in self.db:
            self.db[table_name].to_csv('%s.csv' % table_name)
        else:
            if table_name == 'lines':
                pd.DataFrame(columns=['name','recipe','rate']).to_csv('lines.csv', index=False)
            elif table_name == 'stores':
                pd.DataFrame(columns=['name','product','initial','limit']).to_csv('stores.csv', index=False)
            elif table_name == 'recipes':
                pd.DataFrame(columns=['name','product','in_out','amount']).to_csv('recipes.csv', index=False)
            elif table_name == 'conns':
                pd.DataFrame(columns=['input','output','product','trans_time']).to_csv('conns.csv', index=False)
            elif table_name == 'orders':
                pd.DataFrame(columns=['name','product','amount','due']).to_csv('conns.csv', index=False)
            elif table_name == 'schedule':
                pd.DataFrame(columns=['line','recipe','amount','instore','outstore']).to_csv('schedule.csv', index=False)

    def load_csv(self, table_name):
        self.db[table_name] = pd.read_csv('%s.csv' % table_name)

d = data()
d.create_csv('stores')