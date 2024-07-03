# Filename: file_manager.py

import socket
import signal
import sys
import re
import termios  # Terminal I/O control
import tty  # Terminal control
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
        self.current_code = ""
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("\nStrg+C erkannt, beende das Programm...")
        self.running = False
        sys.exit(0)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def register_with_server(self):
        self.send_message('register:file_manager')

    def extract_filename(self, code):
        match = re.search(r'# ?[Ff]ilename: (.+)', code)
        if match:
            return match.group(1).strip()
        return None

    def save_code(self):
        filename = self.extract_filename(self.current_code)
        if filename:
            self.file_operations.save_file(filename, self.current_code)
            print(f"Datei {filename} wurde erfolgreich gespeichert.")
        else:
            print("Kein gültiger Dateiname gefunden.")

    def read_input(self):
        code_lines = []
        print("Bitte fügen Sie den Code ein (Ende mit Strg+D, Strg+F oder Strg+C):")
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)  # Setze Terminal in Rohmodus
            while True:
                ch = sys.stdin.read(1)
                if ch == '\x04':  # Ctrl+D
                    print("\nStrg+D erkannt, speichere den Code...")
                    return '\n'.join(code_lines), 'save_only'
                elif ch == '\x06':  # Ctrl+F
                    print("\nStrg+F erkannt, speichere den Code und führe ihn aus...")
                    return '\n'.join(code_lines), 'save_and_send'
                elif ch == '\x03':  # Ctrl+C
                    print("\nStrg+C erkannt, beende das Programm...")
                    self.signal_handler(signal.SIGINT, None)
                elif ch == '\r' or ch == '\n':  # Enter
                    code_lines.append('')
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                elif ch == '\x7f':  # Backspace
                    if code_lines and code_lines[-1]:
                        code_lines[-1] = code_lines[-1][:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    if len(code_lines) == 0:
                        code_lines.append(ch)
                    else:
                        code_lines[-1] += ch
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Terminal-Einstellungen wiederherstellen

    def run(self):
        try:
            # Registrieren Sie den FileManager beim Server
            self.register_with_server()
            while self.running:
                self.current_code, action = self.read_input()
                if action == 'save_only' and self.current_code:
                    self.save_code()
                elif action == 'save_and_send':
                    if self.current_code:
                        self.save_code()
                    self.send_message(f'message:run:execute:{self.main_filename}')
                else:
                    print("Kein Code eingegeben.")
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

