import sys

class ArgumentParser:
    def __init__(self):
        self.help = False
        self.edit_filename = None
        self.program_to_run = None
        self.run_mode = False
        self.parse_arguments()

    def parse_arguments(self):
        if len(sys.argv) > 1:
            if '-h' in sys.argv or '--help' in sys.argv:
                self.help = True
            elif '-d' in sys.argv:
                filename_index = sys.argv.index('-d') + 1
                if filename_index < len(sys.argv):
                    self.edit_filename = sys.argv[filename_index]
                else:
                    print("Kein Dateiname angegeben. Verwenden Sie das Format 'python3 main.py -d <filename>'")
                    sys.exit(1)
            elif '-p' in sys.argv:
                program_index = sys.argv.index('-p') + 1
                if program_index < len(sys.argv):
                    self.program_to_run = sys.argv[program_index]
                else:
                    print("Kein Programm angegeben. Verwenden Sie das Format 'python3 main.py -p <program>'")
                    sys.exit(1)
            elif '-r' in sys.argv:
                self.run_mode = True
                program_index = sys.argv.index('-r') + 1
                if program_index < len(sys.argv):
                    self.program_to_run = sys.argv[program_index]
                else:
                    print("Kein Programm angegeben. Verwenden Sie das Format 'python3 main.py -r <program>'")
                    sys.exit(1)

    def print_help(self):
        help_message = """
Verwendung: python script.py [OPTION]

Optionen:
  -h, --help         Zeigt diese Hilfenachricht an
  -d DATEINAME       Bearbeitet nur die angegebene Datei
  -p PROGRAMM        Startet den Run-Server und führt das angegebene Programm nach dem Bearbeiten der Datei aus
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
