# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:18:21 2024

@author: m.mader
"""

import os

class DatenSpeicher:
    def __init__(self, basis_verzeichnis="code"):
        """
        Initialisiert den DatenSpeicher mit dem Basisverzeichnis für die Code-Dateien.
        """
        self.basis_verzeichnis = basis_verzeichnis
        # Stellt sicher, dass das Verzeichnis existiert
        os.makedirs(self.basis_verzeichnis, exist_ok=True)

    def speichere_code(self, programm_name, code):
        """
        Speichert den gegebenen Code unter dem angegebenen Programmnamen.
        """
        dateipfad = os.path.join(self.basis_verzeichnis, programm_name + ".py")
        with open(dateipfad, 'w', encoding='utf-8') as datei:
            datei.write(code)
        print(f"Code gespeichert unter: {dateipfad}")

    def lade_code(self, programm_name):
        """
        Lädt den Code des angegebenen Programmnamens.
        """
        dateipfad = os.path.join(self.basis_verzeichnis, programm_name + ".py")
        try:
            with open(dateipfad, 'r', encoding='utf-8') as datei:
                code = datei.read()
            return code
        except FileNotFoundError:
            print(f"Datei {dateipfad} nicht gefunden.")
            return None
