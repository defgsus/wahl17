from sklearn.decomposition import PCA
import numpy as np

from data import load_wahlkreise
from plothelper import render_template, get_scatter_plot_markup, test_plot

PARTY_COLORS = {
    "AfD": "#44f",
    "CDU": "#111",
    "CSU": "#111",
    "FDP": "#ff8",
    "Grüne": "#5f5",
    "Linke": "#0af",
    "NPD": "#f80",
    "SPD": "#f44",
}

def get_party_color(name):
    return PARTY_COLORS.get(name, "#888")


def calc_party_embedding(wks, value_key="percent1"):
    party_set = set()
    for wk in wks.values():
        for r in wk["results"]:
            party_set.add((r["id"], r["partyname"]))
    party_set = sorted(party_set, key=lambda t: t[1])
    party_idx = {t[0]: i for i, t in enumerate(party_set)}
    for wk in wks.values():
        embedding = [0.] * len(party_set)
        for r in wk["results"]:
            embedding[party_idx[r["id"]]] = r[value_key]
        wk["embedding"] = embedding
    return party_set

def _signed(x):
    return "+%s" % x if x > 0 else "%s" % x

#areas = load_area_data()
#print(areas["states"][0])

wks = load_wahlkreise()
party_names = calc_party_embedding(wks, "percent2")
print(wks[1])
print(party_names)

if 1:
    #party_names = get_party_grid("percent1")
    #X = np.array([g for g in wks.values()], dtype="float32")
    EMB, LABELS, COLORS, WKNAME = [], [], [], []
    for wk in wks.values():
        EMB.append(wk["embedding"])
        results = sorted(((r["partyname"], r["percent2"], _signed(r["percent2Diff"])) for r in wk["results"]),
                         key=lambda t: -t[1])
        LABELS.append(", ".join("%s %s (%s)" % r for r in results if r[1] >= 5.))
        WKNAME.append("%s %s" % (wk["wkid"], wk.get("name", "-")))
        COLORS.append(get_party_color(results[0][0]))

    pca = PCA(n_components=2, svd_solver='full')
    X = pca.fit(EMB).transform(EMB)

    markup = get_scatter_plot_markup(
        {
            "x": [x[0] for x in X],
            "y": [x[1] for x in X],
            "color": COLORS,
            "Partei": LABELS,
            "Wahlkreis": WKNAME,
        },
        width=600, height=600
    )
    render_template("./website/index.template", "./index.html", {
        "plot": markup,
    })


BTW_FEED = {"wahlkreisname": "Flensburg – Schleswig",
            "bundesland": "Schleswig-Holstein",
            "result": {"cdu": {"value": 34.2, "value_old": 38.2, "diff": -4, "votes": 58307},
                       "spd": {"value": 23.7, "value_old": 32.6, "diff": -8.9, "votes": 40376},
                       "afd": {"value": 6.8, "value_old": 4.1, "diff": 2.7, "votes": 11647},
                       "fdp": {"value": 11.1, "value_old": 5, "diff": 6.1, "votes": 18948},
                       "linke": {"value": 8.2, "value_old": 5.7, "diff": 2.5, "votes": 13995},
                       "gruene": {"value": 13.1, "value_old": 9.8, "diff": 3.3, "votes": 22290},
                       "wahlbeteiligung": {"value": 76.2, "value_old": 71.7, "diff": 4.5},
                       "sonstige": {"value": 2.8}
                       },
            "other": {"ohnemigration": {"value": 90},
                      "mitmigration": {"value": 10},
                      "eigentum": {"value": 49.4},
                      "einkommen": {"value": 20265},
                      "arbeitslose": {"value": 7.2},
                      "auslaender": {"value": 5.7}},
            "winner": "cdu",
            "winnerOld": "cdu",
            "votes": 170396
            }
