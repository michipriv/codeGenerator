# Filename: modules/conversation_manager.py

import tiktoken
import os
from datetime import datetime

class ConversationManager:
    def __init__(self, max_tokens=2048):
        self.conversation_history = []
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4o")
        self.content_list = []
        self.log_directory = os.path.join(os.getcwd(), 'log')

        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        self.trim_history()

    def trim_history(self):
        total_tokens = sum(self.count_tokens(msg['content']) for msg in self.conversation_history)
        while total_tokens > self.max_tokens:
            removed_message = self.conversation_history.pop(0)
            total_tokens -= self.count_tokens(removed_message['content'])

    def count_tokens(self, text):
        tokens = self.encoding.encode(text)
        return len(tokens)

    def get_history(self):
        return self.conversation_history

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
        log_filename = os.path.join(self.log_directory, f"ki-ausgabe.log.{timestamp}.txt")
        with open(log_filename, 'w') as log_file:
            log_file.write(generierter_code)

    def save_content(self, text, code_blocks):
        text = self.remove_empty_codeblocks(text)
        if text:
            self.content_list.append(("TEXT", text))
        for index, block in enumerate(code_blocks):
            self.content_list.append((f"CODE_{index + 1}", block))
    
    def remove_empty_codeblocks(self, text):
        import re
        text = re.sub(r'```python\s*```', '', text)
        return text

#EOF
