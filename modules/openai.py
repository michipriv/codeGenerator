# Filename: modules/openai.py

from modules.client import Client
import threading
import os
import termios
import sys
from modules.message import Message
from modules.code_generator import CodeGenerator
from modules.conversation_manager import ConversationManager
import tiktoken

class OpenAIIntegration(Client):
    """
    Klasse zur Integration mit OpenAI, die die Kommunikation mit der OpenAI-API verwaltet
    und die Verarbeitung von Benutzeranfragen sowie die Extraktion von Codeblöcken übernimmt.

    Attributes:
        api_key (str): Der API-Schlüssel für die OpenAI-Integration.
        organization (str): Die Organisation für die OpenAI-Integration.
        prompt (str): Der Start-Prompt für die Konversation.
        total_tokens (int): Die Gesamtanzahl der bisher verwendeten Tokens.
        client (CodeGenerator): Der CodeGenerator zur Generierung von Code.
        conversation_manager (ConversationManager): Verwaltet die Konversationshistorie.
        encoding: Tokenizer für das GPT-4-Modell.
        running (bool): Gibt an, ob die Instanz aktiv ist.
        receiver_thread (threading.Thread): Thread zum Empfang von Nachrichten.
    """

    def __init__(self, args, host, port, api_key, organization, prompt, client_id):
        """
        Initialisiert die OpenAIIntegration-Klasse.

        Parameters:
            args: Die Argumente, die beim Start der Anwendung übergeben wurden.
            host (str): Der Hostname des Servers.
            port (int): Der Port des Servers.
            api_key (str): Der API-Schlüssel für die OpenAI-Integration.
            organization (str): Die Organisation für die OpenAI-Integration.
            prompt (str): Der Start-Prompt für die Konversation.
            client_id (str): Die eindeutige ID des Clients.
        """
        super().__init__(host, port, client_id)
        self.api_key = api_key
        self.organization = organization
        self.prompt = prompt
        self.total_tokens = 0  # Gesamtanzahl der Tokens bisher

        self.client = CodeGenerator(api_key, organization)  # Initialisiere den CodeGenerator
        self.conversation_manager = ConversationManager()
        self.conversation_manager.add_message("system", self.prompt)

        self.encoding = tiktoken.encoding_for_model("gpt-4")  # Tokenizer für das Modell

        # Registrierung bei ZMQ-Server
        self.register()

        # Starte Empfangsthread
        self.running = True
        self.receiver_thread = threading.Thread(target=self.start_receiving)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def start_receiving(self):
        """
        Wartet auf eingehende Nachrichten über ZMQ und verarbeitet diese.
        """
        while self.running:
            try:
                msg_obj = self.receive_message()  # Empfange Nachricht über ZMQ
                if msg_obj:
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
                    self.process_file_content(msg_obj.content)  # Verarbeite den empfangenen Datei-Inhalt
            except Exception as e:
                print(f"Error while receiving messages: {e}")

    def process_file_content(self, file_content):
        """
        Verarbeitet den empfangenen Datei-Inhalt und generiert eine Antwort von OpenAI.

        Parameters:
            file_content (str): Der Inhalt der empfangenen Datei.
        """
        # Füge den Inhalt zur Konversation hinzu
        self.conversation_manager.add_message("user", file_content)

        # Generiere die Antwort von OpenAI
        generierter_code = self.client.generiere_code(self.conversation_manager.get_history())

        # Codeblöcke und restlichen Text extrahieren
        code_blocks, remaining_text = self.conversation_manager.extract_code_blocks(generierter_code)

        # Sende die Codeblöcke einzeln an den FileManager
        if code_blocks:
            self.send_code_blocks(code_blocks)
        else:
            print("Keine Codeblöcke gefunden!")

        # Gib den restlichen Text ohne Codeblöcke aus
        if remaining_text.strip():
            print("KI Antwort:")
            print("")
            print(remaining_text)

    def send_code_blocks(self, code_blocks):
        """
        Sendet die extrahierten Codeblöcke einzeln an den FileManager.

        Parameters:
            code_blocks (list): Eine Liste von Codeblöcken, die gesendet werden sollen.
        """
        for block in code_blocks:
            try:
                recipient = "file_manager"
                message_type = Message.SEND
                print(f"Sende Codeblock an File_Manager")
                self.send_message(recipient, self.client_id, message_type, block)  # Sende Codeblock an FileManager
            except Exception as e:
                print(f"Error while sending code block: {e}")

    def run_interactive_mode(self):
        """
        Startet den interaktiven Modus zur Verarbeitung von Benutzeranfragen.
        """
        try:
            while True:
                print("Waiting for user input...")
                gpt_user_prompt = self.read_multiline_input("Was soll ich tun? (Beenden mit Strg+D) ")

                # Füge die Benutzereingabe zur Konversation hinzu
                self.conversation_manager.add_message("user", gpt_user_prompt)

                # Generiere die OpenAI-Antwort basierend auf dem Konversationsverlauf
                generierter_code = self.client.generiere_code(self.conversation_manager.get_history())

                # Extrahiere Codeblöcke und Text
                code_blocks, remaining_text = self.conversation_manager.extract_code_blocks(generierter_code)

                # Sende die Codeblöcke an den FileManager
                if code_blocks:
                    self.send_code_blocks(code_blocks)
                else:
                    print("Keine Codeblöcke gefunden!")

                # Zeige den Text ohne Codeblöcke im Terminal an
                if remaining_text.strip():
                    print("Generierter Text (ohne Codeblöcke):")
                    print(remaining_text)

        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")
        finally:
            self.running = False
            self.receiver_thread.join()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def read_multiline_input(self, prompt):
        """
        Liest mehrzeilige Benutzereingaben.

        Parameters:
            prompt (str): Der Text, der als Eingabeaufforderung angezeigt wird.

        Returns:
            str: Der eingegebene mehrzeilige Text.
        """
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
        """
        Zählt die Anzahl der Tokens in einem gegebenen Text.

        Parameters:
            text (str): Der Text, dessen Tokens gezählt werden sollen.

        Returns:
            int: Die Anzahl der Tokens.
        """
        return len(self.encoding.encode(text))

# EOF
