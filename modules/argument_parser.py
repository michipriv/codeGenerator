# Filename: modules/argument_parser.py

import sys

class ArgumentParser:
    def __init__(self):
        self.help = False
        self.edit_filename = None
        self.run_mode = False
        self.ki = False
        self.server_mode = False
        self.example_mode = False
        self.client_id = None
        self.prompt = None
        self.parse_arguments()

    def parse_arguments(self):
        if len(sys.argv) > 1:
            if '-h' in sys.argv or '--help' in sys.argv:
                self.help = True
            if '-d' in sys.argv:
                filename_index = sys.argv.index('-d') + 1
                if filename_index < len(sys.argv):
                    self.edit_filename = sys.argv[filename_index]
                else:
                    print("No filename provided. Use the format 'python3 main.py -d <filename>'")
                    sys.exit(1)
            if '-r' in sys.argv:
                self.run_mode = True
            if '-s' in sys.argv:
                self.server_mode = True
            if '-ki' in sys.argv:
                self.ki = True
                if '-p' in sys.argv:
                    prompt_index = sys.argv.index('-p') + 1
                    if prompt_index < len(sys.argv):
                        self.prompt = sys.argv[prompt_index]
                    else:
                        print("No prompt provided. Use the format 'python3 main.py -ki -p <prompt>'")
                        sys.exit(1)
                else:
                    print("The -ki option requires the -p <prompt> argument. Use the format 'python3 main.py -ki -p <prompt>'")
                    sys.exit(1)
            if '-bsp' in sys.argv:
                self.example_mode = True
                client_id_index = sys.argv.index('-bsp') + 1
                if client_id_index < len(sys.argv):
                    self.client_id = sys.argv[client_id_index]
                else:
                    print("No client ID provided. Use the format 'python3 main.py -bsp <client_id>'")
                    sys.exit(1)

    def print_help(self):
        help_message = """
Usage: python script.py [OPTION]

Options:
  -h, --help         Show this help message
  -d FILENAME        Main file to run
  -r                 Start the run server and wait for commands
  -s                 Start the server
  -ki                Run the OpenAI integration and generate code based on a description
  -bsp CLIENT_ID     Start the example client that receives and sends messages to the server
  -p PROMPT          Load prompt with the given name from the prompts file

Without parameters, the script starts in interactive mode and expects input in the following format:
  FILENAME

Examples:
  python script.py -h
  python script.py -d main.py
  python script.py -d some_file.txt -r
  python script.py -s
  python script.py -ki -p python-entwickler
  python script.py -bsp client_id
  python script.py -p python-entwickler
"""
        print(help_message)

#EOF
