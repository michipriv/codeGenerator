# Filename: modules/file_operations.py

import os
import shutil

class FileOperations:
    """
    Klasse zur Durchführung von Dateioperationen.

    Diese Klasse ermöglicht das Erstellen, Lesen, Schreiben, Löschen und Verwalten von Dateien und Verzeichnissen,
    sowie das Verwalten von Backups.

    Attributes:
        backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
    """

    def __init__(self, backup_manager):
        """
        Initialisiert die FileOperations-Klasse.

        Parameters:
            backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
        """
        self.backup_manager = backup_manager

    def ensure_directory(self, filepath):
        """
        Stellt sicher, dass das Verzeichnis für den angegebenen Dateipfad existiert.

        Parameters:
            filepath (str): Der Pfad zur Datei, für die das Verzeichnis überprüft wird.
        """
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Verzeichnis {directory} wurde erfolgreich erstellt.")
        elif directory:
            print(f"Verzeichnis {directory} existiert bereits.")

    def save_file(self, filename, content):
        """
        Speichert den angegebenen Inhalt in der Datei.

        Parameters:
            filename (str): Der Name der Datei, in die der Inhalt geschrieben werden soll.
            content (str): Der Inhalt, der in die Datei geschrieben werden soll.
        """
        try:
            self.ensure_directory(filename)
            self.backup_manager.manage_backups(filename)
            with open(filename, 'w') as f:
                f.write(content)
            print(f"Datei {filename} wurde erfolgreich geändert und gesichert.")
        except Exception as e:
            print(f"Fehler beim Schreiben der Datei {filename}: {e}")

    def delete_file(self, filename):
        """
        Löscht die angegebene Datei.

        Parameters:
            filename (str): Der Name der Datei, die gelöscht werden soll.
        """
        try:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Datei {filename} wurde erfolgreich gelöscht.")
            else:
                print(f"Datei {filename} existiert nicht.")
        except Exception as e:
            print(f"Fehler beim Löschen der Datei {filename}: {e}")

    def create_directory(self, directory):
        """
        Erstellt das angegebene Verzeichnis.

        Parameters:
            directory (str): Der Name des Verzeichnisses, das erstellt werden soll.
        """
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Verzeichnis {directory} wurde erfolgreich erstellt.")
            else:
                print(f"Verzeichnis {directory} existiert bereits.")
        except Exception as e:
            print(f"Fehler beim Erstellen des Verzeichnisses {directory}: {e}")

    def delete_directory(self, directory):
        """
        Löscht das angegebene Verzeichnis und seinen Inhalt.

        Parameters:
            directory (str): Der Name des Verzeichnisses, das gelöscht werden soll.
        """
        try:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                print(f"Verzeichnis {directory} wurde erfolgreich gelöscht.")
            else:
                print(f"Verzeichnis {directory} existiert nicht.")
        except Exception as e:
            print(f"Fehler beim Löschen des Verzeichnisses {directory}: {e}")

    def read_file(self, filename):
        """
        Liest den Inhalt der angegebenen Datei.

        Parameters:
            filename (str): Der Name der Datei, die gelesen werden soll.

        Returns:
            str: Der Inhalt der Datei oder None, wenn ein Fehler auftritt.
        """
        try:
            with open(filename, 'r') as f:
                content = f.read()
            print(f"Datei {filename} wurde erfolgreich gelesen.")
            return content
        except Exception as e:
            print(f"Fehler beim Lesen der Datei {filename}: {e}")
            return None

    def list_directory_files(self, directory):
        """
        Listet die Dateien im angegebenen Verzeichnis auf.

        Parameters:
            directory (str): Der Pfad zum Verzeichnis, dessen Dateien aufgelistet werden sollen.

        Returns:
            list: Eine Liste der Dateien im Verzeichnis oder eine leere Liste, wenn das Verzeichnis nicht existiert.
        """
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

    def list_project_files(self):
        """
        Listet die Projektdateien im aktuellen Verzeichnis auf.

        Diese Methode sucht im Hauptverzeichnis nach der Datei main.py und
        im modules-Verzeichnis nach allen Python-Dateien.
        """
        current_dir = os.getcwd()
        print(f"Einlesen des aktuellen Verzeichnisses: {current_dir}")

        # Hauptverzeichnis durchsuchen und nur main.py ausgeben
        main_py_file = os.path.join(current_dir, 'main.py')
        if os.path.exists(main_py_file):
            print(f"Gefundene Datei im Hauptverzeichnis: {main_py_file}")
        else:
            print("Keine main.py im Hauptverzeichnis gefunden.")

        # Modules-Verzeichnis durchsuchen und alle .py-Dateien auflisten
        modules_dir = os.path.join(current_dir, 'modules')
        if os.path.exists(modules_dir) and os.path.isdir(modules_dir):
            py_files = [f for f in os.listdir(modules_dir) if f.endswith('.py')]
            if py_files:
                print("Gefundene .py-Dateien im modules-Verzeichnis:")
                for py_file in py_files:
                    print(py_file)
            else:
                print("Keine .py-Dateien im modules-Verzeichnis gefunden.")
        else:
            print("Kein modules-Verzeichnis gefunden.")

# EOF
