import logging
from pythonjsonlogger import jsonlogger
from .config import Settings

def init_logger(settings: Settings):
    logger = logging.getLogger()

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    
    logger.addHandler(logHandler)
    logger.setLevel(settings.LOG_LEVEL)

    return logger
