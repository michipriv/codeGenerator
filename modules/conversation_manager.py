# Filename: modules/conversation_manager.py

import tiktoken
import os
from datetime import datetime

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

    def __init__(self, max_tokens=2048):
        """
        Initialisiert die ConversationManager-Klasse.

        Parameters:
            max_tokens (int): Maximale Anzahl der Tokens für die Konversationshistorie.
        """
        self.conversation_history = []
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4")  # Tokenizer für das Modell
        self.content_list = []
        self.log_directory = os.path.join(os.getcwd(), 'log')

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def add_message(self, role, content):
        """
        Füge eine Nachricht zur Unterhaltung hinzu.

        Parameters:
            role (str): Rolle des Senders (z.B. "user", "system").
            content (str): Inhalt der Nachricht.
        """
        self.conversation_history.append({"role": role, "content": content})
        self.trim_history()  # Kürze die Historie, falls die maximale Tokenanzahl überschritten wird

    def trim_history(self):
        """
        Kürze die Historie, um die maximale Tokenanzahl zu beachten.
        """
        total_tokens = sum(self.count_tokens(msg['content']) for msg in self.conversation_history)
        while total_tokens > self.max_tokens:
            removed_message = self.conversation_history.pop(0)
            total_tokens -= self.count_tokens(removed_message['content'])

    def count_tokens(self, text):
        """
        Zähle die Anzahl der Tokens in einem Text.

        Parameters:
            text (str): Der Text, dessen Tokens gezählt werden sollen.

        Returns:
            int: Die Anzahl der Tokens.
        """
        tokens = self.encoding.encode(text)
        return len(tokens)

    def get_history(self):
        """
        Gibt die gesamte Gesprächshistorie zurück.

        Returns:
            list: Die Liste der Nachrichten in der Konversation.
        """
        return self.conversation_history

    def extract_code_blocks(self, text):
        """
        Extrahiere Codeblöcke aus dem gegebenen Text.

        Parameters:
            text (str): Der Text, aus dem Codeblöcke extrahiert werden sollen.

        Returns:
            tuple: Eine Liste von Codeblöcken und der verbleibende Text.
        """
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
        """
        Logge die Antwort der KI in eine Datei.

        Parameters:
            generierter_code (str): Die von der KI generierte Antwort, die geloggt werden soll.
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_filename = os.path.join(self.log_directory, f"ki-ausgabe.log.{timestamp}.txt")
        with open(log_filename, 'w') as log_file:
            log_file.write(generierter_code)

    def save_content(self, text, code_blocks):
        """
        Speichere den Text und die Codeblöcke.

        Parameters:
            text (str): Der Text, der gespeichert werden soll.
            code_blocks (list): Eine Liste von Codeblöcken, die gespeichert werden sollen.
        """
        text = self.remove_empty_codeblocks(text)
        if text:
            self.content_list.append(("TEXT", text))
        for index, block in enumerate(code_blocks):
            self.content_list.append((f"CODE_{index + 1}", block))

    def remove_empty_codeblocks(self, text):
        """
        Entferne leere Codeblöcke aus dem Text.

        Parameters:
            text (str): Der Text, aus dem leere Codeblöcke entfernt werden sollen.

        Returns:
            str: Der bereinigte Text ohne leere Codeblöcke.
        """
        import re
        text = re.sub(r'```python\s*```', '', text)
        return text

# EOF
