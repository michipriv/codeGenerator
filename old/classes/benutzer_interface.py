# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:17:00 2024

@author: m.mader
"""

class BenutzerInterface:
    def erfasse_beschreibung(self):
        """
        Fordert den Benutzer auf, eine Beschreibung für die Codegenerierung einzugeben.
        """
        print("Bitte geben Sie eine Beschreibung für den zu generierenden Code ein (oder 'beenden' zum Beenden):")
        beschreibung = input()
        return beschreibung

    def zeige_ergebnis(self, ergebnis):
        """
        Zeigt das Ergebnis der Codegenerierung oder -korrektur an.
        """
        print("Ergebnis:\n" + ergebnis)

    def zeige_fehler(self, fehlermeldung):
        """
        Zeigt eine Fehlermeldung an.
        """
        print("Fehler: " + fehlermeldung)
