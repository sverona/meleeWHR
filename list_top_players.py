#!/bin/env/python
import json
import math
import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt
from datetime import date, timedelta
from scipy.interpolate import CubicSpline
from cycler import cycler

startdate = date(2003, 1, 1)

ratings = json.load(open('ratings_whr_4.json'))


def wiener_rate(player, t, K=0.01):
    def nearest_ratings(series):
        prevs = [k for k, rate in enumerate(series) if rate[0] <= t]
        if prevs:
            last = max(prevs)
            last_rate = series[last]
            try:
                next_rate = series[last + 1]
            except IndexError:
                next_rate = None
            return last_rate, next_rate
        else:
            return None, None

    last_rate, next_rate = nearest_ratings(ratings[player])
    if last_rate and next_rate:
        t1, mu1, var1 = last_rate
        t2, mu2, var2 = next_rate
        return (mu1 * (t2 - t) + mu2 * (t - t1)) / (t2 - t1)  # - 3 * (var1 * var2)**0.25
    elif last_rate:
        t1, mu1, var1 = last_rate
        return mu1 * math.exp(K * (t1 - t))  # - 3 * var1**0.5
    else:
        return 0


def rate(player, week=795, K=0.00075):
    def last_rating(series):
        trunc = [s for s in series if s[0] <= week]
        if trunc:
            return trunc[-1]

    last = last_rating(ratings[player])
    if last:
        # rating = last[1] * math.exp(K * (last[0] - week))
        return last[1]
    else:
        return 0


def top_players(ratings, week=795, K=0.01, threshold=25):
    tags = sorted(ratings.keys(), key=lambda p: wiener_rate(p, t=week, K=K), reverse=True)[:threshold]
    return [(t, wiener_rate(t, t=week, K=K)) for t in tags]


def plot_top_players(ratings):
    tops = set()
    for w in range(77, 795 + 1):
        tops.update(x[0] for x in top_players(ratings, week=w, threshold=10))
        # print(startdate + timedelta(days=7) * w, top_players(ratings, week=w, threshold=25))

    # tops.update(['ppmd', 'mango', 'mew2king', 'armada', 'hungrybox', 'plup', 'leffen', 'amsah', 'ken', 'sfat', 'wizzrobe', 'n0ne', 's2j'])

    tops = list(sorted(tops, key=lambda p: wiener_rate(p, 795)))

    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(16.5, 12.25) 
    ax.set_prop_cycle(cycler('linestyle', [':', '--', "-"]) *
                      cycler('color', list('rbgckm') + ['xkcd:burgundy', 'xkcd:lavender', 'xkcd:gold']))

    ax.set_yticks(range(1800, 2800, 100))
    ax.set_yticks(range(1800, 2800, 25), minor=True)
    ax.grid(which='both')

    for t in tops:
        entry_date = ratings[t][0][0]
        end_date = min(795, ratings[t][-1][0] + 10)
        weeks = range(entry_date, end_date + 1)
        # weeks = [r[0] for r in ratings[t]]

        dates = [startdate + timedelta(days=7) * w for w in weeks]
        # rates = [1800 + 0.5 * r[1] for r in ratings[t]]
        rates = [1800 + 0.5 * wiener_rate(t, w) for w in weeks]
        if len(rates) >= 2:
            # cs = CubicSpline(weeks, rates)
            # plt.plot(dates, cs(weeks), label=t)
            for z in zip(dates, rates):
                print(z)
            plt.plot(dates, rates, label=t)

    handles, labels = ax.get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: wiener_rate(t[0], 795), reverse=True))

    lgd = ax.legend(handles, labels, ncol=1, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('plot.png', bbox_extra_artists=(lgd,), bbox_inches='tight')


def __main__():
    for p, r in top_players(ratings, week=52 * (2004 - 2003 + 1), K=0.00075, threshold=10):
        print(p, r, sep='\t')



if __name__ == "__main__":
    __main__()
