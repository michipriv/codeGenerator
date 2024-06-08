import socket
import signal
import os
import sys
from modules.logger import Logger

class Run:
    def __init__(self, log_file='run.log'):
        self.logger = Logger(log_file).get_logger()
        self.server_address = ('localhost', 65433)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.log_file = log_file

    def signal_handler(self, sig, frame):
        print("Run wird durch Strg+C beendet.")
        sys.exit(0)

    def receive_commands(self, program_to_run):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.server_address)
        server_socket.listen(1)
        print(f"Warten auf Verbindungen zum Ausführen von {program_to_run}...")

        while True:
            try:
                conn, addr = server_socket.accept()
                with conn:
                    print(f'Verbunden mit {addr}')
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8')
                        print(f"Befehl empfangen: {command}")
                        if command.startswith('execute:'):
                            filename = command.split(':')[1]
                            if os.path.exists(filename):
                                os.system(f'python3 {program_to_run} {filename} 2>&1 | tee -a {self.log_file}')
                            else:
                                print(f"Datei {filename} existiert nicht.")
                        if command == 'exit':
                            print("Server wird beendet.")
                            server_socket.close()
                            sys.exit(0)
            except KeyboardInterrupt:
                print("Server wird durch Strg+C beendet.")
                server_socket.close()
                sys.exit(0)
