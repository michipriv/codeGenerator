#Filename: logger.py

import logging
import sys
import os

class Logger:
    def __init__(self, log_file='log/app.log'):
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
        def __init__(self, logger, log_level):
            self.logger = logger
            self.log_level = log_level
            self.linebuf = ''

        def write(self, buf):
            for line in buf.rstrip().splitlines():
                self.logger.log(self.log_level, line.rstrip())

        def flush(self):
            pass

    def get_logger(self):
        return self.logger



#EOF