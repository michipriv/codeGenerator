# Filename: modules/server.py

import zmq
import sys
from .message import Message

class ServerHandler:
    """
    Klasse zur Verwaltung eines ZMQ-Servers.

    Diese Klasse ermöglicht das Empfangen von Nachrichten von Clients,
    die Verarbeitung dieser Nachrichten und das Senden von Antworten.

    Attributes:
        host (str): Der Hostname des Servers.
        port (int): Der Port, auf dem der Server lauscht.
        context (zmq.Context): Der ZMQ-Kontext.
        socket (zmq.REP): Der ZMQ-Socket, der für den Empfang von Nachrichten verwendet wird.
        clients (dict): Ein Dictionary zur Speicherung der registrierten Clients.
    """

    def __init__(self, host, port):
        """
        Initialisiert die ServerHandler-Klasse.

        Parameters:
            host (str): Der Hostname des Servers.
            port (int): Der Port, auf dem der Server lauscht.
        """
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.clients = {}

    def start_server(self):
        """
        Startet den Server und wartet auf eingehende Nachrichten.
        """
        print(f"Server started at {self.host}:{self.port}")
        try:
            while True:
                message = self.socket.recv()
                msg_obj = Message.deserialize(message)
                print(f"Received message from {msg_obj.sender}: {msg_obj.content}")

                # Verarbeite die Nachricht und sende eine Antwort
                reply = self.process_message(msg_obj)
                self.socket.send(reply.serialize())
        except KeyboardInterrupt:
            self.shutdown_server()

    def process_message(self, message):
        """
        Verarbeitet die empfangene Nachricht und gibt eine Antwort zurück.

        Parameters:
            message (Message): Die empfangene Nachricht.

        Returns:
            Message: Die Antwortnachricht.
        """
        if message.message_type == Message.REGISTER:
            self.clients[message.sender] = message.content
            return Message(message.sender, "server", Message.RESPONSE, "Registration successful")
        elif message.message_type == Message.SEND:
            recipient = message.recipient
            if recipient in self.clients:
                recipient_address = self.clients[recipient]
                self.send_to_client(recipient_address, message)
                return Message(message.sender, "server", Message.RESPONSE, f"Message sent to {recipient}")
            else:
                return Message(message.sender, "server", Message.RESPONSE, f"Recipient {recipient} not found")
        else:
            return Message(message.sender, "server", Message.RESPONSE, "Unknown message type")

    def send_to_client(self, address, message):
        """
        Sendet eine Nachricht an den angegebenen Client.

        Parameters:
            address (str): Die Adresse des Clients.
            message (Message): Die zu sendende Nachricht.
        """
        client_socket = self.context.socket(zmq.REQ)
        client_socket.connect(address)
        client_socket.send(message.serialize())
        client_socket.recv()
        client_socket.close()

    def signal_handler(self, sig, frame):
        """
        Behandelt das Signal zum Beenden des Servers.

        Parameters:
            sig: Das empfangene Signal.
            frame: Der aktuelle Stack-Frame.
        """
        print("Shutting down server...")
        self.shutdown_server()
        sys.exit(0)

    def shutdown_server(self):
        """
        Schließt den Server und gibt Ressourcen frei.
        """
        self.socket.close()
        self.context.term()

#EOF
