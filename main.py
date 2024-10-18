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
    """
    Clears the terminal screen based on the operating system.

    - On Windows, it uses the 'cls' command.
    - On Unix-based systems, it uses the 'clear' command.

    :return: None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config(file_path: str = 'etc/config.json') -> dict:
    """
    Loads configuration settings from a JSON file.

    :param file_path: The path to the configuration file (default: 'etc/config.json').
    :return: A dictionary containing the configuration data.
    """
    with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8') as f:
        return json.load(f)

def load_prompts(file_path: str = 'etc/prompt.txt') -> dict:
    """
    Loads prompts from a text file with a custom format. The text file must follow a specific structure,
    with prompts indicated by 'PROMPT:' and corresponding text between 'TEXT:' and 'END:'.

    :param file_path: The path to the prompts file (default: 'etc/prompt.txt').
    :return: A dictionary mapping prompt names to their corresponding prompt text.
    """
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
    except UnicodeDecodeError as e:
        print(f"Error decoding file {file_path}: {e}")
    return prompts

def load_overview_json(file_path: str = 'doc/overview.json') -> dict:
    """
    Läd die Datei overview.json aus dem Verzeichnis 'doc/overview' und gibt den Inhalt zurück.

    Falls die Datei nicht existiert, wird eine Fehlermeldung ausgegeben.

    :param file_path: Der Pfad zur overview.json-Datei (standardmäßig im Verzeichnis doc/overview).
    :return: Der Inhalt der Datei als Dictionary.
    """
    try:
        with open(os.path.join(BASE_DIR, file_path), 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"overview.json erfolgreich geladen: {file_path}")
            return data
    except FileNotFoundError:
        print(f"Die Datei {file_path} wurde nicht gefunden. Sie muss zuerst erstellt werden.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Fehler beim Einlesen der JSON-Datei: {e}")
        return {}

def main():
    """
    Main entry point of the application. This function clears the screen, loads the configuration and prompt files,
    parses command-line arguments, and starts the appropriate mode based on the arguments provided.

    Supported modes:
    - **OpenAI Mode**: Uses OpenAI API for AI-based interaction.
    - **Server Mode**: Starts the application in server mode.
    - **Run Mode**: Runs a client in a custom mode.
    - **File Manager Mode**: Opens the file manager for a given file.
    - **Example Mode**: Runs a sample client as an example.

    :return: None
    """
    clear_screen()

    # Lade overview.json aus dem Verzeichnis 'doc/overview', wenn vorhanden
    overview_data = load_overview_json()

    # Load the configuration and prompts
    config = load_config()  # Config laden
    prompts_dict = load_prompts()  # Prompts aus der Textdatei laden

    # Parse command-line arguments
    args = ArgumentParser()

    server_thread = None

    def signal_handler(sig, frame):
        """
        Handles system signals, allowing graceful shutdown when the application runs in server mode.

        :param sig: The signal received.
        :param frame: The current stack frame.
        :return: None
        """
        if server_thread:
            server_thread.signal_handler(sig, frame)
        sys.exit(0)

    # Set up the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Retrieve the prompt text based on the argument
    prompt_text = prompts_dict.get(args.prompt)
    
    # Display the prompt being used
    if prompt_text:
        print(f"Prompt '{args.prompt}' wurde erfolgreich geladen.")
    else:
        print(f"Kein Prompt gefunden für '{args.prompt}'.")

    # Handle different modes based on command-line arguments
    if args.help:
        # Zeige Hilfe und verfügbare Optionen
        args.print_help()
    elif args.ki:
        # Starte den OpenAI-Integrationsmodus
        print("Starting OpenAI mode...")
        openai_integration = OpenAIIntegration(
            args,
            config['host'],
            config['port'],
            config['openai_api_key'],
            config['openai_organization'],
            prompt_text,
            client_id="openai",
            overview_data=overview_data  # Übergibt die geladenen Daten aus overview.json
        )
        openai_integration.run_interactive_mode()
    elif args.server_mode:
        # Starte den Server-Modus
        print("Starting server mode...")
        server_thread = ServerHandler(config['host'], config['port'])
        server_thread.start_server()  # Sync Server-Start
    elif args.run_mode:
        # Starte den Run-Modus für benutzerdefinierte Befehle
        print("Starting run mode...")
        run_client = Run(args, config['host'], config['port'], client_id="run")
        run_client.start()
    elif args.edit_filename:
        # Starte den FileManager-Modus für die angegebene Datei
        print(f"Starting FileManager mode for main file: {args.edit_filename}...")
        file_manager = FileManager(args, config['host'], config['port'], args.edit_filename, client_id="file_manager")
        file_manager.run()
    elif args.example_mode:
        # Starte den Beispielmodus
        print("Starting example mode...")
        example_client = ExampleClient(config['host'], config['port'], client_id="run")
        example_client.run()
    else:
        # Kein gültiges Argument angegeben
        print("No valid arguments provided. Use '-h' for help.")

if __name__ == "__main__":
    main()

# EOF
