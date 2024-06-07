# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:05:45 2024

@author: m.mader
"""

"""

CodeEvolver/
│
├── main.py                 # Hauptskript, das die Anwendung startet.
├── code/                   # Verzeichnis für den von der KI generierten oder geladenen Code.
│
└── classes/
    ├── benutzer_interface.py  # Implementierung der Benutzerinteraktion.
    ├── openai_integration.py  # Verwaltet Kommunikation mit der OpenAI API.
    ├── programm_manager.py    # Hauptlogik für Programmverwaltung.
    ├── code_ausfuehrer.py     # Führt generierten oder geladenen Code aus.
    └── daten_speicher.py      # Verwaltet das Laden und Speichern von Code.

"""

from classes.benutzer_interface import BenutzerInterface
from classes.openai_integration import OpenAIIntegration
from classes.programm_manager import ProgrammManager
from classes.code_ausfuehrer import CodeAusfuehrer
from classes.daten_speicher import DatenSpeicher

def main():
    # Ersetze 'dein_api_schluessel' mit deinem tatsächlichen OpenAI API-Schlüssel
    api_schluessel = "hier einfügen "
    
    # Instanzen der Komponenten erstellen
    benutzer_interface = BenutzerInterface()
    openai_integration = OpenAIIntegration(api_schluessel)
    daten_speicher = DatenSpeicher()
    code_ausfuehrer = CodeAusfuehrer()
    
    # ProgrammManager mit allen benötigten Komponenten initialisieren
    programm_manager = ProgrammManager(benutzer_interface, openai_integration, daten_speicher, code_ausfuehrer)
    
    # Start der Anwendung
    while True:
        beschreibung = benutzer_interface.erfasse_beschreibung()
        if beschreibung.lower() == 'beenden':
            print("Anwendung wird beendet.")
            break
        
        programm_manager.verarbeite_beschreibung(beschreibung)

if __name__ == "__main__":
    main()
