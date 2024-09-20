import marshal

# Lade den kompilierten Code aus der Datei
with open("test.bin", "rb") as f:
    compiled_code = marshal.load(f)

# Führe den kompilierten Code aus
exec(compiled_code)
