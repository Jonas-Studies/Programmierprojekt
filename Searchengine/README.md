# Anwendung
Die Anwendung ist eine nodejs Webanwendung welche unter **Port 3000** gestartet wird.
Sie ermöglicht dass Suchen nach von den Webscrapern ermittelten Designerdrogen.
# Dateistruktur
```
Searchengine
├── main.js
├── database.js
├── models
├── views
└── public
```
## main.js
Die Datei `main.js` ist der Startpunkt des Webservers, diese definiert die vom Server bereitgestellten Routen.
## database.js
Die Datei `database.js` exportiert eine Klasse zum verwenden der MongoDB des Projekts.
## models
Der Ordner `models` enthält js-module welche zum Bedienen der Datenbank verwendet werden.
## views
Der Ordner `views` enthält alle pug-templates und pug-mixins welche für die Anzeigen der Suchmaschine benötigt werden.
## public
Der Ordner `public` enthält alle Dateien welche dem Client zur Verfügung gestellt werden. Dieser unterteilt sich in folgende Unterordner:
```
public
├── css
├── js
├── icons
└── fonts
```
### css
Der Ordner `css` enthält alle Stylesheets. Von diesen existiert ein Stylesheet `layout` mti globalen css Optionen. Sowie ein Stylesheet für jedes pug-template und pug-mixin, welches gleich diesem Benannt ist.
### js
Der Ordner `js` enthält alle von der Website benötigten js Skripte.
### icons
Der Ordner `icons` enthält eine svg Datei mit allen Bootstrap-Icons.
### fonts
Der Ordner `fonts` enthält alle von der Anwendung verwendeten fonts.
