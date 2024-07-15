# Filename: main.py

import sys
import os
import json
import signal

# Bestimme das Basisverzeichnis (codeGenerator)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Füge das BASE_DIR zum Suchpfad hinzu
sys.path.append(BASE_DIR)

from modules.argument_parser import ArgumentParser
from modules.server import ServerHandler
from modules.file_manager import FileManager
from modules.run import Run  # Importiere die Run-Klasse
from modules.beispiel import ExampleClient  # Importiere die ExampleClient-Klasse
from modules.openai import OpenAIIntegration  # Importiere die OpenAIIntegration-Klasse

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config(file_path='etc/config.json'):
    with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8') as f:
        return json.load(f)

def load_prompts(file_path='etc/prompt.txt'):
    prompts = {}
    current_key = None
    current_prompt = []

    try:
        with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8', errors='replace') as file:
            for line in file:
                line = line.strip()
                if line.startswith('//') or not line:
                    continue
                if line.startswith('PROMPT:'):
                    current_key = line[len('PROMPT:'):].strip()
                    current_prompt = []
                elif line.startswith('TEXT:') and current_key:
                    current_prompt = [line[len('TEXT:'):].strip()]
                elif line.startswith('END:') and current_key:
                    prompts[current_key] = '\n'.join(current_prompt)
                    current_key = None
                    current_prompt = []
                elif current_key:
                    current_prompt.append(line)
    
        #debugausgabe
        #for key, value in prompts.items():
        #    print(f"{key}: {value}")
        #    print("::::::::::::::::::::::::::::")
            
            
    except UnicodeDecodeError as e:
        print(f"Error decoding file {file_path}: {e}")
    return prompts


def main():
    clear_screen()

    config = load_config()  # config laden
    prompts_dict = load_prompts()  # Laden der Prompts aus der Textdatei
    # Argumente parsen
    args = ArgumentParser()

    server_thread = None

    def signal_handler(sig, frame):
        if server_thread:
            server_thread.signal_handler(sig, frame)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    prompt_text = prompts_dict.get(args.prompt)
    
    
    
    if args.help:
        args.print_help()
    elif args.ki:
        print("Starting OpenAI mode...")
        #print(prompt_text)
        openai_integration = OpenAIIntegration(args, config['host'], config['port'], config['openai_api_key'], config['openai_organization'], prompt_text,  client_id="openai")
        openai_integration.run_interactive_mode()
    elif args.server_mode:
        print("Starting server mode...")
        server_thread = ServerHandler(config['host'], config['port'])
        server_thread.start_server()  # Sync Server-Start
    elif args.run_mode:
        print("Starting run mode...")
        run_client = Run(args, config['host'], config['port'], client_id="run")
        run_client.start()
    elif args.edit_filename:
        print(f"Starting FileManager mode for main file: {args.edit_filename}...")
        file_manager = FileManager(args, config['host'], config['port'], args.edit_filename, client_id="file_manager")
        file_manager.run()
    elif args.example_mode:
        print("Starting example mode...")
        example_client = ExampleClient(config['host'], config['port'], client_id="run")
        example_client.run()
        
    else:
        print("No valid arguments provided. Use '-h' for help.")

if __name__ == "__main__":
    main()

#EOF
