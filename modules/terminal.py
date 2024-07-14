# Filename: modules/terminal.py

import termios
import tty
import sys
import signal

class Terminal:
    def __init__(self):
        self.old_settings = termios.tcgetattr(sys.stdin.fileno())
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print("\nStrg+C erkannt, beende das Programm...")
        self.running = False
        self.reset_terminal()
        sys.exit(0)

    def reset_terminal(self):
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
        print("\nTerminal wurde zurückgesetzt.")

    def read_input(self):
        code_lines = []
        print("Bitte fügen Sie den Code ein (Ende mit Strg+D, Strg+F oder Strg+C):")
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while self.running:
                ch = sys.stdin.read(1)
                if ch == '\x04':
                    print("\nStrg+D erkannt, speichere den Code...")
                    return '\n'.join(code_lines), 'save_only'
                elif ch == '\x06':
                    print("\nStrg+F erkannt, speichere den Code und führe ihn aus...")
                    return '\n'.join(code_lines), 'save_and_send'
                elif ch == '\x03':
                    print("\nStrg+C erkannt, beende das Programm...")
                    self.signal_handler(signal.SIGINT, None)
                    return None, None
                elif ch in ['\r', '\n']:
                    code_lines.append('')
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                elif ch == '\x7f':
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

#EOF
