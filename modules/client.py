# Filename: modules/client.py

import zmq
import hashlib
import random
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
        self.unique_port = self.generate_unique_port()
        self.listener_socket = self.context.socket(zmq.REP)
        self.listener_socket.bind(f"tcp://{self.host}:{self.unique_port}")

    def generate_unique_port(self):
        while True:
            unique_port = random.randint(1024, 65535)  # Get a random port number in the range 1024-65535
            if self.is_port_available(unique_port):
                return unique_port

    def is_port_available(self, port):
        with zmq.Context.instance().socket(zmq.REQ) as socket:
            try:
                socket.bind(f"tcp://{self.host}:{port}")
                socket.unbind(f"tcp://{self.host}:{port}")
                return True
            except zmq.ZMQError:
                return False

    def register(self):
        unique_port = self.unique_port
        msg = Message("server", self.client_id, Message.REGISTER, f"tcp://{self.host}:{unique_port}")
        self.server_socket.send(msg.serialize())
        reply = self.server_socket.recv()
        reply_msg = Message.deserialize(reply)
        print(f"Client {self.client_id} registered with port {unique_port}.")
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
