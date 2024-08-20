import random
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict


def nums_till(n, thresh):
    seq = list(range(1, n+1))
    
    res = defaultdict(int)
    num_loops = 0
    for x in list(range(1, 1000)):
        num_loops = x
        r = random.choice(seq)
        res[r] += 1
        if sum([v for v in res.values() if v > 1]) >= thresh:
            break
    return num_loops

def run_sim(runs: int=5000, n: int=365,
            thresh: int=1):
    results = []
        
    for x in list(range(1, runs)):
        results.append(nums_till(n, thresh))
    
    plotting = pd.DataFrame(results, columns=['result_counts'])
    vc = pd.DataFrame(plotting.value_counts(normalize=True))
    vc.reset_index(inplace=True)
    vc.set_index('result_counts', inplace=True)
    new_index = list(range(1, max(vc.index)))
    vc = vc.reindex(new_index, fill_value=0)
    vc.reset_index(inplace=True)
    vc.columns = ['result_counts', 'prob']
    vc['cdf'] = vc.prob.cumsum()

    above_50 = vc[vc.cdf >=.5]
    idx_above = min(above_50.result_counts)
    
    return vc, idx_above

def plot_results(vc, halfway_point, pool_size: int=23):
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.bar(vc.result_counts, vc.prob)
    ax.plot(vc.result_counts, vc.cdf)
    cum_prob = vc[vc.result_counts == halfway_point].cdf.values[0]
    ax.axhline(cum_prob, xmax= float(halfway_point / max(vc.result_counts)), c='r')
    ax.axvline(halfway_point, ymax=cum_prob, c='r')
    cum_prob_pool = vc[vc.result_counts == pool_size].cdf.values[0]

    ax.set_title(f'Number of People Until >50% Likely: {halfway_point}\nCumulative Prob of Pool Size {pool_size}: {cum_prob_pool:.2%}')

if __name__ == '__main__':
    vc, idx_above = run_sim()
    plot_results(vc, idx_above)
    
    vc, idx_above = run_sim(n=30, thresh=9)
    plot_results(vc, idx_above, pool_size=15)
