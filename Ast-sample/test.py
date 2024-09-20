import ast
import marshal

# Definiere den Python-Code als String
code = """
print('Hello, World!')
"""

# Parse den Code in einen AST
parsed_code = ast.parse(code)

# Kompiliere den AST zu ausführbarem Code
compiled_code = compile(parsed_code, filename="<ast>", mode="exec")

# Speichere den kompilierten Code in einer Datei
with open("test.bin", "wb") as f:
    marshal.dump(compiled_code, f)

print("Code wurde kompiliert und gespeichert.")
