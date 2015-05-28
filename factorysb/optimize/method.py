import tools

import pandas as pd

def brute_random(factory, attempts):
    log = pd.DataFrame()
    for i in range(attempts):
        factory.job_list = tools.random_job_list(factory, 50)
        factory.run('out')
        print factory.ord
        log = log.append(tools.cost(factory),ignore_index=True).sort('total')
        factory.ord['complete'] = 0
        for product_name in factory.prod:
            factory.stores['in'].c[product_name].put(50000)
        print factory.ord
    print log