import os
from modules.utils import clear_screen

class FileOperations:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager

    def read_input(self):
        try:
            return input()
        except EOFError:
            return None

    def edit_file(self, filename, program_to_execute=None):
        print(f"Bitte geben Sie den neuen Inhalt für {filename} ein (Ende mit Strg+D):")
        new_content = []

        while True:
            try:
                line = self.read_input()
                if line is None:
                    break
                new_content.append(line)
            except EOFError:
                print("\nEnde der Eingabe erkannt. Verarbeite den Inhalt...")
                break

        self.process_content(new_content, filename, program_to_execute)

    def process_content(self, new_content, filename, program_to_execute=None):
        if new_content:
            try:
                self.backup_manager.manage_backups(filename)
                with open(filename, 'w') as f:
                    f.write('\n'.join(new_content))

                clear_screen()
                print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")

                if program_to_execute:
                    print("Programm wird ausgeführt...")
                    os.system(program_to_execute)

            except Exception as e:
                print(f"Fehler beim Schreiben der Datei {filename}: {e}")
        else:
            print("Kein neuer Inhalt angegeben. Datei wurde nicht geändert.")
        print("Warten auf weitere Eingaben...")
