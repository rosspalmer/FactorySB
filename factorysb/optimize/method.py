import tools

import pandas as pd

def brute_random(factory, attempts):
    log = pd.DataFrame()
    for i in range(attempts):
        factory.job_list = tools.random_job_list(factory, 50)
        factory.run('out')
        print 'ran'
        log = log.append(tools.cost(factory),ignore_index=True).sort('total')
    print log