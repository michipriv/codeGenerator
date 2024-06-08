#Filename: README.md

verhalte dich wie ein Python entwickler der  objektorient und Klassen entwickelt.
Ich poste dir nun einen Code der aus mehreren klassen besteht.
Lies den code nur ein und warte auf mein coewort
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



erstelle nun eine eigene openai kiklasse, sie dir obigen code an verwende diese api aufrufe, lesse das secerte aus der json datei aus
ich starte die openai klasse übr main ine einr eognen gensfertt und kommuniziere dort.
ddas ergebniss osl per wserve an die filemanger klasse gesendet werden