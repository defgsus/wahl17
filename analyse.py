import json

import numpy as np
from scipy import ndimage
from matplotlib import pyplot as plt

from sklearn import manifold
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA


ROOT = "/home/defgsus/prog/DATA/wahl17/welt.de/"

def _convert(dic, Type, keys):
    for key in keys:
        try:
            dic[key] = Type(dic[key])
        except ValueError:
            dic[key] = Type(0)

def load_wks():
    wks = dict()
    for i in range(1, 917):
        try:
            with open(ROOT + "wk/wk%s.json" % i, "r") as f:
                wk = json.load(f)
                wk = wk["results"][0]

                _convert(wk, float, ('percentTurnout', 'percentTurnoutPre', 'percentTurnoutDiff'))
                _convert(wk, int, ('absolute1', 'absolute2', 'absoluteVoters', 'absoluteEntitled', 'countedTotal', 'type', 'wkid'))
                for res in wk["results"]:
                    _convert(res, float, ('percent1', 'percent2', 'percent2Pre', 'percent2Diff'))
                    _convert(res, int, ('absolute1', 'absolute2', 'seats'))

                wks[wk["wkid"]] = wk
        except FileNotFoundError:
            pass
    return wks


def print1():
    wks = load_wks()
    for wk in sorted(wks):
        wk = wks[wk]
        print("--- %s" % wk["wkid"])
        print(wk["winnerName"])
        print(wk["type"])
        print(wk["winnerparty_id"])
        print("  ".join(
            "%s %s" % (r["partyname"], r["percent1"]) for r in sorted(wk["results"], key=lambda r: -r["percent1"])))


def get_party_grid(value_key="percent1"):
    wks = load_wks()
    party_set = set()
    for wk in wks.values():
        for r in wk["results"]:
            party_set.add(r["partyname"])
    party_set = sorted(party_set)
    grid = dict()
    for wk in wks.values():
        values = [0.] * len(party_set)
        for r in wk["results"]:
            values[party_set.index(r["partyname"])] = r[value_key]
        grid[wk["wkid"]] = values
    return grid, party_set

if 0:
    grid = get_party_grid()
    for key in grid:
        print("%4s %s" % (key, grid[key]))

def plot_clustering(X, WIN, LABELS, title=None):
    x_min, x_max = np.min(X, axis=0), np.max(X, axis=0)
    X = (X - x_min) / max(x_max - x_min)
    #X /= [42., 1.]

    plt.figure(figsize=(6, 4))
    for i in range(X.shape[0]):
        plt.scatter(X[i, 0], X[i, 1], s=8, alpha=0.7, color=plt.cm.spectral(WIN[i]/10.))
        plt.text(X[i, 0], X[i, 1], str(LABELS[i]), fontdict={'size': 6})

    #plt.xticks([])
    #plt.yticks([])
    if title is not None:
        plt.title(title, size=17)
    plt.axis('off')
    plt.tight_layout()

def plot_wk_cluster():
    grid, party_names = get_party_grid("percent1")
    X = np.array([g for g in grid.values()], dtype="float32")
    WIN, LABELS = [], []
    for row in X:
        k, maxx = 0, row[0]
        for i, x in enumerate(row):
            if x > maxx:
                k, maxx = i, x
        WIN.append(k)
        LABELS.append(party_names[k])
    #grid = grid[:50]
    pca = PCA(n_components=2, svd_solver='full')
    X = pca.fit(X).transform(X)
    #print(X)
    #print(pca.explained_variance_)
    clustering = AgglomerativeClustering(linkage='complete', n_clusters=len(X[0]))
    #X = clustering.fit(X)
    #print(clustering.children_)
    plot_clustering(X, WIN, LABELS)
    plt.show()

plot_wk_cluster()


R = {'results': [
        {
            'percentTurnoutPre': '68.2',
            'absoluteEntitled': '1765814',
            'winnerName': '',
            'counted': '',
            'absolute2': '1312056',
            'percentCounted': '',
            'percentTurnoutDiff': '6.1',
            'sourceResults': 'sourceFinal',
            'sourceString': '',
            'absoluteVoters': '',
            'statusDate': '2017-09-25 04:32:06',
            'absolute1': '1312056',
            'type': '6',
            'percentTurnout': '74.3',
            'wkid': '916',
            'countedTotal': '',
            'winnerparty_id': '',
            'results': [
                {
                    'id': 'p200',
                    'partyname': 'CDU',
                    'percent2': '28.8',
                    'absolute2': '372216',
                    'seats': '',
                    'absolute1': '',
                    'percent1': '31.6',
                    'percent2Pre': '38.8',
                    'percent2Diff': '-10'
                },
                {'id': 'p644', 'partyname': 'AfD', 'percent2': '22.7', 'absolute2': '294045', 'seats': '', 'absolute1': '',
                 'percent1': '22.5', 'percent2Pre': '6.2', 'percent2Diff': '16.5'},
                {'id': 'p500', 'partyname': 'Linke', 'percent2': '16.9', 'absolute2': '218183', 'seats': '', 'absolute1': '',
                 'percent1': '17.6', 'percent2Pre': '23.4', 'percent2Diff': '-6.5'},
                {'id': 'p100', 'partyname': 'SPD', 'percent2': '13.2', 'absolute2': '171011', 'seats': '', 'absolute1': '',
                 'percent1': '14.6', 'percent2Pre': '16.1', 'percent2Diff': '-2.9'},
                {'id': 'p400', 'partyname': 'FDP', 'percent2': '7.8', 'absolute2': '101114', 'seats': '', 'absolute1': '',
                 'percent1': '5.5', 'percent2Pre': '2.6', 'percent2Diff': '5.2'},
                {'id': 'p300', 'partyname': 'Grüne', 'percent2': '4.1', 'absolute2': '53338', 'seats': '', 'absolute1': '',
                 'percent1': '3.6', 'percent2Pre': '4.9', 'percent2Diff': '-0.8'},
                {'id': 'p608', 'partyname': 'Freie Wähler', 'percent2': '1.6', 'absolute2': '21091', 'seats': '',
                 'absolute1': '', 'percent1': '', 'percent2Pre': '1.4', 'percent2Diff': '0.2'},
                {'id': 'p735', 'partyname': 'Die Partei', 'percent2': '1.5', 'absolute2': '19094', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '', 'percent2Diff': ''},
                {'id': 'p910', 'partyname': 'NPD', 'percent2': '1.2', 'absolute2': '16091', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '3.2', 'percent2Diff': '-2'},
                {'id': 'p611', 'partyname': 'ÖDP', 'percent2': '0.5', 'absolute2': '6402', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '0.6', 'percent2Diff': '-0.1'},
                {'id': 'p609', 'partyname': 'Piraten', 'percent2': '0.5', 'absolute2': '6080', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '2.4', 'percent2Diff': '-1.9'},
                {'id': 'p661', 'partyname': 'BGE', 'percent2': '0.4', 'absolute2': '5302', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '', 'percent2Diff': ''},
                {'id': 'p786', 'partyname': 'DM', 'percent2': '0.4', 'absolute2': '4947', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '', 'percent2Diff': ''},
                {'id': 'p670', 'partyname': 'V-Partei', 'percent2': '0.3', 'absolute2': '3468', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '', 'percent2Diff': ''},
                {'id': 'p637', 'partyname': 'MLPD', 'percent2': '0.1', 'absolute2': '1907', 'seats': '', 'absolute1': '',
                 'percent1': '', 'percent2Pre': '0.1', 'percent2Diff': '0'}
            ]
        }
    ]
}
