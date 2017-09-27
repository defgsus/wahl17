from data2 import WahlData

wd = WahlData()

# ['kategorien', 'themen', 'version', 'gebietsergebnisArten', 'gebietsergebnisse', 'parteien', 'merkmale']
PARTEI = {'type': 'PARTEI',
          'name': {'de': 'Christlich Demokratische Union Deutschlands',
                   'en': 'Christlich Demokratische Union Deutschlands'},
          'schluessel': '2',
          'kurzname': {'de': 'CDU', 'en': 'CDU'},
          'inPraesentation': True,
          'farbe': '44448A'}
PARTEI2 = {'type': 'EINZELBEWERBER',
           'name': {'de': 'Bürgerkandidaten für Gemeinwohl und Volksentscheid',
                    'en': 'Bürgerkandidaten für Gemeinwohl und Volksentscheid'},
           'inPraesentation': False,
           'schluessel': '565',
           'kurzname': {'de': 'EB: Maier', 'en': 'EB: Maier'}
           }
GEBIETSERGEBNIS = {
    'gebietId': 'bund-99',
    'gebietsergebnisArtId': 'ERSTSTIMMEN',
    'datensaetze': [
        {'wertFormatiert': {'en': '30.2', 'de': '30,2'}, 'wert': 30.244956, 'label': {'en': 'CDU', 'de': 'CDU'}, 'parteiSchluessel': '2'},
    ]}
WAHLTMETA = ['kategorien', 'merkmale', 'wahlatlasLokalisierungen', 'wahlName', 'themen', 'version', 'gebietsdaten', 'parteien']

# print(wd.party_data())
#wks = wd.wahlergebnis_json()
#print(wks["gebietsergebnisse"][601])
meta = wd.wahlmetadaten_json()
for m in meta["merkmale"]:
    print(m)
    break
#for m in wks["gebietsergebnisse"]:
#    print(m["gebietsergebnisArtId"])
