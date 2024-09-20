# Filename: modules/run.py

import signal
import sys
import threading
import os
from modules.client import Client
from modules.message import Message

class Run:
    """
    Klasse zur Ausführung eines Clients, der mit einem Server kommuniziert.

    Diese Klasse ermöglicht das Empfangen von Befehlen über einen Client
    und deren Ausführung im System.

    Attributes:
        server_address (tuple): Die Adresse des Servers (Host, Port).
        running (bool): Status, ob der Client aktiv ist oder nicht.
        client_id (str): Die ID des Clients.
        client (Client): Die Instanz des Clients zur Kommunikation mit dem Server.
        message_thread (threading.Thread): Der Thread zum Empfangen von Nachrichten.
    """

    def __init__(self, args, host, port, client_id):
        """
        Initialisiert die Run-Klasse und registriert den Client.

        Parameters:
            args: Die übergebenen Argumente.
            host (str): Der Hostname des Servers.
            port (int): Der Port, auf dem der Server lauscht.
            client_id (str): Die ID des Clients.
        """
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server_address = (host, port)
        self.running = True
        self.client_id = client_id
        self.client = Client(host, port, self.client_id)
        self.client.register()
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_thread.daemon = True
        self.message_thread.start()

    def signal_handler(self, sig, frame):
        """
        Behandelt das Signal für Strg+C, um den Client zu beenden.

        Parameters:
            sig: Das empfangene Signal.
            frame: Der aktuelle Stack-Frame.
        """
        print("Run wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def handle_message(self, message):
        """
        Verarbeitet die empfangene Nachricht.

        Parameters:
            message (bytes): Die empfangene serialisierte Nachricht.
        """
        data = Message.deserialize(message)

        if data.message_type == Message.SEND:
            command = data.content
            print(f"Empfangener Befehl: {command}")
            filename = command.split()[1] if len(command.split()) > 1 else None
            if filename and os.path.exists(filename):
                os.system(command)
            else:
                print(f"Datei {filename} existiert nicht.")
        elif data.message_type == Message.RESPONSE:
            print(f"Nachricht: {data.content}")

    def receive_messages(self):
        """
        Wartet auf eingehende Nachrichten und verarbeitet diese.
        """
        while self.running:
            try:
                msg_obj = self.client.receive_message()
                if msg_obj:
                    self.handle_message(msg_obj.serialize())
            except Exception as e:
                print(f"Fehler beim Empfangen der Nachricht: {e}")

    def start(self):
        """
        Startet den Run-Client und wartet auf Befehle.
        """
        print("Run client started and waiting for commands...")
        self.receive_messages()

#EOF
