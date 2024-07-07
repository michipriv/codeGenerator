import json
import socket
import sys
import termios
import tty
import os
from datetime import datetime
from modules.code_generator import CodeGenerator

class OpenAIIntegration:
    def __init__(self, args, host, port, api_key, organization):
        self.client = CodeGenerator(api_key, organization)
        self.server_address = (host, port)
        self.register_with_server()
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.conversation_history = []
        self.log_directory = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def register_with_server(self):
        self.send_message('register:openai')

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(self.server_address)
            s.sendall(message.encode('utf-8'))

    def receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.server_address[1] + 1))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        return data.decode('utf-8')
        return None

    def create_prompt(self):
        return (
            "Verhalte dich wie ein Python-Entwickler, der objektorientiert und mit Klassen entwickelt. "
            "Bei der Antwort füge im Codeblock immer die Zeile mit: #Filename ein, das ist extrem wichtig für die Zuordnung. "
            "Achte darauf, dass der Code mit #Filename beginnt und mit #EOF endet."
            "Das Hauptprogramm heißt immer main.py. "
            "Klassen werden im Verzeichnis modules abgespeichert."
            "Du kannst mit dem Befehl: delete_file:dateiname Daten löschen."
            "Du kannst mit dem Befehl: delete_directory:verzeichnis Daten löschen."
        )

    def read_multiline_input(self, prompt):
        print(prompt)
        print("")
        
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                print("Eingabe abgeschlossen.")
                break
            lines.append(line)
        return "\n".join(lines)

    def extract_code_blocks(self, text):
        code_blocks = []
        remaining_text = text
        while True:
            start_index = remaining_text.find("#Filename:")
            if start_index == -1:
                break
            end_index = remaining_text.find("#EOF", start_index)
            if end_index == -1:
                print("Warnung: Kein #EOF gefunden. Abbruch.")
                break
            end_index += len("#EOF")
            code_blocks.append(remaining_text[start_index:end_index].strip())
            remaining_text = remaining_text[:start_index] + remaining_text[end_index:]
        return code_blocks, remaining_text.strip()

    def log_ki_antwort(self, generierter_code):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_filename = os.path.join(self.log_directory, f"ki-ausgabe.log.{timestamp}")
        with open(log_filename, 'w') as log_file:
            log_file.write(generierter_code)
        print(f"KI-Antwort in {log_filename} gespeichert.")

    def run_interactive_mode(self):
        try:
            gpt_assistant_prompt = self.create_prompt()
            self.conversation_history.append({"role": "system", "content": gpt_assistant_prompt})
            
            while True:
                gpt_user_prompt = self.read_multiline_input("Was soll ich tun? (Beenden mit Strg+D) ")
                self.conversation_history.append({"role": "user", "content": gpt_user_prompt})
                
                # Generiere den Code basierend auf der Benutzereingabe und sende ihn an den FileManager
                generierter_code = self.client.generiere_code(self.conversation_history)
                #print("##### TEST AUSGABE Code-generator -ki"); print(generierter_code); print("##### TEST AUSGABE Code-generator -ki")

                # Loggen der KI-Antwort
                self.log_ki_antwort(generierter_code)

                # Trenne KI-Text und Codeblöcke
                code_blocks, remaining_text = self.extract_code_blocks(generierter_code)
                
                # Zeige den textlichen Teil der KI-Antwort an
                if remaining_text:
                    print("KI-Antwort (ohne Code):")
                    print(remaining_text)
                
                self.conversation_history.append({"role": "assistant", "content": generierter_code})
                
                for block in code_blocks:
                    self.send_message(f"message:file_manager:save:{block}")
                    print(f"Codeblock an FileManager gesendet:\n{block}")

                # Verarbeiten von Löschbefehlen (Dateien und Verzeichnisse)
                if "delete_file:" in remaining_text:
                    file_to_delete = remaining_text.split("delete_file:")[1].strip()
                    self.send_message(f"message:file_manager:delete_file:{file_to_delete}")
                    print(f"Lösche Datei: {file_to_delete}")
                if "delete_directory:" in remaining_text:
                    directory_to_delete = remaining_text.split("delete_directory:")[1].strip()
                    self.send_message(f"message:file_manager:delete_directory:{directory_to_delete}")
                    print(f"Lösche Verzeichnis: {directory_to_delete}")

        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

#EOF
