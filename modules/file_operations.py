#Filename: file_operations.py

import os
from modules.utils import clear_screen

class FileOperations:
    def __init__(self, backup_manager, logger):
        self.backup_manager = backup_manager
        self.logger = logger

    def read_input(self):
        try:
            return input()
        except EOFError:
            return None  # EOFError wird abgefangen und None zurückgegeben

    def edit_file(self, filename):
        self.logger.info(f"Bearbeiten der Datei: {filename}")
        print(f"Bitte geben Sie den neuen Inhalt für {filename} ein (Ende mit Strg+D):")
        new_content = []

        while True:
            line = self.read_input()
            if line is None:
                self.logger.info("Ende der Eingabe erkannt. Verarbeite den Inhalt...")
                break
            new_content.append(line)

        self.process_content(new_content, filename)

    def process_content(self, new_content, filename):
        if new_content:
            try:
                self.backup_manager.manage_backups(filename)
                with open(filename, 'w') as f:
                    f.write('\n'.join(new_content))

                #clear_screen()
                self.logger.info(f"Datei {filename} wurde erfolgreich geändert und gesichert.")

            except Exception as e:
                self.logger.error(f"Fehler beim Schreiben der Datei {filename}: {e}")
        else:
            self.logger.info("Kein neuer Inhalt angegeben. Datei wurde nicht geändert.")
        self.logger.info("Bearbeitung abgeschlossen. Signal wird gesendet.")
