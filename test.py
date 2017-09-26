from data import load_wahlkreise
from plothelper import get_scatter_plot_markup, test_plot


def render_template(in_filename, out_filename, context):
    with open(in_filename, "r") as f:
        html = f.read()
    for key in context:
        html = html.replace("{{ %s }}" % key, context[key])
    with open(out_filename, "w") as f:
        f.write(html)
    return html


#areas = load_area_data()
#print(areas["states"][0])

#wks = load_wahlkreise()
#print(wks[1])


markup = get_scatter_plot_markup([1,2,3], [4,5,3])
render_template("./website/index.template", "./website/index.html", {
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
