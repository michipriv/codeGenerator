# Filename: modules/client.py

import zmq
import hashlib
from modules.message import Message

class Client:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.context = zmq.Context()
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect(f"tcp://{self.host}:{self.port}")
        
        # Generate a unique port for the client
        unique_port = self.generate_unique_port(port, client_id)
        self.listener_socket = self.context.socket(zmq.REP)
        self.listener_socket.bind(f"tcp://{self.host}:{unique_port}")

    def generate_unique_port(self, base_port, client_id):
        hash_object = hashlib.md5(client_id.encode())
        unique_number = int(hash_object.hexdigest(), 16) % 10000  # Get a 4-digit unique number
        return base_port + 1 + unique_number

    def register(self):
        unique_port = self.generate_unique_port(self.port, self.client_id)
        msg = Message("server", self.client_id, Message.REGISTER, f"tcp://{self.host}:{unique_port}")
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

    def receive_message(self):
        try:
            message = self.listener_socket.recv()
            msg_obj = Message.deserialize(message)
            self.listener_socket.send(Message("server", self.client_id, Message.RESPONSE, "Message received").serialize())
            return msg_obj
        except Exception as e:
            raise Exception(f"Error while receiving messages: {e}")

    def send_message(self, recipient, sender, message_type, content):
        if message_type not in [Message.REGISTER, Message.SEND, Message.RESPONSE]:
            message_type = Message.UNKNOWN
        msg = Message(recipient, sender, message_type, content)
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Received reply from {reply_msg.sender}: {reply_msg.content}")

#EOF
