# Filename: modules/beispiel.py
# Beispielklasse um Nachrichten zu empfangen und zu senden
# Empfang wird in einem eigenen Thread gestartet
# send_message ist hier interaktiv gestaltet

import threading
from modules.client import Client
from modules.message import Message

class ExampleClient:
    def __init__(self, host, port, client_id):
        self.client_id = client_id
        self.client = Client(host, port, client_id)
        self.client.register()
        self.running = True

    def start_receiving(self):
        while self.running:
            try:
                msg_obj = self.client.receive_message()
                if msg_obj:
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
            except Exception as e:
                print(f"Error while receiving messages: {e}")

    def send_message_input(self):
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
        recv_thread = threading.Thread(target=self.start_receiving)
        recv_thread.daemon = True
        recv_thread.start()

        try:
            self.send_message_input()
            
            # Beispiel Aufruf von send_message
            recipient_id = "server"
            sender_id = self.client_id
            message_type = "send"
            content = "This is an example message content."
            self.client.send_message(recipient_id, sender_id, message_type, content)
            
            
            
        except KeyboardInterrupt:
            self.running = False
            recv_thread.join()

#EOF
