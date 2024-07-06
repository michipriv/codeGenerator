# Filename: utils.py

import os
import socket

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class TestMessenger:
    def __init__(self, host, port):
        self.server_address = (host, port)

    def send_message(self, message, target):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            full_message = f"message:{target}:{message}"
            s.sendall(full_message.encode('utf-8') )
        return 


#EOF