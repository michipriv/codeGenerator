# Filename: modules/file_operations.py

import os
import shutil  # Fügen Sie diesen Import hinzu

class FileOperations:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager

    def ensure_directory(self, filepath):
        required_dirs = ['bak', 'log', 'etc']
        
        # Check if required directories exist, if not, create them
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(f"Verzeichnis {dir_name} erstellt.")
        
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Verzeichnis {directory} erstellt.")

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



#EOF
