#Filename: main.py

import sys
from modules.utils import clear_screen
from modules.file_manager import FileManager
from modules.argument_parser import ArgumentParser
from modules.server import ServerHandler
from modules.run import Run
from modules.openai import OpenAIIntegration

def main():
    clear_screen()
    
    # Argumente parsen
    args = ArgumentParser()

    if args.help:
        args.print_help()
    elif args.run_mode:
        run_server = Run()
        run_server.receive_commands(args.program_to_run)
    elif args.ki:
        openai_integration = OpenAIIntegration('api_key.json')
        openai_integration.run_interactive_mode()
    else:
        # Starten des FileManagers
        file_manager = FileManager(args)
        file_manager.run()

if __name__ == "__main__":
    main()
