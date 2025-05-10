import logging
import time

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            # Configuration du logger
            cls._instance.logger = logging.getLogger('newsandie')
            cls._instance.logger.setLevel(logging.DEBUG)

            # Configuration du formateur
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Gestionnaire pour les logs dans un fichier
            timestamp = time.time()
            file_handler = logging.FileHandler( ".\\" + 'newsandie_'+ str(timestamp) +'.log')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)

            # Gestionnaire pour les logs sur la console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.ERROR)
            console_handler.setFormatter(formatter)

            # Ajout des gestionnaires au logger
            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(console_handler)
        return cls._instance

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


