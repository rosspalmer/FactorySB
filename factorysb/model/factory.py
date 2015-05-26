import components as cp

import simpy
import pandas as pd

class Factory(object):

    def __init__(self):
        self.env = simpy.Environment()
        self.prod = {}
        self.ord = pd.DataFrame()
        self.stores = {}
        self.lines = {}
        self.job_list = {}
        self.log = pd.DataFrame()

    def create_product(self, name, job_amount, job_time, transport):
        prod = {'job_amount':job_amount,
                    'job_time':job_time,'transport':transport}
        self.prod[name] = prod

    def create_order(self, product_name, amount, time, late_fee):
        order = {'product_name':product_name, 'amount':amount,'time':time,
            'late_fee':late_fee, 'total_fee':0, 'complete':'no'}
        self.ord = self.ord.append(order, ignore_index=True).sort('time')

    def create_store(self, name, product_list, limit=1):
        store = cp.Store(self.env, limit)
        for product in product_list:
            store.add_product(product['name'],product['amount'])
        self.stores[name] = store

    def create_line(self, name, in_store, out_store):
        self.lines[name] = cp.Line(self.env, self.prod,
                self.stores[in_store], self.stores[out_store])

    def run(self, output_store):
        for line in self.lines:
            print line
            self.env.process(self.lines[line].run(self.job_list[line]))
        #self.env.process(self.fill_orders(output_store))
        self.env.run()
        for line in self.lines:
            log = self.lines[line].log
            log['line'] = line
            self.log = self.log.append(log,ignore_index=True).sort('start')

    def fill_orders(self, output_store):
        while 'no' in self.ord['complete'].unique():
            for name in self.ord['product_name'].unique():
                order = self.ord[self.ord['product_name'] == name \
                        and self.ord['complete'] == 'no'].iloc[0]
                if order <= self.stores[output_store].c.level:
                    yield self.stores[output_store].c.get(order['amount'])
                    if self.env.now > order['time']:
                        order['late_fine'] = order['late_fee']\
                            *int(self.env.now/order['time'])
                    else:
                        order['late_fine'] = 0
                    order['complete'] = 'yes'
                    self.ord = self.ord.drop(order.name)
                    self.ord = self.ord.append(order, ignore_index='True')
            yield self.env.timeout(15)