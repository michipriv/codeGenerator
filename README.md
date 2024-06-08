#Filename: README.md

verhalte dich wie ein Python entwickler der  objektorient und Klassen entwickelt.
Ich poste dir nun einen Code den du einliest und du versehen lernst.
Wenn ich fertig bin schreibe ich dir das wort Bingo.


die verzeichniss struktur sieht so aus:
Unter modules liegen die klassen
codeGenerator/
│
├── main.py
├── modules/
│   ├── __init__.py
│   ├── file_operations.py
│   ├── backup_manager.py
│   ├── utils.py
│   ├── logger.py
│   ├── run.py
│   └── server.py
│   └── file_manager.py



#virutelle Umgebung für modul installion erzeugen:

python3 -m venv myenv
source myenv/bin/activate


# github einchecken
git add .
git commit -m "."
git push


# programm starten
python3 main.py  -r  test.py
python3 main.py  -d  test.py