# Filename: modules/logger.py

import logging
import sys
import os

class Logger:
    """
    Klasse zur Protokollierung von Ereignissen in einer Anwendung.

    Diese Klasse konfiguriert den Logger, um Nachrichten in eine Logdatei zu schreiben
    und umgeleitete Standardausgaben zu protokollieren.

    Attributes:
        logger (Logger): Die Logger-Instanz.
    """

    def __init__(self, log_file='log/app.log'):
        """
        Initialisiert die Logger-Klasse.

        Parameters:
            log_file (str): Der Pfad zur Logdatei. Standardmäßig 'log/app.log'.
        """
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self.logger = logging.getLogger('RunLogger')
        self.logger.setLevel(logging.DEBUG)

        # Datei-Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Formatierung
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Hinzufügen der Handler zum Logger
        self.logger.addHandler(file_handler)

        # Umleitung der Standardausgaben und Fehlerausgaben
        sys.stdout = self.StreamToLogger(self.logger, logging.INFO)
        sys.stderr = self.StreamToLogger(self.logger, logging.ERROR)

    class StreamToLogger:
        """
        Hilfsklasse zum Umleiten von Standardausgaben an den Logger.

        Attributes:
            logger (Logger): Die Logger-Instanz.
            log_level (int): Der Log-Level für die Umleitung.
            linebuf (str): Buffer für die Zeilen, die geschrieben werden.
        """

        def __init__(self, logger, log_level):
            """
            Initialisiert die StreamToLogger-Klasse.

            Parameters:
                logger (Logger): Die Logger-Instanz.
                log_level (int): Der Log-Level für die Umleitung.
            """
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            """
            Schreibt den gegebenen Puffer in den Logger.

            Parameters:
                buf (str): Der Puffer mit den zu protokollierenden Nachrichten.
            """
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            """Stellt sicher, dass alle gepufferten Ausgaben geschrieben werden."""
            pass

    def get_logger(self):
        """
        Gibt die Logger-Instanz zurück.

        Returns:
            Logger: Die Logger-Instanz.
        """
        return self.logger

#EOF
