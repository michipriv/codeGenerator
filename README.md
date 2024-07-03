# Filename: README.md

Ideen


error log ist verloren gegangen ohne lib  loggin alle bidlschirmmeldungen und alle fehelrmledungen in datei logen, 
je nach porgrmmstart mit datum/zeit aufteilen
modul: einlesen eines bestehenedn Programmcodes in die sitzung
modul: einlesen vo internet information zb zu einer Api oder programm beispiele

erledigt: strg +f ohne code einfügen startet programm
erledigt:automatisches erstellend er verz bak, etc log

# Prompt 1 um in einem neuen Chatverlauf die Klassen des Codegenrators zu hinterlegen

Verhalte dich wie ein Python-Entwickler, der objektorientiert und mit Klassen entwickelt.
Ich poste dir nun einen Code, der aus mehreren Klassen besteht.
Bei der Antwort füge im Codeblock immer die Zeile mit: #Filename ein, das ist extrem wichtig für die Zuordnung.
Lies den Code nur ein und warte, bis ich das Stichwort BINGO schreibe.

Die Verzeichnisstruktur sieht so aus:
Unter modules liegen die Klassen

codeGenerator/
│
├── main.py
├── etc/                # Verzeichnis für API-Schlüssel und Konfigurationsdateien
│   └── config.json     # Beispiel für eine weitere Konfigurationsdatei
├── log/                # Verzeichnis für Logdateien
│   ├── app.log         # Beispiel für eine Logdatei
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



# Prompt 2
Ablaufbeschreibung

Datei schreiben:
python3 main.py  -d test.py
Starte das Programm in einer Linux-Shell und übergibt den Dateinamen test.py.
Das Programm wartet in einer Eingabezeile, bis ein Programmcode eingefügt wird.
Nach dem Einfügen wird mittels Strg + D der eingefügte Code in die jeweilige Datei enigefügt bzw vorher das Verzeichnis und die datei erstellt.
Mit STRG +F wird gespeichert und zusätzlich die Datei in der run klasse ausgeführt.
Wird strg +f gedrückt und es ist kein Code eingegegben wird die datei in der runklasse ausgeführt

Kommunikation:
Zusätzlich starte über die main.py einen Server, um mit anderen Bereichen des Programmes zu kommunizieren.
der austausch zwischen code speichern und ausführen erfplgt über die serveroutine

Programm ausführen:
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
Das ist wichtig da ich diee ausgabe einer KI routine übergebe die auf diese Stichwörter lauscht
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

Verhalte dich wie ein Python experte.
Sende am Anfang des codes immer Folgendes: # Filename: test.py Erstelle als Ausgabe nur Python code keine erklärungen.
Eerstelle  "Hello World" das ASCII druckt



# GitHub einchecken
git add .
git commit -m "."
git push


# Virtuelle Umgebung für Modul-Installation erzeugen:

python3 -m venv myenv
source myenv/bin/activate
cd /mnt/c/tmp/codeGenerator

python3 main.py -s                # startet server
python3 main.py -ki -d test.py    #KI eingabe (in entwicklung)


#start in anderem verzeichnis
cd test                                             #neues Programm
mkdir bak && mkdir log && mkdir etc

python3 ../codeGenerator/main.py -d main.py         # Übergabe der Main Datei, diese wird durch run ausgeführt
                                                    # alle anderen Datein werden in eigene Klassen geschrieben
python3 ../codeGenerator/main.py -r -p python3      #führt die -d Main datei automatisch aus, alle anderen Dateien werden nicht aufgerufen




beispiel für gcc

python3 main.py -r test -p "gcc -o test"

lsof -i :47011
