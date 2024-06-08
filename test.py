import os
from art import text2art

def clear_screen():
    # Überprüfen, ob das Betriebssystem Windows ist
    if os.name == 'nt':
        os.system('cls')  # Befehl zum Löschen des Bildschirms unter Windows
    else:
        os.system('clear')  # Befehl zum Löschen des Bildschirms unter Unix/Linux/Mac

def print_hello_world_ascii():
    ascii_art = text2art("Hello, World!")
    print(ascii_art)

# Bildschirm löschen
clear_screen()

# ASCII-Art drucken
print_hello_world_ascii()