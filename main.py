#Filename: main.py
import sys
import os
from modules.utils import clear_screen, print_help
from modules.file_manager import FileManager

if __name__ == "__main__":
    clear_screen()
    file_manager = FileManager()
    file_manager.run()
