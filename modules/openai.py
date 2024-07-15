# Filename: modules/openai.py

import sys
import termios
import tty
import threading
import os
import tiktoken
from modules.code_generator import CodeGenerator
from modules.conversation_manager import ConversationManager
from modules.client import Client
from modules.message import Message

class OpenAIIntegration(Client):
    def __init__(self, args, host, port, api_key, organization, prompt, client_id):
        super().__init__(host, port, client_id)
        self.api_key = api_key
        self.organization = organization
        self.prompt = prompt
        self.total_tokens = 0  # Gesamtanzahl der Tokens bisher

        self.client = CodeGenerator(api_key, organization)  # Initialisiere den CodeGenerator
        self.conversation_manager = ConversationManager()
        self.conversation_manager.add_message("system", self.prompt)
        
        self.encoding = tiktoken.encoding_for_model("gpt-4")  # Tokenizer für das Modell

        # Register with the server
        self.register()

        # Start the receiver thread
        self.running = True
        self.receiver_thread = threading.Thread(target=self.start_receiving)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def create_prompt(self):
        return self.prompt

    def read_multiline_input(self, prompt):
        print("")
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

    def count_tokens(self, text):
        return len(self.encoding.encode(text))

    def run_interactive_mode(self):
        try:
            while True:
                print("Waiting for user input...")
                gpt_user_prompt = self.read_multiline_input("Was soll ich tun? (Beenden mit Strg+D) ")
                
                self.conversation_manager.add_message("user", gpt_user_prompt)
                
                user_tokens = self.count_tokens(gpt_user_prompt)
                
                generierter_code = self.client.generiere_code(self.conversation_manager.get_history())
                
                assistant_tokens = self.count_tokens(generierter_code)
                self.total_tokens += user_tokens + assistant_tokens
                
                print(f"Tokens - Frage: {user_tokens} | Antwort: {assistant_tokens} | Gesamt: {self.total_tokens}")
                
                self.conversation_manager.log_ki_antwort(generierter_code)
                
                code_blocks, remaining_text = self.conversation_manager.extract_code_blocks(generierter_code)
                
                self.log_code_blocks(code_blocks)  # Logge die Codeblöcke zur Kontrolle
                self.send_code_blocks(code_blocks)  # Sende die Codeblöcke einzeln

                self.conversation_manager.save_content(remaining_text, code_blocks)
                
                self.conversation_manager.add_message("assistant", generierter_code)

                print("Gespeicherte Inhalte:")
                for item in self.conversation_manager.content_list:
                    key, value = item
                    if key == "TEXT":
                        print(f"{key}: {value}")

        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")
        finally:
            self.running = False
            self.receiver_thread.join()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def start_receiving(self):
        while self.running:
            try:
                msg_obj = self.receive_message()
                if msg_obj:
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
            except Exception as e:
                print(f"Error while receiving messages: {e}")

    def send_code_blocks(self, code_blocks):
        for block in code_blocks:
            try:
                recipient = "file_manager"
                message_type = "send"
                self.send_message(recipient, self.client_id, message_type, block)
            except Exception as e:
                print(f"Error while sending code block: {e}")

    def log_code_blocks(self, code_blocks):
        log_directory = os.path.join(os.getcwd(), 'log')
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        
        for i, block in enumerate(code_blocks, 1):
            log_filename = os.path.join(log_directory, f"code_block_{i}.log")
            with open(log_filename, 'w') as log_file:
                log_file.write(block)

    def run(self):
        recv_thread = threading.Thread(target=self.start_receiving)
        recv_thread.daemon = True
        recv_thread.start()

        try:
            pass  # Hier wird nichts weiter gemacht, send_message_input wurde entfernt
        except KeyboardInterrupt:
            self.running = False
            recv_thread.join()

#EOF
