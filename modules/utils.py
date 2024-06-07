#Filename: utils.py


import os

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def print_help():
    help_message = """
Verwendung: python script.py [OPTION]

Optionen:
  -h, --help         Zeigt diese Hilfenachricht an
  -d DATEINAME       Bearbeitet nur die angegebene Datei
  -p PROGRAMM        Führt das angegebene Programm nach dem Bearbeiten der Datei aus

Ohne Parameter startet das Skript im interaktiven Modus und erwartet Eingaben im folgenden Format:
  Filename: [dateiname]

Beispiele:
  python script.py -h
  python script.py -d Dockerfile
  python script.py -d irgendeine_datei.txt -p "python your_program.py"
"""
    print(help_message)
