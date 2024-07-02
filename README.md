# Programmierprojekt

## Installation

Zum Verwenden der Anwendung müssen NodeJs und Python 3.12.4 installiert sein.

Die Anwendung kann mit folgenden Commands installiert werden:
``` bash
git clone https://github.com/Jonas-Studies/Programmierprojekt

cd Programmierprojekt

install.bat
```

Diese Befehle downloaden die Anwendung und installieren alle von dieser benötigten Module.

## Scrapen und Importieren

Alle JSON-Dateien (von anderen Teams), die importiert werden sollen, können im `Imports` Ordner abgelegt werden.

Durch ausführen von `import.bat` werden alle json-Dokumente welche im Ordner `Imports` liegen importiert, und alle Substanzen von Caymanchem gescraped.

## Ausführung

Das Skript `run.bat` startet die Anwendung.

## Export

Die von Caymanchem importierten Substanzen können durch ausführen von `export.bat` in den Ordner `Exports` gelegt werden.

## Einstellungen

In `Python\settings.py` können einige Einstellungen am Webscraper vorgenommen werden:
- Datenbank-Einstellungen
- Logging-Level
- Korrigieren der Substanzeigenschaften
- Genutzte CPU-Threads beim validieren/korrigieren der Daten
- Exporteinstellungen
