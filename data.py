# original article: https://www.welt.de/politik/deutschland/article168883713

import subprocess

for url in (
        'https://static.apps.welt.de/2017/bundestagswahl-2017/shapes/wahlkreise.json',
        'https://static.apps.welt.de/2017/bundestagswahl-2017/data/btwfeed-all-zip.json',
        'https://static.apps.welt.de/2017/bundestagswahl-2017/hochburgen/data/constituencies.json',
        'https://static.apps.welt.de/2017/bundestagswahl-2017/hochburgen/data/germanySmall.json',
        'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/config/areas.json',
        'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/summaryParties.json',
        'https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/summaryWinners.json'):
    subprocess.call(("wget", url))

for i in range(1, 917):
    url = "https://static.apps.welt.de/2017/dpa/bundestagswahl/bw_de/feed/s2017/votingAreas/wk%s.json" % i
subprocess.call(("wget", url))