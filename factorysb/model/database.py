import pandas as pd
import random as rn
from sqlalchemy import create_engine
from pandas.io.sql import read_sql

class data(object):

    def __init__(self):
        self.eng = create_engine('sqlite:///fsb.db')
        self.db = {}
        self.db['lines'] = pd.DataFrame(columns=['name','recipe','rate'],
                        index=['name','recipe'])
        self.db['stores'] = pd.DataFrame(columns=['name','product','initial','limit'],
                        index=['name','product'])
        self.db['recipes'] = pd.DataFrame(columns=['name','product','amount','ratio',
                        'output'],index=['name','product'])
        self.db['conns'] = pd.DataFrame(columns=['input','output','product','rate',
                        'workers'],index=['input','output','product'])

    def load(self):
        for table in self.db.keys():
            self.db[table] = read_sql(table, self.eng)

    def update(self):
        for table in self.db.keys():
            self.db[table].to_sql(table, self.eng, if_exists='replace')

    def create_xl(self):
        writer = pd.ExcelWriter('fsb.xlsx')
        for table in self.db.keys():
            self.db[table].to_excel(writer, table)

d = data()
for i in range(10):
    row = {'name':rn.randint(1,4),'recipe':rn.randint(1,10),'rate':rn.randint(100,200)}
    d.db['lines'] = d.db['lines'].append(row, ignore_index='True')

print d.db['lines']

