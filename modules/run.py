# Filename: modules/run.py

import signal
import sys
import threading
import os
from modules.client import Client
from modules.message import Message

class Run:
    def __init__(self, args, host, port, client_id="run"):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server_address = (host, port)
        self.running = True
        self.client = Client(host, port, client_id)
        self.client.register()
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_thread.daemon = True
        self.message_thread.start()

    def signal_handler(self, sig, frame):
        print("Run wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def handle_message(self, message):
        print("Nachricht erhalten")  # Debugging output
        data = Message.deserialize(message)
        print(f"Empfangene Nachricht: {data}")  # Debugging output

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
        while self.running:
            try:
                print("Warte auf Nachrichten...")  # Debugging output
                message = self.client.listener_socket.recv()
                self.handle_message(message)
                self.client.listener_socket.send(Message("server", self.client.client_id, Message.RESPONSE, "Message received").serialize())
            except Exception as e:
                print(f"Fehler beim Empfangen der Nachricht: {e}")

    def start(self):
        print("Run client started and waiting for commands...")
        self.receive_messages()

#EOF
