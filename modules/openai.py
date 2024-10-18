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
import json

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
        overview_data (dict): Enthält Daten aus der overview.json, falls vorhanden.
        first_prompt_sent (bool): Indikator, ob der erste Prompt bereits an die KI gesendet wurde.
    """

    def __init__(self, args, host: str, port: int, api_key: str, organization: str, prompt: str, client_id: str, overview_data: dict = None):
        """
        Initialisiert die OpenAIIntegration-Klasse.

        :param args: Die Argumente, die beim Start der Anwendung übergeben wurden.
        :param host: Der Hostname des Servers.
        :param port: Der Port des Servers.
        :param api_key: Der API-Schlüssel für die OpenAI-Integration.
        :param organization: Die Organisation für die OpenAI-Integration.
        :param prompt: Der Start-Prompt für die Konversation.
        :param client_id: Die eindeutige ID des Clients.
        :param overview_data: Daten aus der overview.json, falls vorhanden.
        """
        super().__init__(host, port, client_id)
        self.api_key = api_key
        self.organization = organization
        self.prompt = prompt
        self.total_tokens = 0  # Gesamtanzahl der Tokens bisher
        self.overview_data = overview_data  # Speichert die Daten aus overview.json, falls vorhanden
        self.first_prompt_sent = False  # Indikator, ob der erste Prompt bereits gesendet wurde

        self.client = CodeGenerator(api_key, organization)  # Initialisiere den CodeGenerator
        self.conversation_manager = ConversationManager()
        self.conversation_manager.add_message("system", self.prompt)

        self.encoding = tiktoken.encoding_for_model("gpt-4")  # Tokenizer für das Modell

        # Registrierung bei ZMQ-Server
        self.register()

        # Starte Empfangsthread
        self.running = True
        self.receiver_thread = threading.Thread(target=self.start_receiving)  # Korrekte Referenzierung
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

       

    def start_receiving(self) -> None:
        """
        Wartet auf eingehende Nachrichten über ZMQ und verarbeitet diese.

        :return: None
        """
        while self.running:
            try:
                msg_obj = self.receive_message()  # Empfange Nachricht über ZMQ
                if msg_obj:
                    print(f"Received message from {msg_obj.sender}: {msg_obj.content}")
                    self.process_file_content(msg_obj.content)  # Verarbeite den empfangenen Datei-Inhalt
            except Exception as e:
                print(f"Error while receiving messages: {e}")

    def process_file_content(self, file_content: str) -> None:
        """
        Verarbeitet den empfangenen Datei-Inhalt und generiert eine Antwort von OpenAI.

        :param file_content: Der Inhalt der empfangenen Datei.
        :return: None
        """
        # Wenn der erste Prompt gesendet wird, hänge die overview.json Daten an
        if not self.first_prompt_sent:
            file_content = self._append_overview_to_prompt(file_content)
            self.first_prompt_sent = True

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

    def _append_overview_to_prompt(self, file_content: str) -> str:
        """
        Hängt den Inhalt von overview.json an den ersten Prompt an.

        :param file_content: Der ursprüngliche Prompt-Inhalt.
        :return: Der erweiterte Prompt-Inhalt mit der overview.json.
        """
        if self.overview_data:
            overview_text = "\n\n# Overview Data:\n"
            overview_text += json.dumps(self.overview_data, indent=2)  # Formatiere overview.json-Inhalt als Text
            print("overview.json an den ersten Prompt angehängt.")
            return file_content + overview_text
        return file_content

    def send_code_blocks(self, code_blocks: list) -> None:
        """
        Sendet die extrahierten Codeblöcke einzeln an den FileManager.

        :param code_blocks: Eine Liste von Codeblöcken, die gesendet werden sollen.
        :return: None
        """
        for block in code_blocks:
            try:
                recipient = "file_manager"
                message_type = Message.SEND
                print(f"Sende Codeblock an File_Manager")
                self.send_message(recipient, self.client_id, message_type, block)  # Sende Codeblock an FileManager
            except Exception as e:
                print(f"Error while sending code block: {e}")

    def run_interactive_mode(self) -> None:
        """
        Startet den interaktiven Modus zur Verarbeitung von Benutzeranfragen.

        :return: None
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

    def read_multiline_input(self, prompt: str) -> str:
        """
        Liest mehrzeilige Benutzereingaben.

        :param prompt: Der Text, der als Eingabeaufforderung angezeigt wird.
        :return: Der eingegebene mehrzeilige Text.
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

    def count_tokens(self, text: str) -> int:
        """
        Zählt die Anzahl der Tokens in einem gegebenen Text.

        :param text: Der Text, dessen Tokens gezählt werden sollen.
        :return: Die Anzahl der Tokens.
        """
        return len(self.encoding.encode(text))

# EOF
