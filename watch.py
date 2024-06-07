import os
import shutil
import sys
import signal

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def signal_handler(sig, frame):
    print("\nProgramm wurde beendet.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

clear_screen()

mkommentar = '''
Verhalte dich wie ein Docker und Linux Experte.
Verwende für die Codeblock-Ausgabe folgendes Format.
"""
Filename: [filename einsetzen]

Inhalt deiner Ausgabe

EOF
"""

Erstelle ein Dockerfile für Hummingbot
'''

print("")
print("Prompt:")
print("###################################################")
print("")
print(mkommentar)
print("")
print("###################################################")
print("")

# Dictionary mit Dateinamen
files = {
    "Dockerfile": "Dockerfile",
    "docker-compose.yml": "docker-compose.yml",
    "manage": "manage.sh",
}

# Verzeichnis für Backups
backup_dir = "bak"
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

def manage_backups(filename):
    base_filename = os.path.basename(filename)
    backup1 = os.path.join(backup_dir, f"{base_filename}.bak1")
    backup2 = os.path.join(backup_dir, f"{base_filename}.bak2")
    backup3 = os.path.join(backup_dir, f"{base_filename}.bak3")

    # Backup-Rotation
    if os.path.exists(backup3):
        os.remove(backup3)
    if os.path.exists(backup2):
        os.rename(backup2, backup3)
    if os.path.exists(backup1):
        os.rename(backup1, backup2)
    if os.path.exists(filename):
        shutil.copy2(filename, backup1)

def read_input():
    try:
        return input()
    except EOFError:
        return None

def edit_file(filename, program_to_execute=None):
    print(f"Bitte geben Sie den neuen Inhalt für {filename} ein (Ende mit Strg+D):")
    new_content = []

    while True:
        try:
            line = read_input()
            if line is None:
                break
            new_content.append(line)
        except EOFError:
            print("\nEnde der Eingabe erkannt. Verarbeite den Inhalt...")
            break

    process_content(new_content, filename, program_to_execute)

def process_content(new_content, filename, program_to_execute=None):
    if new_content:
        try:
            # Backups verwalten und Datei mit neuem Inhalt aktualisieren
            manage_backups(filename)
            with open(filename, 'w') as f:
                f.write('\n'.join(new_content))

            clear_screen()
            print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")

            if program_to_execute:
                # Nach dem erfolgreichen Schreiben abfragen, ob ein Programm ausgeführt werden soll
                print("Programm wird ausgeführt...")
                os.system(program_to_execute)

        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {filename}: {e}")
    else:
        print("Kein neuer Inhalt angegeben. Datei wurde nicht geändert.")
    print("Warten auf weitere Eingaben...")

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

# Hauptlogik
try:
    if len(sys.argv) > 1:
        if '-h' in sys.argv or '--help' in sys.argv:
            print_help()
        else:
            filename = None
            program_to_execute = None

            if '-d' in sys.argv:
                filename_index = sys.argv.index('-d') + 1
                if filename_index < len(sys.argv):
                    filename = sys.argv[filename_index]

            if '-p' in sys.argv:
                program_index = sys.argv.index('-p') + 1
                if program_index < len(sys.argv):
                    program_to_execute = sys.argv[program_index]


            if filename:
                while True:
                    edit_file(filename, program_to_execute)
            else:
                print("Fehler: Kein Dateiname angegeben. Verwenden Sie die Option -d, um einen Dateinamen anzugeben.")
                print_help()
    else:
        while True:
            print("Bitte geben Sie den neuen Inhalt ein:")

            line = read_input()
            if line is None:
                break

            if line.startswith("Filename: ") or line.startswith("# Filename: "):
                keyword = line.split("Filename: ")[1].strip()
            else:
                print("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
                continue

            # Überprüfen, ob das Stichwort im Dictionary existiert
            if keyword in files:
                filename = files[keyword]
                edit_file(filename)
            else:
                print("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
except KeyboardInterrupt:
    print("\nProgramm wurde beendet.")
    sys.exit(0)
