import sys
import os
import signal

# Absoluten Pfad des aktuellen Verzeichnisses und des 'modules'-Verzeichnisses hinzufügen
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'modules'))

from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
from modules.utils import clear_screen, print_help

class FileManager:
    def __init__(self):
        self.files = {
            "Dockerfile": "Dockerfile",
            "docker-compose.yml": "docker-compose.yml",
            "manage": "manage.sh",
        }
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("\nProgramm wurde beendet.")
        sys.exit(0)

    def run(self):
        try:
            if len(sys.argv) > 1:
                if '-h' in sys.argv or '--help' in sys.argv:
                    print_help()
                else:
                    filename = None
                    program_to_execute = None

                    if '-d' in sys.argv:
                        filename_index = sys.argv.index('-d') + 1
                        if filename_index < len(sys.argv):
                            filename = sys.argv[filename_index]

                    if '-p' in sys.argv:
                        program_index = sys.argv.index('-p') + 1
                        if program_index < len(sys.argv):
                            program_to_execute = sys.argv[program_index]

                    if filename:
                        while True:
                            self.file_operations.edit_file(filename, program_to_execute)
                    else:
                        print("Fehler: Kein Dateiname angegeben. Verwenden Sie die Option -d, um einen Dateinamen anzugeben.")
                        print_help()
            else:
                while True:
                    print("Bitte geben Sie den neuen Inhalt ein:")

                    line = self.file_operations.read_input()
                    if line is None:
                        break

                    if line.startswith("Filename: ") or line.startswith("# Filename: "):
                        keyword = line.split("Filename: ")[1].strip()
                    else:
                        print("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
                        continue

                    if keyword in self.files:
                        filename = self.files[keyword]
                        self.file_operations.edit_file(filename)
                    else:
                        print("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")
            sys.exit(0)


if __name__ == "__main__":
    clear_screen()
    file_manager = FileManager()
    file_manager.run()
