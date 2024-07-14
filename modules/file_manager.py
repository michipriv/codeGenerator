# Filename: modules/file_manager.py

import signal
import sys
import threading
import zmq
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
from modules.format_code import FormatCode
from modules.terminal import Terminal
from modules.client import Client
from modules.message import Message

class FileManager:
    def __init__(self, args, host, port, main_filename, client_id):
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.format_code_util = FormatCode()
        self.terminal = Terminal()
        self.args = args
        self.running = True
        self.main_filename = main_filename
        self.current_code = ""
        self.client = Client(host, port, client_id)
        self.client.register()
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_thread.daemon = True

    def receive_messages(self):
        poller = zmq.Poller()
        poller.register(self.client.listener_socket, zmq.POLLIN)
        
        while self.running:
            try:
                socks = dict(poller.poll(1000))  # Warte 1000 ms auf eingehende Nachrichten
                if socks.get(self.client.listener_socket) == zmq.POLLIN:
                    message = self.client.listener_socket.recv(zmq.NOBLOCK)  # Nicht blockierendes Empfangen
                    msg_obj = Message.deserialize(message)
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
                    self.save_received_code(msg_obj.content)
                    self.client.listener_socket.send(Message("server", self.client.client_id, Message.RESPONSE, "Message received").serialize())
            except zmq.ZMQError as e:
                print(f"ZMQ Error while receiving messages: {e}")
            except Exception as e:
                print(f"General Error while receiving messages: {e}")

    def save_received_code(self, code):
        print("Original received code:")
        print(code)
        self.current_code = self.format_code_util.format_code(code)
        print("Formatted code:")
        print(self.current_code)
        filename = self.format_code_util.extract_filename(self.current_code)
        if filename:
            self.file_operations.save_file(filename, self.current_code)
            print(f"Received code saved to file {filename}.")
        else:
            print("No valid filename found in received code.")

    def run(self):
        try:
            self.message_thread.start()
            print(f"Message receiving thread started: {self.message_thread.is_alive()}")

            while self.running:
                self.current_code, action = self.terminal.read_input()
                if not self.running:
                    break
                if action == 'save_only' and self.current_code:
                    self.save_received_code(self.current_code)
                elif action == 'save_and_send' and self.current_code:
                    self.save_received_code(self.current_code)
                    command = f"python3 {self.main_filename}"
                    self.client.send_message("run", self.client.client_id, Message.SEND, command)
                elif action == 'save_and_send' and not self.current_code:
                    command = f"python3 {self.main_filename}"
                    self.client.send_message("run", self.client.client_id, Message.SEND, command)
                else:
                    print("No code entered.")
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)
        finally:
            self.running = False
            if self.message_thread:
                self.message_thread.join(1)
            self.terminal.reset_terminal()
            print("FileManager terminated.")

    def signal_handler(self, sig, frame):
        print("Shutting down FileManager...")
        self.running = False
        self.terminal.reset_terminal()
        sys.exit(0)

#EOF
