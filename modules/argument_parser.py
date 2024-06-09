#Filename: argument_parser.py

import sys

class ArgumentParser:
    def __init__(self):
        self.help = False
        self.edit_filename = None
        self.program_to_run = None
        self.run_mode = False
        self.ki = False
        self.server_mode = False
        self.parse_arguments()

    def parse_arguments(self):
        if len(sys.argv) > 1:
            if '-h' in sys.argv or '--help' in sys.argv:
                self.help = True
            if '-d' in sys.argv:
                filename_index = sys.argv.index('-d') + 1
                if filename_index < len(sys.argv):
                    self.edit_filename = sys.argv[filename_index]
                else:
                    print("Kein Dateiname angegeben. Verwenden Sie das Format 'python3 main.py -d <filename>'")
                    sys.exit(1)
            if '-r' in sys.argv:
                self.run_mode = True
                program_index = sys.argv.index('-r') + 1
                if program_index < len(sys.argv):
                    self.program_to_run = sys.argv[program_index]
                else:
                    print("Kein Programm angegeben. Verwenden Sie das Format 'python3 main.py -r <program>'")
                    sys.exit(1)
            if '-s' in sys.argv:
                self.server_mode = True
            if '-ki' in sys.argv:
                self.ki = True

    def print_help(self):
        help_message = """
Verwendung: python script.py [OPTION]

Optionen:
  -h, --help         Zeigt diese Hilfenachricht an
  -d DATEINAME       Bearbeitet nur die angegebene Datei
  -r PROGRAMM        Startet den Run-Server und wartet auf Befehle, um das angegebene Programm auszuführen
  -s                 Startet den Server
  -ki                Führt die OpenAI-Integration aus und generiert Code basierend auf einer Beschreibung

Ohne Parameter startet das Skript im interaktiven Modus und erwartet Eingaben im folgenden Format:
  DATEINAME

Beispiele:
  python script.py -h
  python script.py -d Dockerfile
  python script.py -d irgendeine_datei.txt -r /mnt/c/tmp/test.py
  python script.py -s
  python script.py -ki
"""
        print(help_message)
