# Filename: modules/conversation_manager.py

import tiktoken
import os
from datetime import datetime
import re

class ConversationManager:
    """
    Klasse zur Verwaltung der Konversationshistorie und zur Extraktion von Codeblöcken.

    Attributes:
        conversation_history (list): Liste der Nachrichten in der Konversation.
        max_tokens (int): Maximale Anzahl der Tokens, die in der Historie erlaubt sind.
        encoding: Tokenizer für das GPT-4-Modell.
        content_list (list): Liste zum Speichern von Textinhalten und Codeblöcken.
        log_directory (str): Verzeichnis zum Speichern von Logdateien.
    """

    def __init__(self, max_tokens: int = 2048):
        """
        Initialisiert die ConversationManager-Klasse.

        :param max_tokens: Maximale Anzahl der Tokens für die Konversationshistorie.
        """
        self.conversation_history = []
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4")  # Tokenizer für das Modell
        self.content_list = []
        self.log_directory = os.path.join(os.getcwd(), 'log')

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def add_message(self, role: str, content: str) -> None:
        """
        Füge eine Nachricht zur Unterhaltung hinzu.

        :param role: Rolle des Senders (z.B. "user", "system").
        :param content: Inhalt der Nachricht.
        :return: None
        """
        self.conversation_history.append({"role": role, "content": content})
        self.trim_history()  # Kürze die Historie, falls die maximale Tokenanzahl überschritten wird

    def trim_history(self) -> None:
        """
        Kürze die Historie, um die maximale Tokenanzahl zu beachten.

        :return: None
        """
        total_tokens = sum(self.count_tokens(msg['content']) for msg in self.conversation_history)
        while total_tokens > self.max_tokens:
            removed_message = self.conversation_history.pop(0)
            total_tokens -= self.count_tokens(removed_message['content'])

    def count_tokens(self, text: str) -> int:
        """
        Zähle die Anzahl der Tokens in einem Text.

        :param text: Der Text, dessen Tokens gezählt werden sollen.
        :return: Die Anzahl der Tokens.
        """
        tokens = self.encoding.encode(text)
        return len(tokens)

    def get_history(self) -> list:
        """
        Gibt die gesamte Gesprächshistorie zurück.

        :return: Die Liste der Nachrichten in der Konversation.
        """
        return self.conversation_history

    def extract_code_blocks(self, text: str) -> tuple:
        """
        Extrahiere Codeblöcke aus dem gegebenen Text.

        Diese Methode sucht nach Codeblöcken, die mit "#Filename:" beginnen und mit "#EOF" enden.
        Zusätzlich entfernt sie Markierungen wie ```python, die eventuell von der KI-Antwort mitgesendet werden.

        :param text: Der Text, aus dem Codeblöcke extrahiert werden sollen.
        :return: Eine Liste von Codeblöcken und der verbleibende Text.
        """
        code_blocks = []
        remaining_text = text
        
        # Regex zur Suche nach Codeblöcken, die mit "#Filename:" und "#EOF" markiert sind
        while True:
            start_index = remaining_text.find("#Filename:")
            if start_index == -1:
                break
            end_index = remaining_text.find("#EOF", start_index)
            if end_index == -1:
                print("Warnung: Kein #EOF gefunden. Abbruch.")
                break
            end_index += len("#EOF")
            block = remaining_text[start_index:end_index].strip()

            # Entferne Markierungen wie ```python``` und ``` innerhalb des Codeblocks
            block = re.sub(r"```python|```", "", block)
            code_blocks.append(block)
            remaining_text = remaining_text[:start_index] + remaining_text[end_index:]

        return code_blocks, remaining_text.strip()

    def log_ki_antwort(self, generierter_code: str) -> None:
        """
        Logge die Antwort der KI in eine Datei.

        :param generierter_code: Die von der KI generierte Antwort, die geloggt werden soll.
        :return: None
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_filename = os.path.join(self.log_directory, f"ki-ausgabe.log.{timestamp}.txt")
        with open(log_filename, 'w') as log_file:
            log_file.write(generierter_code)

    def save_content(self, text: str, code_blocks: list) -> None:
        """
        Speichere den Text und die Codeblöcke.

        :param text: Der Text, der gespeichert werden soll.
        :param code_blocks: Eine Liste von Codeblöcken, die gespeichert werden sollen.
        :return: None
        """
        text = self.remove_empty_codeblocks(text)
        if text:
            self.content_list.append(("TEXT", text))
        for index, block in enumerate(code_blocks):
            self.content_list.append((f"CODE_{index + 1}", block))

    def remove_empty_codeblocks(self, text: str) -> str:
        """
        Entferne leere Codeblöcke aus dem Text.

        :param text: Der Text, aus dem leere Codeblöcke entfernt werden sollen.
        :return: Der bereinigte Text ohne leere Codeblöcke.
        """
        text = re.sub(r'```python\s*```', '', text)
        return text

# EOF
