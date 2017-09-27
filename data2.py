import subprocess
import json

BASE_PATH = "./bundeswahlleiter/"

class WahlData:
    def __init__(self):
        self._wks = None

    def wahlergebnis_json(self):
        if self._wks is None:
            with open(BASE_PATH + "wahlergebnis.json", "r", encoding="utf-8") as f:
                self._wks = json.load(f)
        return self._wks

    def wahlmetadaten_json(self):
        with open(BASE_PATH + "wahlmetadaten.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def party_data(self):
        wks = self.wahlergebnis_json()
        parties = dict()
        for p in wks["parteien"]:
            parties[p["schluessel"]] = {
                "id": p["schluessel"],
                "name": p["name"]["de"],
                "shortname": p["kurzname"]["de"],
                "color": p.get("farbe", "808080"),
                "type": p["type"],
            }
        return parties

    def result_data(self, artId="ERSTSTIMMEN"):
        wks = self.wahlergebnis_json()
        res = dict()
        def _get_datensaetze(ds):
            return sorted([{
                "id": x["parteiSchluessel"],
                "value": x["wert"],
                "name": x["label"]["de"],
            } for x in ds], key=lambda r: -r["value"])
        for r in wks["gebietsergebnisse"]:
            if r["gebietsergebnisArtId"] == artId:
                res[r["gebietId"]] = _get_datensaetze(r["datensaetze"])
        return res

if __name__ == "__main__":
    def get_url(url):
        subprocess.call(("wget", "--directory-prefix=%s" % BASE_PATH, url))

    for url in (
            'https://bundeswahlleiter.de/dam/jcr/66816b6a-1b9d-4563-8017-d8beed5dd7e3/gebietsdaten.json',
            'https://bundeswahlleiter.de/dam/jcr/bac614e2-3cc2-48b4-b929-4b53d70b0e80/wahlmetadaten.json',
            'https://bundeswahlleiter.de/dam/jcr/879f26d9-4cba-4f49-a911-42d9282d2b16/strukturdaten.json',
            'https://bundeswahlleiter.de/dam/jcr/f00c03fe-cf87-46f4-a6ec-981bc65dcb35/wahlergebnis.json',
            'https://bundeswahlleiter.de/dam/jcr/e8143880-7cce-4252-af73-103a47856fd3/suchindex.json',
            ):
        get_url(url)
