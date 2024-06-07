# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:18:00 2024

@author: m.mader
"""

class CodeAusfuehrer:
    def execute_code(self, code):
        """
        Führt den gegebenen Code aus und fängt mögliche Laufzeitfehler ab.
        
        :param code: Der auszuführende Code als String.
        :return: Ein Tupel (erfolg, ergebnis/fehlermeldung).
                 'erfolg' ist ein Boolean, der angibt, ob die Ausführung erfolgreich war.
                 'ergebnis/fehlermeldung' ist das Ergebnis der Ausführung oder eine Fehlermeldung.
        """
        try:
            # Umgebungs-Dictionary zur sicheren Ausführung
            lokale_umgebung = {}
            exec(code, {"__builtins__": {}}, lokale_umgebung)
            return True, "Code erfolgreich ausgeführt."
        except Exception as e:
            return False, str(e)
