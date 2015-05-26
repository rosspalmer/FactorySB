import simpy
import pandas as pd

#|Store object simulates inventory store for various products
#|ands has an external access limit variable
class Store(object):

    #|Import enviroment, set limit of access points
    def __init__(self, env, limit):
        self.env = env
        self.r = simpy.Resource(self.env, limit)
        self.c = {}

    #|Add product container (type) to Store object
    def add_product(self, product_name, amount):
        self.c[product_name] = simpy.Container(self.env, init=amount)

#|Line object simulates a production line by running through
#|a product list by processing objects from
class Line(object):

    #|Import enviroment, product database, job list,
    #|input Store and output Store and create log DataFrame
    def __init__(self, env, prod, in_store, out_store):
        self.env = env
        self.prod = prod
        self.in_store = in_store
        self.out_store = out_store
        self.log = pd.DataFrame()

    #|Run Line process
    def run(self, job_list):

        #|Cycle through list of jobs
        for job in job_list:

            #|Transport items from input Store, run job on Line, and
            #|transport items to output Store
            start = self.env.now
            yield self.env.process(self.transport(job, self.in_store, 'from'))
            job_start = self.env.now
            yield self.env.timeout(self.prod[job]['job_time'])
            job_end = self.env.now
            yield self.env.process(self.transport(job, self.out_store, 'to'))
            end = self.env.now

            #|Calculate idle time for job and add to total, and
            #|create log entry and add to master log
            idle = (job_start-start) + (end-job_end)
            log = {'product':job,'start':start,'job_start':job_start,
                'job_end':job_end,'end':end,'idle':idle}
            self.log = self.log.append(log, ignore_index=True)

    #|Request use of Store and transport inventory 'to' or 'from' Store
    def transport(self, job, store, mode):
        with store.r.request() as req:
            yield req
            if mode == 'to':
                yield store.c[job].put(self.prod[job]['job_amount'])
            yield self.env.timeout(self.prod[job]['transport'])
            if mode =='from':
                yield store.c[job].get(self.prod[job]['job_amount'])