# Filename: run.py

import socket
import signal
import sys
import os

class Run:
    def __init__(self, args, host, port ):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.server_address = (host, port)
        self.program_to_run = args.program_to_run
        self.program_call = args.program_call
        self.running = True

    def signal_handler(self, sig, frame):
        print("Run wird durch Strg+C beendet.")
        self.running = False
        sys.exit(0)

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def start(self):
        print(f"Run-Client läuft und wartet auf Befehle am Port {self.server_address[1]}...")
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(self.server_address)
                    s.sendall(b'register:run')
                    response = s.recv(1024).decode('utf-8')
                    print(f"Antwort vom Server: {response}")
                    while self.running:
                        data = s.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8')
                        print(f"Befehl empfangen: {command}")
                        if command.startswith('execute:'):
                            filename = command.split(':')[1]
                            if os.path.exists(filename):
                                print(f"Führe Datei {filename} aus...")
                                
                                print (f'{self.program_call} {filename}')
                                os.system(f'{self.program_call} {filename}')    # Interpreter oder compilieren
                                
                                #if self.program_to_run:
                                #    os.system(f'./{self.program_to_run}')  # compiler prg starten
                                    
                                
                                self.send_message('Befehl empfangen und ausgeführt')
                            else:
                                self.send_message('Datei nicht gefunden')
                        elif command == 'exit':
                            self.running = False
                            break
            except Exception as e:
                print(f"Fehler im Run-Client: {e}")
                self.running = False
                sys.exit(0)



#EOF