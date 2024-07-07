# Filename: modules/server.py

"""
Klassen die untereinander kommunizieren müssen sich am server registrieren

self.send_message('register:file_manager')
self.send_message('register:run')

Senden von Nachrichten:
self.send_message('message:run:execute:filename.py')


run ist die client ID
execute ist der Befehl an die run Klasse
"""

import socket
import threading
import signal
import sys

clients = {}

class ServerHandler(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.settimeout(1)  # Setzt ein Timeout für den Server-Socket
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        self._bind_socket()
        #print(f"Server-Handler initialisiert auf {self.server_address}")

    def signal_handler(self, sig, frame):
        print("Server wird durch Strg+C beendet.")
        self.running = False
        self.stop()
        sys.exit(0)

    def _bind_socket(self):
        try:
            self.server_socket.bind(self.server_address)
            self.server_socket.listen(5)
            self.server_address = self.server_socket.getsockname()
            with open('server_port.txt', 'w') as f:
                f.write(str(self.server_address[1]))
            print(f"Socket gebunden an {self.server_address}")
        except OSError as e:
            if e.errno == 98:
                print(f"Adresse {self.server_address} wird bereits verwendet. Bitte verwenden Sie eine andere.")
                self.running = False

    def run(self):
        if not self.running:
            return
        print(f"Server läuft auf {self.server_address}")
        self.register_self()
        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                if not self.running:
                    conn.close()
                    break
                print(f"Verbindung von {addr} erhalten")
                threading.Thread(target=self.handle_client, args=(conn,)).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def register_self(self):
        clients['server'] = self.server_socket
        print("Server registriert mit ID 'server'")

    def handle_client(self, conn):
        with conn:
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    
                    # Anzeigen, dass eine Nachricht empfangen wurde
                    if message.startswith('message:'):
                        parts = message.split(':')
                        if len(parts) > 2:
                            sender = parts[1]
                            print(f"Nachricht für {sender} empfangen")
                    
                    self.route_message(message, conn)
                except socket.error:
                    break
    
    
    def route_message(self, message, conn):
        if message.startswith('register:'):
            client_id = message.split(':')[1]
            clients[client_id] = conn
            conn.sendall(b'Registrierung erfolgreich')
            print(f"Client registriert: {client_id}")  # Debug-Ausgabe
        elif message.startswith('message:'):
            _, to_client, content = message.split(':', 2)
            print(f"Nachricht erhalten für {to_client}: {content}")  # Debug-Ausgabe
            if to_client in clients:
                clients[to_client].sendall(content.encode('utf-8'))
                print(f"Nachricht weitergeleitet an {to_client}")  # Debug-Ausgabe
            else:
                conn.sendall(b'Client nicht gefunden')
                print(f"Client {to_client} nicht gefunden")  # Debug-Ausgabe


    def stop(self):
        self.running = False
        self.server_socket.close()
        for conn in clients.values():
            conn.close()



#EOF
