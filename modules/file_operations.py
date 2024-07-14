# Filename: modules/file_operations.py

import os
import shutil

class FileOperations:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager

    def ensure_directory(self, filepath):
        # Ensure the directory for the file path exists
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Verzeichnis {directory} wurde erfolgreich erstellt.")
        elif directory:
            print(f"Verzeichnis {directory} existiert bereits.")

    def save_file(self, filename, content):
        try:
            self.ensure_directory(filename)
            self.backup_manager.manage_backups(filename)
            with open(filename, 'w') as f:
                f.write(content)
            print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {filename}: {e}")

    def delete_file(self, filename):
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Datei {filename} wurde erfolgreich gelöscht.")
            else:
                print(f"Datei {filename} existiert nicht.")
        except Exception as e:
            print(f"Fehler beim Löschen der Datei {filename}: {e}")

    def create_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Verzeichnis {directory} wurde erfolgreich erstellt.")
            else:
                print(f"Verzeichnis {directory} existiert bereits.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Verzeichnisses {directory}: {e}")

    def delete_directory(self, directory):
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                print(f"Verzeichnis {directory} wurde erfolgreich gelöscht.")
            else:
                print(f"Verzeichnis {directory} existiert nicht.")
        except Exception as e:
            print(f"Fehler beim Löschen des Verzeichnisses {directory}: {e}")
            import traceback
            traceback.print_exc()

    def read_file(self, filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(f"Datei {filename} wurde erfolgreich gelesen.")
            return content
        except Exception as e:
            print(f"Fehler beim Lesen der Datei {filename}: {e}")
            return None

    def list_directory_files(self, directory):
        try:
            if os.path.exists(directory):
                files = os.listdir(directory)
                print(f"Dateien im Verzeichnis {directory}: {files}")
                return files
            else:
                print(f"Verzeichnis {directory} existiert nicht.")
                return []
        except Exception as e:
            print(f"Fehler beim Auflisten der Dateien im Verzeichnis {directory}: {e}")
            return []

#EOF
