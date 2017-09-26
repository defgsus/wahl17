# Principal Component Analysis (PCA) für die Ergebnisse der Bundestagswahl 2017 pro Wahlkreis

Kleines Experiment zum Verständnis der politischen Situation.

Online hier: https://defgsus.github.io/wahl17/

### selber experimentieren

- getestet unter debian (siehe requirements.txt für nötige Pakete)
- virtualenv erzeugen mit **python 3.4+**, dann
```bash
pip install -r requirements.txt
python data.py
python make_website.py
```

`data.py` holt die json Daten von der [Welt.de - app](https://www.welt.de/politik/deutschland/article168883713).
Die Daten liegen hier auch hier im repo unter `./welt.de/` (Stand 25.Sep.2017).