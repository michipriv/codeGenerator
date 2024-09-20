# Filename: modules/code_generator.py

import openai

class CodeGenerator:
    """
    Klasse zur Generierung von Code mithilfe der OpenAI API.

    Diese Klasse ermöglicht es, Anfragen an die OpenAI API zu stellen und
    generierten Code zurückzugeben.

    Attributes:
        api_key (str): Der API-Schlüssel für die OpenAI-Integration.
        organization (str): Die Organisation für die OpenAI-Integration.
    """

    def __init__(self, api_key, organization):
        """
        Initialisiert die CodeGenerator-Klasse.

        Parameters:
            api_key (str): Der API-Schlüssel für die OpenAI-Integration.
            organization (str): Die Organisation für die OpenAI-Integration.
        """
        openai.api_key = api_key
        openai.organization = organization

    def generiere_code(self, messages, model="gpt-4", temperature=0.2, max_tokens=4096, frequency_penalty=0.2):
        """
        Generiert Code basierend auf den übergebenen Nachrichten.

        Parameters:
            messages (list): Eine Liste von Nachrichten, die als Eingabe an das Modell gesendet werden.
            model (str): Das verwendete Modell. Standardmäßig "gpt-4".
            temperature (float): Steuerung der Kreativität der Ausgabe. Standardmäßig 0.2.
            max_tokens (int): Maximale Anzahl der Tokens für die Antwort. Standardmäßig 4096.
            frequency_penalty (float): Bestrafung für die Wiederholung von Tokens. Standardmäßig 0.2.

        Returns:
            str: Der generierte Code oder None, wenn ein Fehler auftritt.
        """
        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                frequency_penalty=frequency_penalty
            )
            generated_code = response.choices[0].message.content
            return generated_code
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

#EOF
