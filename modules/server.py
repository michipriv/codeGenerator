#Filename: server.py

import socket
import sys
import os

class ServerHandler:
    def __init__(self, logger):
        self.logger = logger

    def run_mode(self, program_to_run):
        # Einfache Server-Implementierung zur Kommunikation
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 65433))
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
