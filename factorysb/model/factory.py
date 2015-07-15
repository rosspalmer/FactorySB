import database
import components as cp

import simpy
import pandas as pd

class Factory(object):

    def __init__(self):
        self.env = simpy.Environment()
        self.db = database.data()
        self.db.load_sql()
        self.lines = {}
        self.stores = {}
        self.log = pd.DataFrame()

    def build(self):

        for line_name in self.db.db['lines']['name'].unique():
            self.lines[line_name] = cp.Line(self.env, self.db)

        for store_name in self.db.db['stores']['name'].unique():
            self.lines[store_name] = cp.Store(self.env, self.db)



###############################################3

    def run(self, output_store):
        for line in self.lines:
            self.env.process(self.lines[line].run(self.job_list[line]))
        self.env.process(self.fill_orders(output_store))
        self.env.run()
        for line in self.lines:
            log = self.lines[line].log
            log['line'] = line
            self.log = self.log.append(log,ignore_index=True).sort('start')

    def fill_orders(self, output_store):
        while len(self.ord[self.ord['complete'] == 0].index) > 0:
            for name in self.ord[self.ord['complete'] == 0]\
                        ['product_name'].unique():
                order = self.ord[self.ord['product_name'] == name]
                order = order[order['complete'] == 0].iloc[0]
                if order['amount'] <= self.stores[output_store].c[name].level:
                    yield self.stores[output_store].c[name].get(order['amount'])
                    if self.env.now > order['time']:
                        order['total_fee'] = order['late_fee']\
                            *int(self.env.now/order['time'])
                    else:
                        order['total_fee'] = 0
                    order['complete'] = self.env.now
                    self.ord = self.ord.drop(order.name)
                    self.ord = self.ord.append(order)
            yield self.env.timeout(15)

f = Factory()
f.build()