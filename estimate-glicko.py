from glicko2 import Glicko2
from glob import glob
from datetime import date, timedelta
import json

env = Glicko2(mu=1500, phi=350)

ratings = dict()
tourneys = json.load(open('all_tournaments.json'))


def tourney_time(t):
    return date.fromtimestamp(int(t['printouts']['Has start date'][0]['timestamp']))


players = dict()
series = []
sorted_tourneys = sorted(tourneys.keys(), key=lambda name: tourney_time(tourneys[name]))
for t in sorted_tourneys:
    tourn = tourneys[t]
    week_no = 1 + (tourney_time(tourn) - date(2003, 1, 1)) // timedelta(days=7)
    print(t, week_no)

    files = glob('./brackets/{0}/*.json'.format(tourn['fulltext']))
    for filename in files:
        if not any(x in filename for x in ("Doubles", "Pools", "Crew", "Games")):
            print(filename)

            bracket = json.load(open(filename))
            for name, brak in bracket.items():
                for round, game in brak.items():
                    print(name, round)
                    if 'p1' in game and 'p2' in game and 'Bye' not in (game['p1'], game['p2']) and game['p1'] != game['p2']:
                        p1 = p2 = 0
                        try:
                            p1 = int(game['p1score'])
                        except KeyError:
                            if game['win'] == '1':
                                p1 = 2
                        except ValueError:
                            if game['p1score'] in ['W', 'advance', 'win'] and game['p2score'] != 'DQ':
                                p1 = 2
                        finally:
                            for _ in range(p1):
                                series.append()


"""
for t, month_matches in data.groupby(by='Month'):
    players = set(month_matches['White']) | set(month_matches['Black'])
    month_updates = dict()
    for p in players:
        games = data[(data['Month'] == t) & ((data['White'] == p) | (data['Black'] == p))]
        try:
            rating = ratings[p]
        except KeyError:
            rating = env.create_rating()

        series = []
        for game in games.itertuples():
            if game.White == p:
                if game.Black in ratings.keys():
                    other_rating = ratings[game.Black]
                else:
                    other_rating = env.create_rating()
                series.append((game.Score, other_rating))
            elif game.Black == p:
                if game.White in ratings.keys():
                    other_rating = ratings[game.White]
                else:
                    other_rating = env.create_rating()
                series.append((1 - game.Score, other_rating))

        ratings[p] = env.rate(rating, series)
        # print(t, p, ratings[p].mu, ratings[p].phi, sep="\t")
    print(t, sum(sorted([x.mu for x in ratings.values()], reverse=True)[:100])/100, flush=True)
"""
