#Filename: openai.py


import openai
import json

class OpenAIIntegration:
    def __init__(self, config_path):
        """
        Initialisiert die OpenAIIntegration mit dem API-Schlüssel und der Organisation aus der Konfigurationsdatei.
        """
        self.config = self.lese_konfiguration(config_path)
        openai.api_key = self.config["openai_api_key"]
        self.client = openai

    def lese_konfiguration(self, config_path):
        """
        Liest die Konfiguration aus einer JSON-Datei.
        """
        with open(config_path, 'r') as file:
            return json.load(file)

    def generiere_code(self, gpt_assistant_prompt, gpt_user_prompt, model="gpt-4", temperatur=0.2, max_tokens=256, frequency_penalty=0.0):
        """
        Generiert Programmcode basierend auf einer gegebenen Beschreibung.
        """
        try:
            messages = [
                {"role": "system", "content": gpt_assistant_prompt},
                {"role": "user", "content": gpt_user_prompt}
            ]
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperatur,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            return response.choices[0].message
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def run_interactive_mode(self):
        """
        Führt den interaktiven Modus für die OpenAI-Integration aus.
        """
        try:
            while True:
                gpt_assistant_prompt = "You are a " + input("Who should I be, as I answer your prompt? ")
                gpt_user_prompt = input("What prompt do you want me to do? ")
                gpt_prompt = (gpt_assistant_prompt, gpt_user_prompt)
                print(gpt_prompt)
                
                generierter_code = self.generiere_code(gpt_assistant_prompt, gpt_user_prompt)
                print(f"Generierter Code:\n{generierter_code}")
        except KeyboardInterrupt:
            print("\nProgramm wurde beendet.")
