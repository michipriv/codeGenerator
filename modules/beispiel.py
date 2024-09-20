# Filename: modules/beispiel.py
# Beispielklasse um Nachrichten zu empfangen und zu senden
# Empfang wird in einem eigenen Thread gestartet
# send_message ist hier interaktiv gestaltet

import threading
from modules.client import Client
from modules.message import Message

class ExampleClient:
    """
    Beispielklasse zum Senden und Empfangen von Nachrichten.

    Diese Klasse ermöglicht es, Nachrichten an einen Server zu senden und
    empfangene Nachrichten in einem separaten Thread zu verarbeiten.

    Attributes:
        client_id (str): Die ID des Clients.
        client (Client): Die Client-Instanz zur Kommunikation mit dem Server.
        running (bool): Gibt an, ob der Client aktiv ist.
    """

    def __init__(self, host, port, client_id):
        """
        Initialisiert die ExampleClient-Klasse.

        Parameters:
            host (str): Der Hostname des Servers.
            port (int): Der Port des Servers.
            client_id (str): Die eindeutige ID des Clients.
        """
        self.client_id = client_id
        self.client = Client(host, port, client_id)
        self.client.register()
        self.running = True

    def start_receiving(self):
        """
        Wartet auf eingehende Nachrichten und verarbeitet diese.
        """
        while self.running:
            try:
                msg_obj = self.client.receive_message()
                if msg_obj:
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
            except Exception as e:
                print(f"Error while receiving messages: {e}")

    def send_message_input(self):
        """
        Ermöglicht dem Benutzer das Senden von Nachrichten an einen Empfänger.
        """
        print(f"Client {self.client_id} started. You can send messages now.")
        
        while self.running:
            try:
                recipient = input("Enter recipient id: ")
                message_type = "send"
                content = input("Enter message content: ")
                self.client.send_message(recipient, self.client_id, message_type, content)
            except Exception as e:
                print(f"Error while sending message: {e}")

    def run(self):
        """
        Startet den Empfangsthread und die Eingabeaufforderung zum Senden von Nachrichten.
        """
        recv_thread = threading.Thread(target=self.start_receiving)
        recv_thread.daemon = True
        recv_thread.start()

        try:
            self.send_message_input()
        except KeyboardInterrupt:
            self.running = False
            recv_thread.join()

#EOF
