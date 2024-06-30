# Filename: README.md

# Prompt 1 um in einem neuen Chatverlauf die Klassen des Codegenrators zu hinterlegen

Verhalte dich wie ein Python-Entwickler, der objektorientiert und mit Klassen entwickelt.
Ich poste dir nun einen Code, der aus mehreren Klassen besteht.
Bei der Antwort füge im Codeblock immer die Zeile mit: #Filename ein, das ist extrem wichtig für die Zuordnung.
Lies den Code nur ein und warte, bis ich das Stichwort BINGO schreibe.

# Prompt 2
Ablaufbeschreibung

Datei schreiben:
python3 main.py  -d test.py
Starte das Programm in einer Linux-Shell und übergibt den Dateinamen test.py.
Das Programm wartet in einer Eingabezeile, bis ein Programmcode eingefügt wird.
Nach dem Einfügen wird mittels Strg + D der eingefügte Code in die übergebene Datei -d test.py geschrieben.

Kommunikation:
Zusätzlich starte über die main.py einen Server, um mit anderen Bereichen des Programmes zu kommunizieren.

Programm testen:
python3 main.py  -r test.py
In einer zweiten Linux-Shell läuft das oben angeführte Programm.
Die Run-Klasse wartet nun auf den Ausführungsbefehl und startet dann das Python-Programm test.py.
Der Befehl kommt durch die Datei-schreiben-Klasse.
Sobald das File geschrieben wurde, wird der Befehl zum Starten des Programmes an die Run-Klasse gesendet.
In der Run-Klasse werden die Bildschirmausgaben - normal und Fehler - in eine Logdatei geschrieben, nur die der Run-Klasse.
Zusätzlich wird am Bildschirm die Ausgabe des Programmes angezeigt.

Alle Aufrufe passieren über main.py und werden dann durch die entsprechenden Klassen durchgeführt.
Die Funktionen sind in Klassen ausgelagert, um die Übersicht zu erhalten und die Dateien klein zu halten.

Lese die Programmbeschreibung und antworte ausschließlich: Wie kann ich dir helfen?

# Prompt 3
Die Verzeichnisstruktur sieht so aus:
Unter modules liegen die Klassen

codeGenerator/
│
├── main.py
├── etc/                # Verzeichnis für API-Schlüssel und Konfigurationsdateien
│   ├── api_key.json    # Beispiel für eine Konfigurationsdatei
│   └── config.json     # Beispiel für eine weitere Konfigurationsdatei
├── log/                # Verzeichnis für Logdateien
│   ├── app.log         # Beispiel für eine Logdatei
├── myenv/              # Verzeichnis für virtuelle Umgebung
│   ├── ...             # Inhalte der virtuellen Umgebung
├── modules/
│   ├── __init__.py
│   ├── file_operations.py
│   ├── backup_manager.py
│   ├── utils.py
│   ├── logger.py
│   ├── run.py
│   ├── server.py
│   ├── file_manager.py
│   ├── argument_parser.py
│   └── openai.py
├── bak/                # Verzeichnis für Backups
│   ├── ...



#Prompt 4

Ich kopiere nun die Änderungen in den Code und lasse das Programm laufen.
Sollte es Fehler geben, so poste ich dir diese, und du behebst die Fehler und erstellst mir ausschließlich die Dateien, 
die davon betroffen sind. Achte auch immer darauf, 
dass am Anfang jeder Klasse: #Filename: ... steht.


# Allgemeiner python Entwickler prompt

Verhalte dich wie ein Python Entwickler.
Erstelle Programme Obejektorientiert und in Klassen.
Lege die klassen im Verzeichnis Modul ab.
Füge bei der jeder Codeblock ausgabe am anfang das Wort "#Filename: " hinzu.
Verwende folgende verz struktur
Hauptprogramm/
│
├── main
├── etc/                # Verzeichnis für API-Schlüssel und Konfigurationsdateien
│   ├── api_key.json    # Beispiel für eine Konfigurationsdatei
│   └── config.json     # Beispiel für eine weitere Konfigurationsdatei
│   ├── ...             # Inhalte der virtuellen Umgebung
├── modules/


# test prompt
Sende am Anfang des codes immer Folgendes: # Filename: test.py Erstelle als Ausgabe nur Python code keine erklärungen. erstelle  "Hello World" das ASCII druckt



# GitHub einchecken
git add .
git commit -m "."
git push


# Virtuelle Umgebung für Modul-Installation erzeugen:

python3 -m venv myenv
source myenv/bin/activate
cd /mnt/c/tmp/codeGenerator

python3 main.py -s                # startet server
python3 main.py -d test.py -e m   #manuell eingabe, schreibt datei
python3 main.py -d test.py -e ki  #ki schreibt datei
python3 main.py -r -p python3     #führt programm aus
python3 main.py -ki -d test.py    #KI eingabe




python3 main.py -r test -p "gcc -o test"

lsof -i :47011
