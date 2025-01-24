#!/bin/bash

# Überprüfen, ob ein Verzeichnisname übergeben wurde
if [ -z "$1" ]; then
    echo "Bitte einen Verzeichnisnamen als Argument übergeben."
    echo "./start.sh finetuning"
    exit 1
fi

# Das übergebene Verzeichnis als Variable speichern
VERZ_NAME=$1

# Startet das Python-Skript im Hintergrund
python3 main.py -s &

# Zurück ins übergeordnete Verzeichnis wechseln
cd ..

# Erstellen des neuen Verzeichnisses
mkdir "$VERZ_NAME"

# Wechseln in das neue Verzeichnis
cd "$VERZ_NAME"

# Aufruf des zweiten Python-Skripts mit den entsprechenden Parametern
python3 ../codeGenerator/main.py -d main.py

