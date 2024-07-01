# Filename: file_manager.py

import socket
import signal
import sys
import re
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager

class FileManager:
    def __init__(self, args, host, port, main_filename):
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.args = args
        self.server_address = (host, port)
        self.running = True
        self.main_filename = main_filename
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("FileManager wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def extract_filename(self, code):
        match = re.search(r'# ?[Ff]ilename: (.+)', code)
        if match:
            return match.group(1).strip()
        return None

    def run(self):
        try:
            while self.running:
                try:
                    print("Bitte fügen Sie den Code ein (Ende mit Strg+D):")
                    code_lines = []
                    while True:
                        try:
                            line = input()
                            code_lines.append(line)
                        except EOFError:
                            break

                    if code_lines:
                        code = '\n'.join(code_lines)
                        filename = self.extract_filename(code)
                        if filename:
                            self.file_operations.save_file(filename, code)
                            self.send_message(f'message:run:execute:{self.main_filename}')
                        else:
                            print("Kein gültiger Dateiname gefunden.")
                    else:
                        print("Kein Code eingegeben.")
                except EOFError:
                    print("EOFError erkannt. Wiederholen der Eingabe...")
                    continue
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
