# original article: https://www.welt.de/politik/deutschland/article168883713

import subprocess
import json

BASE_PATH = "./welt.de/"

def _convert(dic, Type, keys):
    for key in keys:
        try:
            dic[key] = Type(dic[key])
        except ValueError:
            dic[key] = Type(0)

def load_area_data():
    """"""
    with open(BASE_PATH + "areas.json", "r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_wahlkreise():
    """Returns a dict with wkid -> Wahlkreis-object"""
    wks = dict()
    for i in range(1, 917):
        try:
            with open(BASE_PATH + "wk%s.json" % i, "r") as f:
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
    areas = load_area_data()
    for info in areas["states"]:
        wks[int(info["wkid"])]["name"] = info["nameLong"]
    return wks



if __name__ == "__main__":
    def get_url(url):
        subprocess.call(("wget", "--directory-prefix=%s" % BASE_PATH, url))

    for url in (
            'https://static.apps.welt.de/2017/bundestagswahl-2017/shapes/wahlkreise.json',
            'https://static.apps.welt.de/2017/bundestagswahl-2017/welt.de/btwfeed-all-zip.json',
            'https://static.apps.welt.de/2017/bundestagswahl-2017/hochburgen/welt.de/constituencies.json',
            'https://static.apps.welt.de/2017/bundestagswahl-2017/hochburgen/welt.de/germanySmall.json',
            'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/config/areas.json',
            'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/summaryParties.json',
            'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/summaryWinners.json'):
        get_url(url)

    for i in range(1, 917):
        url = "https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/wk%s.json" % i
        get_url(url)
