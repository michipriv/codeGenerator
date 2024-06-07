# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:05:56 2024

@author: m.mader
"""

import openai

class OpenAIIntegration:
    def __init__(self, api_key):
        """
        Initialisiert die OpenAIIntegration mit dem gegebenen API-Schlüssel.
        """
        self.api_key = api_key
        openai.api_key = self.api_key

    def generiere_code(self, beschreibung, engine="code-davinci-002", temperatur=0.5, max_tokens=100):
        """
        Generiert Programmcode basierend auf einer gegebenen Beschreibung.
        """
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=beschreibung,
                temperature=temperatur,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                language="python"
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None

    def korrigiere_code(self, code, fehlermeldung, engine="code-davinci-002", temperatur=0.5, max_tokens=100):
        """
        Versucht, den gegebenen Code basierend auf einer Fehlermeldung zu korrigieren.
        """
        korrektur_prompt = f"Korrigiere diesen Code basierend auf der Fehlermeldung:\nCode:\n{code}\nFehlermeldung:\n{fehlermeldung}\nKorrigierter Code:"
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=korrektur_prompt,
                temperature=temperatur,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                language="python"
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None
