# Filename: file_operations.py

class FileOperations:
    def __init__(self, backup_manager):
        self.backup_manager = backup_manager

    def save_file(self, filename, content):
        try:
            self.backup_manager.manage_backups(filename)
            with open(filename, 'w') as f:
                f.write(content)
            print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {filename}: {e}")

    def read_input(self, prompt=""):
        try:
            return input(prompt)
        except EOFError:
            return None
