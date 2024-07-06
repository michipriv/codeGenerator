# Filename: openai.py

import openai
import json
import socket

class OpenAIIntegration:
    def __init__(self, args, host, port, api_key, organization):
        openai.api_key = api_key
        openai.organization = organization
        self.client = openai
        self.server_address = (host, port)
        self.register_with_server()

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

    def generiere_code(self, gpt_assistant_prompt, gpt_user_prompt, model="gpt-4", temperature=0.2, max_tokens=256, frequency_penalty=0.0):
        """
        Generiert Programmcode basierend auf einer gegebenen Beschreibung.
        """
        try:
            messages = [
                {"role": "system", "content": gpt_assistant_prompt},
                {"role": "user", "content": gpt_user_prompt}
            ]
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            generated_code = response.choices[0].message.content
            print (generated_code)
            
            # Entferne alles vor #Filename und nach #EOF
            start_index = generated_code.find("#Filename:")
            end_index = generated_code.find("#EOF") + len("#EOF")
            if start_index != -1 and end_index != -1:
                generated_code = generated_code[start_index:end_index].strip()
            else:
                raise ValueError("System Prompt Fehler: Der generierte Code enthält nicht die erforderlichen #Filename und #EOF Marker")
            
            if not generated_code.startswith("#Filename:"):
                raise ValueError("System Prompt Fehler: Der generierte Code beginnt nicht mit #Filename:")
            if not generated_code.endswith("#EOF"):
                raise ValueError("System Prompt Fehler: Der generierte Code endet nicht mit #EOF")         
          
            self.send_message(f"message:file_manager:save:{generated_code}")
            print(f"Nachricht an Filemanager gesendet")
            return generated_code
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def create_prompt(self):
        return (
            "Verhalte dich wie ein Python-Entwickler, der objektorientiert und mit Klassen entwickelt. "
            "Bei der Antwort füge im Codeblock immer die Zeile mit: #Filename ein, das ist extrem wichtig für die Zuordnung. "
            "Antworte nur mit Code, und achte darauf, dass der Code mit #Filename beginnt und mit #EOF endet. Lasse jede Erklärung weg."
            "das hauptprogramm heist immer main.py"
            "Klassen werden im verzeichnis module abgespeichert"
        )
    
    

    def run_interactive_mode(self):
        """
        Führt den interaktiven Modus für die OpenAI-Integration aus.
        """
        try:
            while True:
                gpt_assistant_prompt = self.create_prompt()
    
                
                gpt_user_prompt = input("Was soll ich tun? ")
                generierter_code = self.generiere_code(gpt_assistant_prompt, gpt_user_prompt)
                print(f"Generierter Code:\n{generierter_code}")
    
                # Sende den generierten Code an den FileManager und löse das Speichern aus
                self.send_message(f"save:{generierter_code}")
    
        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")




#EOF