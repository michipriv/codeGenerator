# Filename: modules/server.py

import zmq
import sys
from .message import Message

class ServerHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.clients = {}

    def start_server(self):
        print(f"Server started at {self.host}:{self.port}")
        try:
            while True:
                message = self.socket.recv()
                msg_obj = Message.deserialize(message)
                print(f"Received message from {msg_obj.sender}: {msg_obj.content}")

                # Process the message and send a reply
                reply = self.process_message(msg_obj)
                self.socket.send(reply.serialize())
        except KeyboardInterrupt:
            self.shutdown_server()

    def process_message(self, message):
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
        client_socket = self.context.socket(zmq.REQ)
        client_socket.connect(address)
        client_socket.send(message.serialize())
        client_socket.recv()
        client_socket.close()

    def signal_handler(self, sig, frame):
        print("Shutting down server...")
        self.shutdown_server()
        sys.exit(0)

    def shutdown_server(self):
        self.socket.close()
        self.context.term()

#EOF
