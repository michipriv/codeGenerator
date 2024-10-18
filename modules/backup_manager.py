# Filename: modules/backup_manager.py

import os
import shutil

class BackupManager:
    """
    Klasse zur Verwaltung von Datei-Backups.

    Diese Klasse erstellt und verwaltet Backups von Dateien, wobei bis zu drei Versionen
    der Backup-Datei gespeichert werden. Die älteste Backup-Version wird überschrieben,
    wenn eine neue Backup-Datei erstellt wird.

    Attributes:
        backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden.
    """

    def __init__(self, backup_dir: str = 'bak'):
        """
        Initialisiert die BackupManager-Klasse und erstellt das Backup-Verzeichnis,
        falls es noch nicht existiert.

        :param backup_dir: Das Verzeichnis, in dem die Backups gespeichert werden sollen.
                           Standardmäßig 'bak'.
        """
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def manage_backups(self, filename: str) -> None:
        """
        Verwalte die Backups für die angegebene Datei.

        Diese Methode verwaltet bis zu drei Backup-Versionen einer Datei. Das älteste Backup
        (Backup3) wird gelöscht, Backup2 wird auf Backup3 verschoben, Backup1 auf Backup2,
        und die neue Backup-Datei wird als Backup1 erstellt.

        :param filename: Der Pfad zur Datei, für die das Backup erstellt werden soll.
        :return: None
        """
        base_filename = os.path.basename(filename)
        backup1 = os.path.join(self.backup_dir, f"{base_filename}.bak1")
        backup2 = os.path.join(self.backup_dir, f"{base_filename}.bak2")
        backup3 = os.path.join(self.backup_dir, f"{base_filename}.bak3")

        # Entfernen des ältesten Backups (Backup3)
        if os.path.exists(backup3):
            os.remove(backup3)

        # Verschieben von Backup2 nach Backup3
        if os.path.exists(backup2):
            os.rename(backup2, backup3)

        # Verschieben von Backup1 nach Backup2
        if os.path.exists(backup1):
            os.rename(backup1, backup2)

        # Erstellen eines neuen Backups von der Originaldatei als Backup1
        if os.path.exists(filename):
            shutil.copy2(filename, backup1)

#EOF
