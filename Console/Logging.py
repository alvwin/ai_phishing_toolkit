import logging
import logging.config

class LoggingConfig:
    def __init__(self, log_file='app.log', log_level=logging.DEBUG):
        self.log_file = log_file
        self.log_level = log_level
        self.setup_logging()

    def setup_logging(self):
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                },
            },
            'handlers': {
                'console': {
                    'level': self.log_level,
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard',
                },
                'file': {
                    'level': self.log_level,
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': self.log_file,
                    'maxBytes': 10485760,
                    'backupCount': 3,
                    'formatter': 'standard',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file'],
                    'level': self.log_level,
                    'propagate': True,
                },
            }
        }
        logging.config.dictConfig(logging_config)

    def set_log_level(self, level):
        """Method to change the log level dynamically."""
        logging.getLogger().setLevel(level)
        for handler in logging.getLogger().handlers:
            handler.setLevel(level)
    
    def add_handler(self, handler):
        """Method to add a new handler dynamically."""
        logging.getLogger().addHandler(handler)
