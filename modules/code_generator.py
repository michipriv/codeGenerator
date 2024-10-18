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

    def __init__(self, api_key: str, organization: str):
        """
        Initialisiert die CodeGenerator-Klasse.

        :param api_key: Der API-Schlüssel für die OpenAI-Integration.
        :param organization: Die Organisation für die OpenAI-Integration.
        """
        openai.api_key = api_key
        openai.organization = organization

    def generiere_code(self, messages: list, model: str = "gpt-4", temperature: float = 0.2, max_tokens: int = 4096, frequency_penalty: float = 0.2) -> str:
        """
        Generiert Code basierend auf den übergebenen Nachrichten.

        :param messages: Eine Liste von Nachrichten, die als Eingabe an das Modell gesendet werden.
        :param model: Das verwendete Modell. Standardmäßig "gpt-4".
        :param temperature: Steuerung der Kreativität der Ausgabe. Standardmäßig 0.2.
        :param max_tokens: Maximale Anzahl der Tokens für die Antwort. Standardmäßig 4096.
        :param frequency_penalty: Bestrafung für die Wiederholung von Tokens. Standardmäßig 0.2.
        :return: Der generierte Code oder None, wenn ein Fehler auftritt.
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
