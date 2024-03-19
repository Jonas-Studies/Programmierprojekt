# Caymanchem
Link: https://www.caymanchem.com/forensics/search/productSearch
Notes:
- Sieht so aus als ließe sich ein Webservice ansprechen mit dem alle Daten geladen werden
# Isomerdesign - PiHKAL
Link: https://isomerdesign.com/PiHKAL/browse.php?domain=pk
Notes:
- Muss über HTML ausgelesen werden
- Liste aller Stoffe
- Unterseiten mit Infos. Hier auf explore *Stoff* gehen
- Unterseiten alle gleich strukturiert
- Unterseiten mit id nummeriert, Liste könnte also ignoriert werden
# Aipsin
Link: https://aipsin.com/newsubstance/100/
Notes:
- Russische Seite
- Muss mittels HTML ausgelesen werden
- Link mit laufender Nummer, keine Gesamtübersicht
- Unterseiten nicht alle gleich
# Slovenische Polizei
Link: https://www.policija.si/apps/nfl_response_web/seznam.php
Notes:
- Eine (gut strukturierte) Tabelle mit allen Infos
- Liste mit paging, aber option für alle. Liste wird auch immer komplett geladen.
- HTML muss ausgelesen werden
- Bilder wären extra Abfragen
# swgdrug
Link: https://swgdrug.org/monographs.htm
Notes:
- Liste mit Links zu pdf's
- Liste muss mittels HTML ausgelesen werden
- Liste ohne paging
- Textuelle Links, Liste wird benötigt
- Pdf's von unterschiedlichen Erstellern, aber im Aufbau einheitlich
- Schätzungsweise eher schwer auszulesen
# cfsre
Link: https://www.cfsre.org/nps-discovery/monographs
Notes:
- Liste mit Links zu pdf's
- Liste mit paging
- Textuelle Links, Liste wird benötigt
- Pdf's vom selben Ersteller, alle gleich im Aufbau
- Nur wenig Infos benötigt also wsl leichter auszulesen
# Wikipedia
Notes:
- Muss über HTML ausgelesen werden
- Eine Liste mit vielleicht allen Stoffen
- Kleinere Teillisten, alle anders strukturiert
- Einzelne Stoffe nicht zwingend gleich strukturiert