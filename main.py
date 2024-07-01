# Filename: main.py

import sys
import os
import json
import signal

# Bestimme das Basisverzeichnis (codeGenerator)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Füge das BASE_DIR zum Suchpfad hinzu
sys.path.append(BASE_DIR)

from modules.utils import clear_screen
from modules.file_manager import FileManager
from modules.argument_parser import ArgumentParser
from modules.run import Run
from modules.server import ServerHandler
from modules.openai import OpenAIIntegration

def load_config(file_path='etc/config.json'):
    with open(os.path.join(BASE_DIR, file_path), 'r') as f:
        return json.load(f)

def main():
    clear_screen()

    config = load_config()

    # Argumente parsen
    args = ArgumentParser()

    server_thread = None

    def signal_handler(sig, frame):
        if server_thread and server_thread.is_alive():
            server_thread.signal_handler(sig, frame)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if args.help:
        args.print_help()
    elif args.ki:
        print("Starte OpenAI-Modus...")
        openai_integration = OpenAIIntegration(args, config['host'], config['port'], os.path.join(BASE_DIR, 'etc/api_key.json'))
        openai_integration.run_interactive_mode()
    elif args.server_mode:
        print("Starte Server-Modus...")
        server_thread = ServerHandler(config['host'], config['port'])
        server_thread.start()
        
        try:
            server_thread.join()  # Lässt den Hauptthread auf den Server-Thread warten
        except KeyboardInterrupt:
            if server_thread:
                server_thread.stop()
    elif args.run_mode:
        print("Starte Run-Modus...")
        run_client = Run(args, config['host'], config['port'])
        run_client.start()
    else:
        print("Starte FileManager-Modus...")
        file_manager = FileManager(args, config['host'], config['port'])
        file_manager.run()

if __name__ == "__main__":
    main()
