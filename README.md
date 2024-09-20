# Filename: README.md

Ideen


übersicht erstellen: welche klassen, welche funktione, damit nicht der gganze code inegelsen werden muss
modul: einlesen eines bestehenedn Programmcodes aus einem Verzeichnis in die bestehende KI-sitzung. file operations datei lesen und directory lesen erstellen
modul: einlesen von internet information zb zu einer Api oder programm beispiele
run: möglichkeit um libraries nachzu installieren wenn diese benötigt werden
error log ist verloren gegangen ohne lib  loggin alle bidlschirmmeldungen und alle fehelrmledungen in datei logen, logik mit datum/zeit 
AST Soruce Code verwaltung damit die KI den Code effizienter versteht


erledigt: strg +f ohne code einfügen startet programm
erledigt: automatisches erstellend er verz bak, etc log
erledigt: ### mkdir bak && mkdir log && mkdir etc  wird durhc programm erstellt wenn neue datein geschrieben werden
erledigt: Ki sendet zusätzlich an filemanager, code einfügen bleibt optional bestehen, filemanager kann auch strg f prg ausführen. beides kann gleichzeitig genutzt werden
erledigt: filemanager gibt bescheid das er eine nachricht von openai erhalten hat
erledigt: löschen von dateien und verzeichnise
erledigt: ki programmierung: es muss code und es müssen fragen über eine sitzung erstellt werden. trenne code und trenne fragen
erledigt: befehle für verbindungsdaufbau, senden , empfangen einheiltich machen und als beispiel erstellen ABleietn aus class run und filemanager
erledigt: Filemanager in klassen /dateien aufteilen
erledigt: normalisierung dateien erstellen,löschen verzeichnise ersteleln und löschen


# Prompt 1 um in einem neuen Chatverlauf die Klassen des Codegenrators zu hinterlegen

Verhalte dich wie ein Python-Entwickler, der objektorientiert und mit Klassen entwickelt.
Erstelle Klassen und programmierung so das Sie wiederverwendbar sind. 
Ich poste dir nun einen Code, der aus mehreren Klassen besteht.
Bei der Antwort füge im Codeblock immer die Zeile mit: #Filename ein, das ist extrem wichtig für die Zuordnung.
beachte die maximale Token grenze von 4096 wenn du klassen erstellst. teile klassen in kleine übersichtbare funktionen auf
verwende Python Docstring Conventions für die docu
Lies den Code nur ein und warte, bis ich das Stichwort BINGO schreibe.



#OPENAI Prompt

Openai:
Ich möchte, dass du immer die Version V1.35.10 der OpenAI-Python-Bibliothek verwendest. 
Bitte überprüfe jedes Mal, ob die von dir verwendeten Methoden und Syntax mit dieser Version kompatibel sind. 
Vermeide die Verwendung von veralteten Methoden wie openai.ChatCompletion.create. 
Verwende stattdessen die aktuell gültige API-Syntax für V1.35.10.
lese die api https://github.com/openai/openai-python/blob/main/api.md
lese https://github.com/openai/openai-python




#Prompt verz
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
│   └── config.yaml     # Beispiel für eine weitere Konfigurationsdatei
│   ├── ...             # Inhalte der virtuellen Umgebung
├── modules/


# test prompt in chatgpt

Verhalte dich wie ein Python experte.
Sende am Anfang des codes immer Folgendes: # Filename: test.py Erstelle als Ausgabe nur Python code keine erklärungen.
Erstelle  "Hello World" das ASCII druckt



#testprompt für codegenerator
Erstelle  "Hello World" in ASCII Art




# GitHub einchecken
git add .
git commit -m "."
git push





# Virtuelle Umgebung für Modul-Installation erzeugen:

python3 -m venv myenv
source myenv/bin/activate



##libs
pip3 install zmq
pip3 install openai
pip3 install tiktoken
pip3 install pybamm



pip3 install pyfiglet		#ascii lib
pip3 install ascii_magic	#ascii lib


# Programm starten
cd /mnt/c/tmp/codeGenerator
python3 main.py -s                # startet server

#start in anderem verzeichnis
cd /mnt/c/tmp/test

python3 ../codeGenerator/main.py -d main.py             # Filemanagerklasse:  Übergabe der Main Datei, diese wird durch die Klasse run ausgeführt
                                                        # alle anderen Datein werden in eigene Klassen geschrieben
                                                        # Strg + C beenden
                                                        # Strg + D speichern
                                                        # Strg + F speichern und ausführen in der run klasse
                                                        # Strg + L liest im aktuellen Verz die main.py und alle python datein aus dem Modul verz.

python3 ../codeGenerator/main.py -ki -p python-entwickler  #KI eingabe 

python3 ../codeGenerator/main.py -r                     #run klasse: führt die -d Main datei automatisch aus, alle anderen Dateien werden nicht aufgerufen



python3 ../codeGenerator/main.py -m "test" -z "beispiel"      #sendet testnachricht an server oder andee client
python3 ../codeGenerator/main.py -m "test" -z "file_manager" -t 10k      #sendet testnachricht mit der größe 10k

python3 ../codeGenerator/main.py -bsp  client2              # Beispiel klasse für senden und empfangen von nachrichten, verwenden um neue klasse das senden und empfange beizubringen
                                                            # cleint1 auslassen
python3 ../codeGenerator/main.py -bsp  client3              # Beispiel klasse für senden und empfangen von nachrichten, verwenden um neue klasse das senden und empfange beizubringen
Nachrichten format:  client2:Helllo world


#andere Porgrammiersprache
beispiel für gcc

python3 main.py -r test -p "gcc -o test"

lsof -i :47011
kill -9 pid


#openai version der installierten openai lib ist wichtig diese muss der aus github entsprechen
https://github.com/openai/openai-python

PyPI version: V1.35.10

pythons starten:

import openai
print(openai.__version__)




#EOF
