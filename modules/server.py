import socket
import sys
import os

class ServerHandler:
    def __init__(self):
        self.server_address = ('localhost', 65433)

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                s.sendall(command.encode('utf-8'))
                print(f"Befehl gesendet: {command}")
        except ConnectionRefusedError:
            print("Verbindung zum Server fehlgeschlagen. Bitte stellen Sie sicher, dass der Server läuft.")

    def run_mode(self, program_to_run):
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
                            os.system(f'python3 {program_to_run} {filename}')
                        if command == 'exit':
                            print("Server wird beendet.")
                            server_socket.close()
                            sys.exit(0)
            except KeyboardInterrupt:
                print("Server wird durch Strg+C beendet.")
                server_socket.close()
                sys.exit(0)
