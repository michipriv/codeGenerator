# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:17:44 2024

@author: m.mader
"""

class ProgrammManager:
    def __init__(self, benutzer_interface, openai_integration, daten_speicher, code_ausfuehrer):
        self.benutzer_interface = benutzer_interface
        self.openai_integration = openai_integration
        self.daten_speicher = daten_speicher
        self.code_ausfuehrer = code_ausfuehrer

    def verarbeite_beschreibung(self, beschreibung):
        """
        Verarbeitet die vom Benutzer eingegebene Beschreibung, um Code zu generieren oder zu laden.
        """
        # Beispiellogik, um zu entscheiden, ob ein Programm geladen oder neuer Code generiert werden soll
        if beschreibung.startswith("Lade Programm:"):
            programm_name = beschreibung[len("Lade Programm:"):].strip()
            code = self.lade_programm(programm_name)
            if code:
                self.benutzer_interface.zeige_ergebnis(code)
            else:
                self.benutzer_interface.zeige_fehler("Programm konnte nicht geladen werden.")
        else:
            generierter_code = self.openai_integration.generiere_code(beschreibung)
            if generierter_code:
                self.benutzer_interface.zeige_ergebnis(generierter_code)
                # Optional: Speichern des generierten Codes
            else:
                self.benutzer_interface.zeige_fehler("Code konnte nicht generiert werden.")

    def lade_programm(self, programm_name):
        """
        Lädt ein gespeichertes Programm aus dem Speicher.
        """
        code = self.daten_speicher.lade_code(programm_name)
        return code

    def speichere_programm(self, programm_name, code):
        """
        Speichert den generierten oder korrigierten Code.
        """
        self.daten_speicher.speichere_code(programm_name, code)

    def fuehre_programm_aus(self, code):
        """
        Führt den generierten oder geladenen Code aus.
        """
        ergebnis, fehlermeldung = self.code_ausfuehrer.execute_code(code)
        if fehlermeldung:
            self.benutzer_interface.zeige_fehler(fehlermeldung)
            # Optional: Korrektur des Codes bei Fehler
        else:
            self.benutzer_interface.zeige_ergebnis(ergebnis)

    def behandele_fehler(self, code, fehlermeldung):
        """
        Versucht, den Code basierend auf einer gegebenen Fehlermeldung zu korrigieren.
        """
        korrigierter_code = self.openai_integration.korrigiere_code(code, fehlermeldung)
        if korrigierter_code:
            self.benutzer_interface.zeige_ergebnis(korrigierter_code)
            # Optional: Erneutes Ausführen des korrigierten Codes
        else:
            self.benutzer_interface.zeige_fehler("Code konnte nicht korrigiert werden.")
