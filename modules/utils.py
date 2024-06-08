import os

def clear_screen():
    if (os.name == 'nt'):
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
  -r PROGRAMM        Startet den Run-Server und wartet auf Befehle, um das angegebene Programm auszuführen

Ohne Parameter startet das Skript im interaktiven Modus und erwartet Eingaben im folgenden Format:
  DATEINAME

Beispiele:
  python script.py -h
  python script.py -d Dockerfile
  python script.py -d irgendeine_datei.txt -p "python your_program.py"
  python script.py -r /mnt/c/tmp/test.py
"""
    print(help_message)
