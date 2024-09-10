import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file='app.log', log_level=logging.DEBUG, name: str = ""):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s', '%Y-%m-%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=3)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger