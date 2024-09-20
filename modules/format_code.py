# Filename: modules/format_code.py

import re

class FormatCode:
    """
    Klasse zur Formatierung von Code und zur Extraktion von Dateinamen.

    Diese Klasse verwendet das 'black'-Modul zur Formatierung von Python-Code
    und stellt Methoden zur Verfügung, um Dateinamen aus Kommentaren im Code
    zu extrahieren.

    Attributes:
        None
    """

    def format_code(self, code):
        """
        Formatiert den gegebenen Code mit dem 'black'-Formatter.

        Parameters:
            code (str): Der zu formatierende Python-Code.

        Returns:
            str: Der formatierte Code oder der ursprüngliche Code, 
                  falls das Formatieren nicht möglich war.
        """
        try:
            import black
            # Versuche, den Code mit black zu formatieren
            formatted_code = black.format_str(code, mode=black.Mode())
            return formatted_code
        except ImportError:
            # Falls black nicht installiert ist, gebe eine Warnung aus und speichere den Code trotzdem
            print("Warnung: Das Modul 'black' ist nicht installiert. Der Code wird unformatiert gespeichert.")
            return code
        except black.InvalidInput:
            # Falls der Code nicht formatiert werden kann, speichere ihn trotzdem
            print("Fehler: Der Code konnte nicht formatiert werden. Der Code wird unformatiert gespeichert.")
            return code
        except Exception as e:
            # Unerwarteter Fehler, speichere den Code trotzdem
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return code

    def extract_filename(self, code):
        """
        Extrahiert den Dateinamen aus dem gegebenen Code.

        Sucht nach einem Kommentar im Format '# Filename: <Dateiname>' oder
        '# filename: <Dateiname>' und gibt den Dateinamen zurück.

        Parameters:
            code (str): Der Code, aus dem der Dateiname extrahiert werden soll.

        Returns:
            str: Der extrahierte Dateiname oder None, wenn kein Dateiname gefunden wurde.
        """
        # Verwende ein Regex, um den Dateinamen zu extrahieren
        match = re.search(r'# ?[Ff]ilename: (.+)', code)
        if match:
            return match.group(1).strip()
        return None

# EOF
