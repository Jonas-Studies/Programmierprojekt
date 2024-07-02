# Programmierprojekt

## Installation

Es müssen Node und Python 3.12.4 installiert sein, damit das Programm problemfrei laufen kann.  

Wichtig: Python 3.12.4 muss der erste Eintrag in Path sein.  
Dies kann überprüft werden, indem `python --version` in der Konsole ausgeführt wird.

Danach können alle Abhängigkeiten durch Doppelklick auf `install.bat` installiert werden.

## Scrapen und Importieren

Alle JSON-Dateien (von anderen Teams), die importiert werden sollen, können im `Imports` Ordner abgelegt werden.

Durch Doppelklick auf `import.bat` werden alle Daten von `Imports` importiert, und alle Substanzen von Caymanchem gescraped.

## Ausführung

Durch Doppelklick auf `run.bat` startet die Suchmaschine.  
Wenn keine Daten angezeigt werden, muss vorher `import.bat` aufgerufen werden!

## Export

Die von Caymanchem importierten Substanzen können durch Doppelklick auf `export.bat` in den `Exports` exportiert werden.

## Einstellungen

In `Python\settings.py` können einige Einstellungen vorgenommen werden:
- Datenbank-Einstellungen
- Logging-Level
- Korrigieren der Substanzeigenschaften
- Genutzte CPU-Threads beim validieren/korrigieren der Daten
- Exporteinstellungen
