# Dateistruktur
**Für den Client:**
Alle Dateien des `public` Ordners werden für den Client bereitgestellt. Dieser Ordner unterteilt sich in die folgenden Unterordner:
- `css`: Enthält alle css stylesheets. Dabei existiert ein allgemeines Stylesheet `layout` sowie ein Stylesheet für die Ausrichtung von Elementen `aligment`, dieses wird direkt von pug templates verwendet. Zusätzlich existiert noch für jedes pug mixin ein eigenes Stylesheet welches gleich diesem benannt ist.
- `js`: Enthält alle vom Client benötigten javascript Skripte.
- `icons`: Enthält eine svg Datei mit allen Bootstrap-Icons.
- `fonts`: Enthält die von der Website verwendeten fonts.
**Für den Server:**
- `main.js`: Der Einstiegspunkt für den NodeJs Server.
- `database.js`: Exportiert eine Klasse zum verwenden der MongoDB.
- `modles`: Enthält Module zum bedienen der Datenbank.
    - `substances.js`: Exportiert Funktionen zum durchsuchen der Substanzen der Datenbank.
- `views`: Enthält alle Pug templates sowie pug mixins welche die Anwendung verwendet.
