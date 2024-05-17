import openai
import subprocess
import sys
import os
import ast
from datetime import datetime

class clApiKeyLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        with open(self.filepath, 'r') as file:
            return file.read().strip()

class clSystemMessageLoader:
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        with open(self.filepath, 'r') as file:
            return file.read().strip()

class clCodeGenerator:
    def __init__(self, api_key, system_message, directory):
        self.api_key = api_key
        self.system_message = system_message
        self.directory = directory
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            code = response.choices[0].message.content.strip()
            # Extrahiere nur den Python-Code aus dem generierten Text
            start_code = code.find("###ANFANG###")
            end_code = code.find("###ENDE###", start_code + 1)
            if start_code != -1 and end_code != -1:
                code = code[start_code + len("###ANFANG###"):end_code].strip()
                # Entferne alle zusätzlichen Texte, die nicht in den Markierungen sind
                code = code.replace("```python", "").replace("```", "").strip()
            # Füge die Interpreter-Definition hinzu
            code = "#!/usr/bin/env python3\n\n" + code
            return code
        except Exception as e:
            self.log_error(f"An error occurred: {e}")
            sys.exit(1)

    def log_error(self, message):
        log_dir = os.path.join(self.directory, "system")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "compile.log")
        with open(log_path, "a") as log_file:
            log_file.write(f"{datetime.now()} - {message}\n")

class clCodeHandler:
    def __init__(self, directory, filename="main.py"):
        self.directory = directory
        self.filename = filename
        self.filepath = os.path.join(directory, self.filename)
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save(self, code):
        with open(self.filepath, 'w') as file:
            file.write(code)

    def read(self):
        with open(self.filepath, 'r') as file:
            return file.read().strip()

    def list_files(self):
        return os.listdir(self.directory)

    def delete_files(self, files):
        for file in files:
            os.remove(os.path.join(self.directory, file))

    def rename_file(self, old_name, new_name):
        os.rename(os.path.join(self.directory, old_name), os.path.join(self.directory, new_name))

class clCodeExecutor:
    def __init__(self, filepath):
        self.filepath = filepath

    def execute(self):
        try:
            result = subprocess.run(['python3', self.filepath], capture_output=True, text=True)
            result.check_returncode()
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return e.stdout, e.stderr

class clCodeVerifier:
    def verify_function_calls(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"Syntaxfehler im generierten Code: {e}")
            return False

        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        calls = [node.func.id for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)]
        return all(func in calls for func in functions)

    def verify_main_block(self, code):
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            print(f"Syntaxfehler im generierten Code: {e}")
            return False

        for node in ast.walk(tree):
            if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
                if (isinstance(node.test.left, ast.Name) and node.test.left.id == "__name__" and
                    isinstance(node.test.ops[0], ast.Eq) and
                    isinstance(node.test.comparators[0], ast.Constant) and node.test.comparators[0].value == "__main__"):
                    return True
        return False

class clMain:
    def __init__(self, api_key_file, system_message_file, prompt, directory):
        self.api_key_file = api_key_file
        self.system_message_file = system_message_file
        self.prompt = prompt
        self.directory = directory

    def run(self):
        api_key_loader = clApiKeyLoader(self.api_key_file)
        api_key = api_key_loader.load()

        system_message_loader = clSystemMessageLoader(self.system_message_file)
        system_message = system_message_loader.load()

        code_generator = clCodeGenerator(api_key, system_message, self.directory)
        code_handler = clCodeHandler(self.directory)
        code_verifier = clCodeVerifier()

        files = code_handler.list_files()
        if "main.py" in files:
            code = code_handler.read()
        else:
            code = code_generator.generate(self.prompt)

        if "lösche alle scripts im verzeichnis" in self.prompt:
            code_handler.delete_files(files)
            print("Alle Skripte im Verzeichnis wurden gelöscht.")
            code = code_generator.generate(self.prompt)

        iteration = 0
        stderr = ""
        while True:
            iteration += 1
            print(f"Iteration {iteration}: Generating code...")

            if iteration > 1:
                self.prompt = f"Hier ist ein fehlerhaftes Python-Skript. Korrigiere es:\n\n{code}\n\nFehler: {stderr}"
                code = code_generator.generate(self.prompt)

            code_handler.save(code)

            print("Überprüfen des Codes auf Funktionsaufrufe und main-Bereich...")
            if not code_verifier.verify_function_calls(code):
                code_generator.log_error(f"Fehlender Funktionsaufruf entdeckt.")
                self.prompt = f"Hier ist ein Python-Skript mit einer Funktion, die nicht aufgerufen wird. Füge den fehlenden Funktionsaufruf hinzu:\n\n{code}"
                code = code_generator.generate(self.prompt)
                code_handler.save(code)
                continue

            if not code_verifier.verify_main_block(code):
                code_generator.log_error(f"Fehlender main-Bereich entdeckt.")
                self.prompt = f"Hier ist ein Python-Skript ohne main-Bereich. Füge den main-Bereich hinzu:\n\n{code}"
                code = code_generator.generate(self.prompt)
                code_handler.save(code)
                continue

            print("Executing code...")
            code_executor = clCodeExecutor(code_handler.filepath)
            stdout, stderr = code_executor.execute()
            if stderr:
                print(f"Fehler gefunden: {stderr}")
                code_generator.log_error(stderr)
            else:
                print(f"Ausgabe: {stdout}")
                break

            if iteration >= 10:  # Max iterations to avoid infinite loops
                print("Maximale Anzahl von Iterationen erreicht, Skript wird beendet.")
                break

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python code_generator.py <api_key_file> <system_message_file> <prompt> <directory>")
        sys.exit(1)

    api_key_file = sys.argv[1]
    system_message_file = sys.argv[2]
    prompt = sys.argv[3]
    directory = sys.argv[4]

    main = clMain(api_key_file, system_message_file, prompt, directory)
    main.run()

