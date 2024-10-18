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

    def __init__(self, host: str, port: int, client_id: str):
        """
        Initialisiert die Client-Klasse und erstellt die ZMQ-Sockets für die
        Kommunikation mit dem Server.

        :param host: Der Hostname des Servers.
        :param port: Der Port des Servers.
        :param client_id: Die eindeutige ID des Clients.
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

    def generate_unique_port(self) -> int:
        """
        Generiert einen einzigartigen Port für den Client, indem ein verfügbarer Port
        im Bereich von 1024 bis 65535 ausgewählt wird.

        :return: Ein verfügbarer Port für den Client.
        """
        while True:
            unique_port = random.randint(1024, 65535)
            if self.is_port_available(unique_port):
                return unique_port

    def is_port_available(self, port: int) -> bool:
        """
        Überprüft, ob ein gegebener Port verfügbar ist.

        :param port: Der zu überprüfende Port.
        :return: True, wenn der Port verfügbar ist, sonst False.
        """
        with zmq.Context.instance().socket(zmq.REQ) as socket:
            try:
                socket.bind(f"tcp://{self.host}:{port}")
                socket.unbind(f"tcp://{self.host}:{port}")
                return True
            except zmq.ZMQError:
                return False

    def register(self) -> None:
        """
        Registriert den Client beim Server, indem eine Registrierungsnachricht an den Server gesendet wird.
        Wartet auf eine Bestätigung vom Server.

        :return: None
        """
        unique_port = self.unique_port
        msg = Message("server", self.client_id, Message.REGISTER, f"tcp://{self.host}:{unique_port}")
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Client {self.client_id} registered with port {unique_port}.")
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

    def receive_message(self) -> Message:
        """
        Empfängt eine Nachricht vom Listener-Socket.

        :return: Das empfangene Message-Objekt.
        :raises Exception: Wenn ein Fehler beim Empfangen der Nachricht auftritt.
        """
        try:
            message = self.listener_socket.recv()
            msg_obj = Message.deserialize(message)
            self.listener_socket.send(Message("server", self.client_id, Message.RESPONSE, "Message received").serialize())
            return msg_obj
        except Exception as e:
            raise Exception(f"Error while receiving messages: {e}")

    def send_message(self, recipient: str, sender: str, message_type: str, content: str) -> None:
        """
        Sendet eine Nachricht an den Server.

        :param recipient: Der Empfänger der Nachricht.
        :param sender: Der Absender der Nachricht.
        :param message_type: Der Typ der Nachricht.
        :param content: Der Inhalt der Nachricht.
        :return: None
        """
        if message_type not in [Message.REGISTER, Message.SEND, Message.RESPONSE]:
            message_type = Message.UNKNOWN
        msg = Message(recipient, sender, message_type, content)
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

#EOF
