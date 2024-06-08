import sys
import os
import signal
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
from modules.server import ServerHandler

class FileManager:
    def __init__(self, args):
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.args = args
        self.server_handler = ServerHandler()
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("Programm wurde beendet.")
        sys.exit(0)

    def send_signal_to_run(self, filename):
        print(f"Signal an Server wird gesendet: {filename}")
        self.server_handler.send_command(f'execute:{filename}')

    def run(self):
        try:
            while True:
                if self.args.help:
                    self.args.print_help()
                    break
                elif self.args.edit_filename:
                    self.file_operations.edit_file(self.args.edit_filename)
                    self.send_signal_to_run(self.args.edit_filename)
                    print("Warten auf weitere Eingaben...")
                else:
                    print("Interaktiver Modus. Bitte geben Sie den Dateinamen ein:")
                    while True:
                        line = self.file_operations.read_input()
                        if line is None:
                            print("Keine Eingabe erkannt. Bitte erneut versuchen.")
                            continue  # Fortsetzen, um erneut auf Eingaben zu warten

                        filename = line.strip()
                        if filename:
                            self.file_operations.edit_file(filename)
                            self.send_signal_to_run(filename)
                            print("Warten auf weitere Eingaben...")
                        else:
                            print("Ungültige Eingabe. Bitte geben Sie einen Dateinamen ein.")
        except KeyboardInterrupt:
            print("Programm wurde beendet.")
            sys.exit(0)
