import os
from modules.utils import clear_screen
from modules.file_manager import FileManager
from modules.argument_parser import ArgumentParser
from modules.server import ServerHandler

if __name__ == "__main__":
    clear_screen()
    
    # Argumente parsen
    args = ArgumentParser()

    if args.help:
        args.print_help()
    elif args.run_mode:
        server_handler = ServerHandler()
        server_handler.run_mode(args.program_to_run)
    else:
        # Starten des FileManagers
        file_manager = FileManager(args)
        file_manager.run()
