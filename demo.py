import factorysb as fsb
import random as rn
import pandas as pd
import math

T = 20000
ATTEMPTS = 50
COOL = 0.98
LOG_INT = 15

cost_df = pd.DataFrame()
orders = pd.DataFrame()
log = pd.DataFrame()

#|Create random order list
for i in range(5):
    order = {'product_name':rn.choice(['A','B','C']), 'amount':rn.randint(100,300),
            'time':rn.randint(500,3000),'late_fee':rn.randint(4000,6000),
            'total_fee':0, 'complete':0}
    orders = orders.append(order, ignore_index=True)

print orders

i = 0

#|Loop while above "Tempature" limit
while T > 0.1:

    if i % LOG_INT == 0:
        print "System Temp: %s" % str(round(T,2))

    #|Create Factory object
    fac = fsb.Factory()

    #|Set Order List
    fac.ord = orders

    #|Create products and define job amount, job time, and transport time
    fac.create_product('A', 100, 200, 50)
    fac.create_product('B', 50, 250, 30)
    fac.create_product('C', 80, 300, 100)

    #|Create input and output inventories
    i_inv = [{'name':'A', 'amount':50000}]
    i_inv.append({'name':'B', 'amount':50000})
    i_inv.append({'name':'C', 'amount':50000})
    o_inv = [{'name':'A', 'amount':0}]
    o_inv.append({'name':'B', 'amount':0})
    o_inv.append({'name':'C', 'amount':0})

    #|Create input and output Stores
    fac.create_store('in', i_inv)
    fac.create_store('out', o_inv)

    #|Create Lines
    fac.create_line('line1', 'in', 'out')
    fac.create_line('line2', 'in', 'out')
    fac.create_line('line3', 'in', 'out')

    #|Create initial random job list if first run
    if T == 20000:
        fac = fsb.random_job_list(fac)
        prev_job = fac.job_list
    #|Switch jobs between random lines and positions
    else:
        fac.job_list = prev_job
        fac = fsb.random_job_list(fac, mode='switch')

    #|Run Factory simulation and calculate costs
    fac.run('out')
    cost = fsb.costs(fac)
    cost_df = cost_df.append(cost, ignore_index='True')

    #|Simulated annealing
    if len(cost_df.index) >= 2:
        if cost_df.iloc[-1]['total'] < cost_df.iloc[-2]['total']:
            prev_job = fac.job_list
        else:
            P = pow(math.e,(-cost_df.iloc[-1]['total']\
                    - cost_df.iloc[-2]['total'])/T)
            if rn.random() < P:
                prev_job = fac.job_list

    #|Reduce tempature
    T = T*COOL
    i += 1

print cost_df.sort('total')
print cost_df