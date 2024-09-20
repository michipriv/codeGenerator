# Filename: modules/backup_manager.py

import os
import shutil

class BackupManager:
    """
    Klasse zur Verwaltung von Datei-Backups.

    Diese Klasse erstellt Backups von Dateien, indem sie bis zu drei Versionen
    der Backup-Datei speichert und sicherstellt, dass die älteste Version überschrieben
    wird, wenn eine neue Backup-Datei erstellt wird.

    Attributes:
        backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden.
    """

    def __init__(self, backup_dir='bak'):
        """
        Initialisiert die BackupManager-Klasse.

        Parameters:
            backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden. 
                              Standardmäßig 'bak'.
        """
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def manage_backups(self, filename):
        """
        Verwalte die Backups für die angegebene Datei.

        Diese Methode erstellt Backups der Datei und verschiebt ältere
        Backups auf eine höhere Version (z.B. .bak1 wird zu .bak2).

        Parameters:
            filename (str): Der Pfad zur Datei, für die das Backup erstellt werden soll.
        """
        base_filename = os.path.basename(filename)
        backup1 = os.path.join(self.backup_dir, f"{base_filename}.bak1")
        backup2 = os.path.join(self.backup_dir, f"{base_filename}.bak2")
        backup3 = os.path.join(self.backup_dir, f"{base_filename}.bak3")

        if os.path.exists(backup3):
            os.remove(backup3)  # Entferne das älteste Backup
        if os.path.exists(backup2):
            os.rename(backup2, backup3)  # Verschiebe Backup2 nach Backup3
        if os.path.exists(backup1):
            os.rename(backup1, backup2)  # Verschiebe Backup1 nach Backup2
        if os.path.exists(filename):
            shutil.copy2(filename, backup1)  # Erstelle ein neues Backup

#EOF
