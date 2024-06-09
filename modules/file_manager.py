# Filename: file_manager.py

import socket
import signal
import sys
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager

class FileManager:
    def __init__(self, args, host, port):
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.args = args
        self.server_address = (host, port)
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("FileManager wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                s.sendall(b'register:file_manager')
                response = s.recv(1024).decode('utf-8')
                print(f"Antwort vom Server: {response}")
            while self.running:
                try:
                    if self.args.edit_filename:
                        self.file_operations.edit_file(self.args.edit_filename)
                        # Benachrichtige den Run-Client über die bearbeitete Datei
                        self.send_message(f'message:run:execute:{self.args.edit_filename}')
                        
                        

                except EOFError:
                    print("EOFError erkannt. Wiederholen der Eingabe...")
                    continue
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
