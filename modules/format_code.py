# Filename: modules/format_code.py

import re

class FormatCode:
    def format_code(self, code):
        try:
            import black
            formatted_code = black.format_str(code, mode=black.Mode())
            return formatted_code
        except ImportError:
            print("Fehler: Das Modul 'black' ist nicht installiert. Der Code wird unformatiert gespeichert.")
            return code
        except black.InvalidInput:
            print("Fehler: Der Code konnte nicht formatiert werden. Der Code wird unformatiert gespeichert.")
            return code
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
            return code

    def extract_filename(self, code):
        match = re.search(r'# ?[Ff]ilename: (.+)', code)
        if match:
            return match.group(1).strip()
        return None

#EOF
