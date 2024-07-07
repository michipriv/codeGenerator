#Filename: modules/backup_manager.py

import os
import shutil

class BackupManager:
    def __init__(self, backup_dir='bak'):
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def manage_backups(self, filename):
        base_filename = os.path.basename(filename)
        backup1 = os.path.join(self.backup_dir, f"{base_filename}.bak1")
        backup2 = os.path.join(self.backup_dir, f"{base_filename}.bak2")
        backup3 = os.path.join(self.backup_dir, f"{base_filename}.bak3")

        if os.path.exists(backup3):
            os.remove(backup3)
        if os.path.exists(backup2):
            os.rename(backup2, backup3)
        if os.path.exists(backup1):
            os.rename(backup1, backup2)
        if os.path.exists(filename):
            shutil.copy2(filename, backup1)



#EOF
