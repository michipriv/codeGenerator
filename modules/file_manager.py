# Filename: modules/file_manager.py

import socket
import signal
import sys
import re
import termios  # Terminal I/O control
import tty  # Terminal control
import threading
import os
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
import time

class FileManager:
    def __init__(self, args, host, port, main_filename):
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.args = args
        self.server_address = (host, port)
        self.running = True
        self.main_filename = main_filename
        self.current_code = ""
        self.message_thread = None
        self.openai_message = ""
        self.old_settings = termios.tcgetattr(sys.stdin.fileno())  # Alte Terminaleinstellungen speichern
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("\nStrg+C erkannt, beende das Programm...")
        self.running = False
        if self.message_thread and self.message_thread.is_alive():
            self.message_thread.join(1)
        self.reset_terminal()
        os._exit(0)

    def reset_terminal(self):
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
        print("\nTerminal wurde zurückgesetzt.")

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def receive_messages(self):
        print("Nachrichtenempfangs-Thread gestartet.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.settimeout(1.0)  # Setzt einen Timeout von 1 Sekunde für den recv-Aufruf
            s.sendall(b'register:file_manager')
            print("FileManager beim Server registriert.")
            
            while self.running:
                try:
                    data = s.recv(1024)
                    if data:
                        message = data.decode('utf-8')
                        if message.startswith("save:"):
                            self.save_received_code(message[len("save:"):].strip())
                        elif message.startswith("delete_file:"):
                            self.file_operations.delete_file(message[len("delete_file:"):].strip())
                        elif message.startswith("delete_directory:"):
                            self.file_operations.delete_directory(message[len("delete_directory:"):].strip())
                        self.send_message('message:server:Nachricht von Openai')
                except socket.timeout:
                    pass  # Timeout tritt nach 1 Sekunde auf, und der Loop geht weiter
                except socket.error as e:
                    if not self.running:
                        break
                    print("Socket-Fehler beim Empfangen der Nachricht:", e)
                    break
                except Exception as e:
                    print("Allgemeiner Fehler beim Empfangen der Nachricht:", e)
                    break
            
            print("Nachrichtenempfangs-Thread beendet.")
            self.reset_terminal()

    def format_code(self, code):
        try:
            import black
            formatted_code = black.format_str(code, mode=black.Mode())
            return formatted_code
        except ImportError:
            print("Fehler: Das Modul 'black' ist nicht installiert. Der Code wird unformatiert gespeichert.")
            return code
        except black.InvalidInput:
            print("Fehler: Der Code konnte nicht formatiert werden. Der Code wird unformatiert gespeichert.")
            return code
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return code

    def save_received_code(self, code):
        print("Original empfangener Code:")
        print(code)
        self.current_code = self.format_code(code)
        print("Formatierter Code:")
        print(self.current_code)
        filename = self.extract_filename(self.current_code)
        if filename:
            self.file_operations.save_file(filename, self.current_code)
            print(f"Empfangener Code in Datei {filename} gespeichert.")
        else:
            print("Kein gültiger Dateiname im empfangenen Code gefunden.")

    def register_with_server(self):
        self.send_message('register:file_manager')
        print("FileManager beim Server registriert.")

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
            while self.running:
                ch = sys.stdin.read(1)
                if ch == '\x04':  # Ctrl+D
                    print("\nStrg+D erkannt, speichere den Code...")
                    original_code = '\n'.join(code_lines)
                    print("Original eingegebener Code:")
                    print(original_code)
                    formatted_code = self.format_code(original_code)
                    print("Formatierter Code:")
                    print(formatted_code)
                    return formatted_code, 'save_only'
                elif ch == '\x06':  # Ctrl+F
                    print("\nStrg+F erkannt, speichere den Code und führe ihn aus...")
                    original_code = '\n'.join(code_lines)
                    print("Original eingegebener Code:")
                    print(original_code)
                    formatted_code = self.format_code(original_code)
                    print("Formatierter Code:")
                    print(formatted_code)
                    return formatted_code, 'save_and_send'
                elif ch == '\x03':  # Ctrl+C
                    print("\nStrg+C erkannt, beende das Programm...")
                    self.signal_handler(signal.SIGINT, None)
                    return None, None
                elif ch in ['\r', '\n']:  # Enter
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
            
            # Starte einen Thread, um Nachrichten vom Server zu empfangen
            self.message_thread = threading.Thread(target=self.receive_messages)
            self.message_thread.start()
            print(f"Nachrichtenempfangs-Thread gestartet: {self.message_thread.is_alive()}")

            while self.running:
                self.current_code, action = self.read_input()
                if not self.running:
                    break
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
        finally:
            self.running = False
            if self.message_thread:
                self.message_thread.join(1)
            self.reset_terminal()
            print("FileManager beendet.")

#EOF
