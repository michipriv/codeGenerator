#Filename: run.py

import socket
import signal
import os
import sys

class Run:
    def __init__(self, logger):
        self.logger = logger
        self.server_address = ('localhost', 65433)
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        self.logger.info("Run wird durch Strg+C beendet.")
        sys.exit(0)

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                s.sendall(command.encode('utf-8'))
                self.logger.info(f"Befehl gesendet: {command}")
        except ConnectionRefusedError:
            self.logger.error("Verbindung zum Server fehlgeschlagen. Bitte stellen Sie sicher, dass der Server läuft.")

    def receive_commands(self, program_to_run):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.server_address)
        server_socket.listen(1)
        self.logger.info(f"Warten auf Verbindungen zum Ausführen von {program_to_run}...")

        while True:
            try:
                conn, addr = server_socket.accept()
                with conn:
                    self.logger.info(f'Verbunden mit {addr}')
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8')
                        self.logger.info(f"Befehl empfangen: {command}")
                        if command.startswith('execute:'):
                            filename = command.split(':')[1]
                            os.system(f'python3 {program_to_run} {filename}')
                        if command == 'exit':
                            self.logger.info("Server wird beendet.")
                            server_socket.close()
                            sys.exit(0)
            except KeyboardInterrupt:
                self.logger.info("Server wird durch Strg+C beendet.")
                server_socket.close()
                sys.exit(0)
