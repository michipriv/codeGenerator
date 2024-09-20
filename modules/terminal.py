# Filename: modules/terminal.py

import termios
import tty
import sys
import signal

class Terminal:
    """
    Klasse zur Verwaltung der Terminal-Eingaben.

    Diese Klasse ermöglicht das Lesen von Benutzereingaben im Terminal
    und behandelt spezielle Steuerbefehle wie Strg+C, Strg+D, Strg+F und Strg+L.

    Attributes:
        file_operations (FileOperations): Instanz der FileOperations-Klasse.
        old_settings: Alte Terminal-Einstellungen zur Wiederherstellung.
        running (bool): Status, ob das Terminal aktiv ist oder nicht.
    """

    def __init__(self, file_operations):
        """
        Initialisiert die Terminal-Klasse.

        Parameters:
            file_operations (FileOperations): Instanz der FileOperations-Klasse.
        """
        self.file_operations = file_operations
        self.old_settings = termios.tcgetattr(sys.stdin.fileno())
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        """
        Behandelt das Signal für Strg+C, um das Programm zu beenden.

        Parameters:
            sig: Das empfangene Signal.
            frame: Der aktuelle Stack-Frame.
        """
        print("\nStrg+C erkannt, beende das Programm...")
        self.running = False
        self.reset_terminal()
        sys.exit(0)

    def reset_terminal(self):
        """
        Setzt die Terminal-Einstellungen auf die alten Werte zurück.
        """
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
        print("\nTerminal wurde zurückgesetzt.")

    def read_input(self):
        """
        Liest Benutzereingaben im Terminal und verarbeitet Steuerbefehle.

        Returns:
            tuple: Ein Tuple, das den eingegebenen Code (oder None) und die Aktion enthält.
        """
        code_lines = []
        print("Bitte fügen Sie den Code ein (Ende mit Strg+D, Strg+F, Strg+L oder Strg+C):")
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while self.running:
                ch = sys.stdin.read(1)
                if ch == '\x04':  # STRG + D
                    print("\nStrg+D erkannt, speichere den Code...")
                    return '\n'.join(code_lines), 'save_only'
                elif ch == '\x06':  # STRG + F
                    print("\nStrg+F erkannt, speichere den Code und führe ihn aus...")
                    return '\n'.join(code_lines), 'save_and_send'
                elif ch == '\x0C':  # STRG + L
                    print("\nStrg+L erkannt, sende Dateien an OpenAI...")
                    return None, 'send_files_to_openai'  # Neue Aktion für STRG + L
                elif ch == '\x03':  # STRG + C
                    print("\nStrg+C erkannt, beende das Programm...")
                    self.signal_handler(signal.SIGINT, None)
                    return None, None
                elif ch in ['\r', '\n']:
                    code_lines.append('')
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                elif ch == '\x7f':  # Backspace
                    if code_lines and code_lines[-1]:
                        code_lines[-1] = code_lines[-1][:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    if len(code_lines) == 0:
                        code_lines.append(ch)
                    else:
                        code_lines[-1] += ch
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# EOF
