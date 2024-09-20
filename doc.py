# Filename: doc.py
import ast
import os
import sys

def extract_classes_funcs(file_path):
    """
    Extrahiert Klassen, Methoden und deren Parameter sowie Docstrings aus einer Python-Datei.

    Parameters:
        file_path (str): Der Pfad zur Python-Datei, die analysiert werden soll.

    Returns:
        list: Eine Liste von Dictionaries, die die Klassen, deren Methoden, 
              die zugehörigen Parameter und die Docstrings enthalten.
    """
    try:
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
    except SyntaxError:
        print(f"Syntaxfehler beim Parsen der Datei: {file_path}")
        return []  # Ignoriere diese Datei bei Fehlern

    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = []
            class_doc = ast.get_docstring(node)  # Extrahiere den Docstring der Klasse
            for n in node.body:
                if isinstance(n, ast.FunctionDef):
                    # Extrahiere die Namen der Argumente und den Docstring der Methode
                    params = [arg.arg for arg in n.args.args]
                    method_doc = ast.get_docstring(n)
                    methods.append({
                        "method": n.name,
                        "params": params,
                        "docstring": method_doc
                    })
            classes.append({
                "class": node.name,
                "docstring": class_doc,
                "methods": methods
            })
    return classes

def scan_directory(path):
    """
    Durchsucht das Verzeichnis nach Python-Dateien.

    Parameters:
        path (str): Der Pfad zum Verzeichnis, das durchsucht werden soll.

    Returns:
        list: Eine Liste von Pfaden zu den gefundenen Python-Dateien.
    """
    return [os.path.join(root, file) for root, _, files in os.walk(path) for file in files if file.endswith(".py")]

def generate_overview(path):
    """
    Erzeugt eine Übersicht der Klassen, Methoden, deren Parameter und Docstrings pro Datei
    und speichert diese in einem Dictionary.

    Parameters:
        path (str): Der Pfad zum Verzeichnis, das durchsucht werden soll.

    Returns:
        dict: Ein Dictionary, das die Klassen, Methoden, Parameter und Docstrings pro Datei enthält.
    """
    overview = {}
    for py_file in scan_directory(path):
        classes = extract_classes_funcs(py_file)
        if classes:
            overview[py_file] = classes
    return overview

def save_as_md(overview, output_file):
    """
    Speichert die Übersicht in einer menschenlesbaren Markdown-Datei.

    Parameters:
        overview (dict): Die Übersicht der Klassen, Methoden und Parameter.
        output_file (str): Der Pfad zur Ausgabedatei.
    """
    with open(output_file, 'w') as f:
        for file_path, classes in overview.items():
            f.write(f"# Datei: {file_path}\n")
            for cls in classes:
                f.write(f"  ## Klasse: {cls['class']}\n")
                if cls['docstring']:
                    f.write(f"    Docstring: {cls['docstring']}\n")
                for method in cls['methods']:
                    params_str = ", ".join(method['params'])
                    f.write(f"    ### Methode: {method['method']}({params_str})\n")
                    if method['docstring']:
                        f.write(f"      Docstring: {method['docstring']}\n")
            f.write("\n")

def save_as_html(overview, output_file):
    """
    Speichert die Übersicht in einer HTML-Datei.

    Parameters:
        overview (dict): Die Übersicht der Klassen, Methoden und Parameter.
        output_file (str): Der Pfad zur Ausgabedatei.
    """
    with open(output_file, 'w') as f:
        f.write("<html><body>\n")
        f.write("<h1>Klassenübersicht</h1>\n")
        for file_path, classes in overview.items():
            f.write(f"<h2>Datei: {file_path}</h2>\n")
            for cls in classes:
                f.write(f"<h3>Klasse: {cls['class']}</h3>\n")
                if cls['docstring']:
                    f.write(f"<p>Docstring: {cls['docstring']}</p>\n")
                for method in cls['methods']:
                    params_str = ", ".join(method['params'])
                    f.write(f"<p>Methode: {method['method']}({params_str})</p>\n")
                    if method['docstring']:
                        f.write(f"<p>Docstring: {method['docstring']}</p>\n")
        f.write("</body></html>")

def print_help():
    """
    Zeigt die Hilfe an, die die Optionen für den Programmaufruf beschreibt.
    """
    help_text = """
    Nutzung:
      python doc.py [-p] [-h] [-?]
    
    Optionen:
      -p    Ausgabe in menschenlesbarer Form auf der Konsole und als Markdown speichern.
      -h    Ausgabe in HTML speichern.
      -?    Diese Hilfe anzeigen.
    """
    print(help_text)

# Hauptfunktion, die den normalen Aufruf und die Optionen -p, -h und -? unterscheidet
def main():
    #project_path = "/mnt/c/tmp/codeGenerator"
    project_path = "./"
    md_output_file = "docu.MD"
    html_output_file = "docu.html"

    # Zeige immer den Hinweis auf die Hilfe an
    print("Für Hilfe verwenden Sie die Option -?")

    # Generiere die Übersicht als Dictionary
    overview = generate_overview(project_path)

    # Prüfe auf verschiedene Flags
    if "-?" in sys.argv:
        print_help()
    elif "-p" in sys.argv:
        # Ausgabe in menschenlesbarer Form
        print("Ausgabe in menschenlesbarer Form:")
        for file_path, classes in overview.items():
            print(f"Datei: {file_path}")
            for cls in classes:
                print(f"  Klasse: {cls['class']}")
                if cls['docstring']:
                    print(f"    Docstring: {cls['docstring']}")
                for method in cls['methods']:
                    params_str = ", ".join(method['params'])
                    print(f"    Methode: {method['method']}({params_str})")
                    if method['docstring']:
                        print(f"      Docstring: {method['docstring']}")
            print()

        # Speichere als Markdown
        save_as_md(overview, md_output_file)
        print(f"Die Markdown-Datei '{md_output_file}' wurde erzeugt.")

    elif "-h" in sys.argv:
        # Speichere als HTML
        save_as_html(overview, html_output_file)
        print(f"Die HTML-Datei '{html_output_file}' wurde erzeugt.")
    else:
        # Standard: Speichere nur als Markdown
        save_as_md(overview, md_output_file)
        print(f"Die Markdown-Datei '{md_output_file}' wurde erzeugt.")

if __name__ == "__main__":
    main()
#EOF
