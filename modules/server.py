#Filename: server.py

"""

Klassen die unterienander kommunizieren müssen sich am server registrieren
self.send_message('register:file_manager')
self.send_message('register:run')


senden von nachrichten:
self.send_message('message:run:execute:filename.py')

run ist die client id
execut ist der befehl an die run klasse



"""

import socket
import threading
import signal

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
        print(f"Server-Handler initialisiert auf {self.server_address}")

    def signal_handler(self, sig, frame):
        print("Server wird durch Strg+C beendet.")
        self.running = False
        self.stop()

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

    def handle_client(self, conn):
        with conn:
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    print(f"Nachricht empfangen: {message}")
                    self.route_message(message, conn)
                except socket.error:
                    break

    def route_message(self, message, conn):
        if message.startswith('register:'):
            client_id = message.split(':')[1]
            clients[client_id] = conn
            conn.sendall(b'Registrierung erfolgreich')
        elif message.startswith('message:'):
            _, to_client, content = message.split(':', 2)
            if to_client in clients:
                clients[to_client].sendall(content.encode('utf-8'))
            else:
                conn.sendall(b'Client nicht gefunden')

    def stop(self):
        self.running = False
        self.server_socket.close()
        for conn in clients.values():
            conn.close()
