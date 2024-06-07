#Filename: file_manager.py

import sys
import os
import signal
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
from modules.logger import Logger
from modules.run import Run
from modules.server import ServerHandler

class FileManager:
    def __init__(self):
        self.logger = Logger().get_logger()
        self.files = {
            "Dockerfile": "Dockerfile",
            "docker-compose.yml": "docker-compose.yml",
            "manage": "manage.sh",
        }
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager, self.logger)
        self.run_instance = Run(self.logger)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.logger.info("Programm wurde beendet.")
        sys.exit(0)

    def send_signal_to_run(self, filename):
        self.logger.info(f"Signal an Run-Server wird gesendet: {filename}")
        self.run_instance.send_command(f'execute:{filename}')

    def run(self):
        try:
            if len(sys.argv) > 1:
                if '-h' in sys.argv or '--help' in sys.argv:
                    print_help()
                elif '-r' in sys.argv:
                    filename_index = sys.argv.index('-r') + 1
                    if filename_index < len(sys.argv):
                        program_to_run = sys.argv[filename_index]
                        self.run_instance.receive_commands(program_to_run)
                    else:
                        self.logger.error("Kein Programm angegeben. Verwenden Sie das Format 'python3 main.py -r <program>'")
                        sys.exit(1)
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
                        self.file_operations.edit_file(filename)
                        self.send_signal_to_run(filename)  # Signal an die Run-Instanz senden
                        self.logger.info("Warten auf weitere Eingaben...")
                    else:
                        self.logger.error("Kein Dateiname angegeben. Verwenden Sie die Option -d, um einen Dateinamen anzugeben.")
                        print_help()
            else:
                
                while True:
                    self.logger.info("Bitte geben Sie den neuen Inhalt ein:")

                    line = self.file_operations.read_input()
                    if line is None:
                        break

                    if line.startswith("Filename: ") or line.startswith("# Filename: "):
                        keyword = line.split("Filename: ")[1].strip()
                    else:
                        self.logger.error("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
                        continue

                    if keyword in self.files:
                        filename = self.files[keyword]
                        self.file_operations.edit_file(filename)
                        self.send_signal_to_run(filename)  # Signal an die Run-Instanz senden
                        
                        self.logger.info("Warten auf weitere Eingaben...")
                        
                    else:
                        self.logger.error("Ungültiges Format. Bitte geben Sie den Dateinamen im Format 'Filename: dateiname' oder '# Filename: dateiname' ein.")
        except KeyboardInterrupt:
            self.logger.info("Programm wurde beendet.")
            sys.exit(0)
