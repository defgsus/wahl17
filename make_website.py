import math

from sklearn.decomposition import PCA
import numpy as np

from data import load_wahlkreise
from plothelper import render_template, get_scatter_plot_markup, test_plot

PARTY_COLORS = {
    "AfD": "#88f",
    "CDU": "#444",
    "CSU": "#444",
    "CDU/CSU": "#444",
    "FDP": "#ff8",
    "Grüne": "#5f5",
    "Linke": "#f8f",
    "NPD": "#f80",
    "SPD": "#f88",

    "Die Partei": "#444",
    "MLPD": "#f88",
    "Piraten": "#ff8", #?
    "ÖDP": "#8f8",
    "V-Partei": "#8f8",
    "Gesundheit": "#8f8",
    "Tierschutzpartei": "#8f8",
    "Freie Wähler": "#88f",
}

def get_party_color(name):
    return PARTY_COLORS.get(name, "#bbb")

def get_embedding_color(embedding, party_names):
    emb = [(embedding[i], party_names[i][1]) for i in range(len(embedding))]
    emb = sorted(emb, key=lambda t:-t[0])[:3]
    sum_ = np.amax([t[0] for t in emb])
    if sum_:
        emb = [(pow(t[0]/sum_, 2.), t[1]) for t in emb]
    col = [0,0,0]
    sum_ = 0.00001
    for t in emb:
        sum_ += t[0]
        c = get_party_color(t[1])
        for i in range(3):
            col[i] += int(c[i+1], 16) * t[0]
    return "#%x%x%x" % tuple(min(255, int(c/sum_*16)) for c in col)

CDU_CSU_MAPPING = {"p201": "p200", "CSU": "CDU/CSU", "CDU": "CDU/CSU"}

def calc_party_embedding(wks, value_key="percent1", party_mapping=None):
    party_mapping = party_mapping or {}
    def _mapping(p):
        return party_mapping.get(p, p)
    party_set = set()
    for wk in wks.values():
        for r in wk["results"]:
            party_set.add((_mapping(r["id"]), _mapping(r["partyname"])))
    party_set = sorted(party_set, key=lambda t: t[1])
    party_idx = {t[0]: i for i, t in enumerate(party_set)}
    for wk in wks.values():
        embedding = [0.] * len(party_set)
        for r in wk["results"]:
            embedding[party_idx[_mapping(r["id"])]] += r[value_key]
        wk["embedding"] = embedding
    return party_set


def _signed(x):
    return "+%s" % x if x > 0 else "%s" % x


def get_party_plot(attribute, party_mapping, title, remove_parties=(), size_mult=1., min_displ=5.):
    party_mapping = party_mapping or {}
    if remove_parties:
        title += "  (ohne %s)" % "/".join(remove_parties)

    wks = load_wahlkreise(remove_parties=remove_parties)
    wks = {wk["wkid"]: wk for wk in wks.values() if wk.get("name")}
    party_names = calc_party_embedding(wks, attribute, party_mapping)
    print("%s %s" % (attribute, sorted(p[1] for p in party_names)))

    #party_names = get_party_grid("percent1")
    #X = np.array([g for g in wks.values()], dtype="float32")
    EMB, LABELS, COLORS, WKNAME, SIZES = [], [], [], [], []
    for wk in wks.values():
        embedding = wk["embedding"]
        EMB.append(embedding)
        results = [(party_mapping.get(r["partyname"], r["partyname"]),
                    r[attribute],
                    _signed(r.get(attribute+"Diff", 0)),
                    r["absolute2"],
                    ) for r in wk["results"]]
        results = sorted(results, key=lambda r: -r[1])
        def _check(res):
            return res[1] >= min_displ and (attribute!="percent2Diff" or res[1] != 0)
        if attribute=="percent2":
            LABELS.append(", ".join("%s %s (%s)" % r[:3] for r in results if _check(r)))
        elif attribute=="percent2Diff":
            LABELS.append(", ".join("%s %s" % (r[0], _signed(r[1])) for r in results if _check(r)))
        else:
            LABELS.append(", ".join("%s %s" % r[:2] for r in results if _check(r)))

        WKNAME.append("%s %s" % (wk["wkid"], wk.get("name", "-")))
        #COLORS.append(get_party_color(results[0][0]))
        COLORS.append(get_embedding_color(embedding, party_names))
        SIZES.append(max(3., min(20., results[0][3]/8000.*size_mult)))

    pca = PCA(n_components=2, svd_solver='full')
    X = pca.fit(EMB).transform(EMB)

    markup = get_scatter_plot_markup(
        {
            "x": [x[0] for x in X],
            "y": [x[1] for x in X],
            "size": SIZES,
            "color": COLORS,
            "Parteien": LABELS,
            "Wahlkreis": WKNAME,
        },
        title=title,
        width=600, height=600
    )
    return markup

if 1:
    REMOVE_PARTIES1 = sorted(("CDU", "CSU", "SPD"))
    REMOVE_PARTIES2 = sorted(("CDU", "CSU", "SPD", "FDP", "AfD", "Linke", "Grüne"))
    render_template("./website/index.template", "./index.html", {
        "plot1": get_party_plot("percent1", {}, "Erststimmen % pro Wahlkreis"),
        "plot2": get_party_plot("percent2", {}, "Zweitstimmen % pro Wahlkreis"),
        "plot3": get_party_plot("percent1", CDU_CSU_MAPPING, "Erststimmen % pro Wahlkreis (CDU/CSU zusammen)"),
        "plot4": get_party_plot("percent2", CDU_CSU_MAPPING, "Zweitstimmen % pro Wahlkreis (CDU/CSU zusammen)"),
        "plot5": get_party_plot("percent1", {}, "Erststimmen % pro Wahlkreis", REMOVE_PARTIES1, 2., 0.1),
        "plot6": get_party_plot("percent2", {}, "Zweitstimmen % pro Wahlkreis", REMOVE_PARTIES1, 2., 0.1),
        "plot7": get_party_plot("percent1", {}, "Erststimmen % pro Wahlkreis", REMOVE_PARTIES2, 17., 0.1),
        "plot8": get_party_plot("percent2", {}, "Zweitstimmen % pro Wahlkreis", REMOVE_PARTIES2, 17., 0.1),
        "plot9": get_party_plot("percent2Diff", {}, "Zuwachs an Zweitstimmen % pro Wahlkreis", (), 2., -100.),
        "plot10": get_party_plot("percent2Diff", {}, "Zuwachs an Zweitstimmen % pro Wahlkreis", ("AfD", "FDP"), 2., -100.),
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
