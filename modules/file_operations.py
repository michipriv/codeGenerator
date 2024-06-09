# Filename: file_operations.py

from modules.utils import clear_screen

class FileOperations:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager

    def read_input(self, prompt=""):
        try:
            return input(prompt)
        except EOFError:
            return None

    def edit_file(self, filename):
        while True:
            print(f"Bearbeiten der Datei: {filename}")
            print(f"Bitte geben Sie den neuen Inhalt für {filename} ein (Ende mit Strg+D):")
            new_content = []
            
            while True:
                try:
                    line = self.read_input()
                    if line is None:
                        print("Ende der Eingabe erkannt. Verarbeite den Inhalt...")
                        break
                    new_content.append(line)
                except KeyboardInterrupt:
                    print("Bearbeitung abgebrochen.")
                    return None
    
            self.process_content(new_content, filename)
            return 


    def process_content(self, new_content, filename):
        if new_content:
            try:
                self.backup_manager.manage_backups(filename)
                with open(filename, 'w') as f:
                    f.write('\n'.join(new_content))
                print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")
            except Exception as e:
                print(f"Fehler beim Schreiben der Datei {filename}: {e}")
        else:
            print("Kein neuer Inhalt angegeben. Datei wurde nicht geändert.")
