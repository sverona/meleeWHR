#!/bin/env/python
import json
import math
import matplotlib
matplotlib.use('GTK3Agg')

import matplotlib.pyplot as plt
from datetime import date, timedelta
from scipy.interpolate import CubicSpline

startdate = date(2003, 1, 1)


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


def top_players(ratings, week=795, K=0.005, threshold=25):
    tags = sorted(ratings.keys(), key=lambda p: rate(p, week=week, K=K), reverse=True)[:threshold]
    return [(t, rate(t)) for t in tags]


ratings = json.load(open('ratings_whr_2.json'))
tops = set()
for w in range(77, 795 + 1):
    tops.update(x[0] for x in top_players(ratings, week=w, threshold=10))
    # print(startdate + timedelta(days=7) * w, top_players(ratings, week=w, threshold=25))

# tops.update(['ppmd', 'mango', 'mew2king', 'armada', 'hungrybox', 'plup', 'leffen', 'amsah', 'ken', 'sfat', 'wizzrobe', 'n0ne', 's2j'])

cm = plt.get_cmap('gist_rainbow')
fig = plt.figure()
fig, ax = plt.subplots(1, 1)
fig.set_size_inches(11, 8.5)
ax.set_prop_cycle('color', [cm(1.0 * i / len(tops)) for i in range(len(tops))])
ax.grid(True)

for t in tops:
    entry_date = ratings[t][0][0]
    end_date = min(795, ratings[t][-1][0] + 10)
    weeks = [r[0] for r in ratings[t]]

    dates = [startdate + timedelta(days=7) * w for w in weeks]
    rates = [1500 + 0.75 * r[1] for r in ratings[t]]
    if len(rates) >= 2:
        cs = CubicSpline(weeks, rates)
        plt.plot(weeks, cs(weeks), label=t)

handles, labels = ax.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))

fig.legend(handles, labels, loc=2, bbox_to_anchor=(8, 1), ncol=1, mode='expand', borderaxespad=0.)
plt.savefig('plot.png')
