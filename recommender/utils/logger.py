import logging
import os.path


class Logger:
    def __init__(self, log_file_name):
        self.logger = logging.getLogger(log_file_name)
        self.logger.setLevel(logging.INFO)
        # Create file handler which logs even debug messages
        log_file_path = os.path.join("logs/" + log_file_name)
        fh = logging.FileHandler(log_file_path)
        fh.setLevel(logging.DEBUG)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(fh)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
