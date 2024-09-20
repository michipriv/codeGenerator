# Filename: modules/client.py

import zmq
import hashlib
import random
from modules.message import Message

class Client:
    """
    Klasse zur Kommunikation mit einem ZMQ-Server.

    Diese Klasse verwaltet die Verbindung zu einem Server, registriert den Client
    und ermöglicht das Senden und Empfangen von Nachrichten.

    Attributes:
        host (str): Der Hostname des Servers.
        port (int): Der Port des Servers.
        client_id (str): Die eindeutige ID des Clients.
        context: Der ZMQ-Kontext.
        server_socket: Socket zum Senden von Nachrichten an den Server.
        unique_port (int): Einzigartiger Port für den Client.
        listener_socket: Socket zum Empfangen von Nachrichten.
    """

    def __init__(self, host, port, client_id):
        """
        Initialisiert die Client-Klasse.

        Parameters:
            host (str): Der Hostname des Servers.
            port (int): Der Port des Servers.
            client_id (str): Die eindeutige ID des Clients.
        """
        self.host = host
        self.port = port
        self.client_id = client_id
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect(f"tcp://{self.host}:{self.port}")

        # Generiere einen einzigartigen Port für den Client
        self.unique_port = self.generate_unique_port()
        self.listener_socket = self.context.socket(zmq.REP)
        self.listener_socket.bind(f"tcp://{self.host}:{self.unique_port}")

    def generate_unique_port(self):
        """
        Generiert einen einzigartigen Port für den Client.

        Returns:
            int: Ein verfügbarer Port für den Client.
        """
        while True:
            unique_port = random.randint(1024, 65535)  # Wähle eine zufällige Portnummer im Bereich 1024-65535
            if self.is_port_available(unique_port):
                return unique_port

    def is_port_available(self, port):
        """
        Überprüft, ob ein gegebener Port verfügbar ist.

        Parameters:
            port (int): Der zu überprüfende Port.

        Returns:
            bool: True, wenn der Port verfügbar ist, sonst False.
        """
        with zmq.Context.instance().socket(zmq.REQ) as socket:
            try:
                socket.bind(f"tcp://{self.host}:{port}")
                socket.unbind(f"tcp://{self.host}:{port}")
                return True
            except zmq.ZMQError:
                return False

    def register(self):
        """
        Registriert den Client beim Server.

        Sendet eine Registrierungsnachricht an den Server und wartet auf eine Antwort.
        """
        unique_port = self.unique_port
        msg = Message("server", self.client_id, Message.REGISTER, f"tcp://{self.host}:{unique_port}")
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Client {self.client_id} registered with port {unique_port}.")
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

    def receive_message(self):
        """
        Empfängt eine Nachricht vom Listener-Socket.

        Returns:
            Message: Das empfangene Message-Objekt.

        Raises:
            Exception: Wenn ein Fehler beim Empfangen der Nachricht auftritt.
        """
        try:
            message = self.listener_socket.recv()
            msg_obj = Message.deserialize(message)
            self.listener_socket.send(Message("server", self.client_id, Message.RESPONSE, "Message received").serialize())
            return msg_obj
        except Exception as e:
            raise Exception(f"Error while receiving messages: {e}")

    def send_message(self, recipient, sender, message_type, content):
        """
        Sendet eine Nachricht an den Server.

        Parameters:
            recipient (str): Der Empfänger der Nachricht.
            sender (str): Der Absender der Nachricht.
            message_type (str): Der Typ der Nachricht.
            content (str): Der Inhalt der Nachricht.
        """
        if message_type not in [Message.REGISTER, Message.SEND, Message.RESPONSE]:
            message_type = Message.UNKNOWN
        msg = Message(recipient, sender, message_type, content)
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

#EOF
