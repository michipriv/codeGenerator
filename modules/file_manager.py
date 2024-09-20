# Filename: modules/file_manager.py

import os
import threading
import signal
import zmq
from modules.file_operations import FileOperations
from modules.backup_manager import BackupManager
from modules.terminal import Terminal
from modules.client import Client
from modules.message import Message
from modules.format_code import FormatCode

class FileManager:
    """
    Klasse zur Verwaltung von Dateien und Nachrichten.

    Diese Klasse ermöglicht das Speichern und Verarbeiten von Code,
    das Empfangen von Nachrichten über ZMQ und das Erstellen von Backups.

    Attributes:
        backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
        file_operations (FileOperations): Die Instanz zur Durchführung von Dateioperationen.
        format_code_util (FormatCode): Die Instanz zur Formatierung von Code.
        terminal (Terminal): Die Instanz zur Verwaltung der Benutzereingabe.
        args: Argumente, die beim Starten des FileManagers übergeben wurden.
        running (bool): Gibt an, ob der FileManager aktiv ist.
        main_filename (str): Der Name der Hauptdatei, die verwaltet wird.
        current_code (str): Der aktuell bearbeitete Code.
        client (Client): Die Instanz zur Kommunikation mit dem Server.
        message_thread (threading.Thread): Der Thread zum Empfangen von Nachrichten.
    """

    def __init__(self, args, host, port, main_filename, client_id):
        """
        Initialisiert die FileManager-Klasse.

        Parameters:
            args: Argumente, die beim Starten des FileManagers übergeben werden.
            host (str): Der Hostname des Servers.
            port (int): Der Port des Servers.
            main_filename (str): Der Name der Hauptdatei, die verwaltet wird.
            client_id (str): Die eindeutige ID des Clients.
        """
        self.backup_manager = BackupManager()
        self.file_operations = FileOperations(self.backup_manager)
        self.format_code_util = FormatCode()  # Initialisiere FormatCode
        self.terminal = Terminal(self.file_operations)
        self.args = args
        self.running = True
        self.main_filename = main_filename
        self.current_code = ""
        self.client = Client(host, port, client_id)
        self.client.register()
        self.message_thread = threading.Thread(target=self.receive_messages)
        self.message_thread.daemon = True

    def run(self):
        """
        Startet den FileManager-Modus und verarbeitet Benutzereingaben.
        """
        print(f"FileManager started for file: {self.main_filename}")
        self.message_thread.start()

        try:
            while self.running:
                self.current_code, action = self.terminal.read_input()
                if action == 'save_only' and self.current_code:
                    self.save_received_code(self.current_code)
                elif action == 'save_and_send':
                    command = f"python3 {self.main_filename}"
                    self.client.send_message("run", self.client.client_id, Message.SEND, command)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

    def receive_messages(self):
        """
        Empfängt Nachrichten über den ZMQ-Socket und verarbeitet sie.
        """
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
        """
        Speichert den empfangenen Code nach Formatierung.

        Parameters:
            code (str): Der empfangene Code, der gespeichert werden soll.
        """
        print("Original received code:")
        print(code)

        # Formatieren des Codes
        self.current_code = self.format_code_util.format_code(code)
        print("Formatted code:")
        print(self.current_code)

        # Extrahiere den Dateinamen
        filename = self.format_code_util.extract_filename(self.current_code)
        if filename:
            self.file_operations.save_file(filename, self.current_code)
            print(f"Received code saved to file {filename}.")
        else:
            print("Fehler: Kein gültiger Dateiname im Code gefunden.")
            default_filename = "received_code.py"
            self.file_operations.save_file(default_filename, self.current_code)
            print(f"Der Code wurde unter {default_filename} gespeichert.")

    def signal_handler(self, sig, frame):
        """
        Behandelt das Signal zum Beenden des FileManagers.

        Parameters:
            sig: Das empfangene Signal.
            frame: Der aktuelle Stack-Frame.
        """
        print("Shutting down FileManager...")
        self.running = False
        sys.exit(0)

#EOF
