import logging
import os

LOGGING_FILE = './logs/log.log'
LOGGING_LEVEL = logging.DEBUG


# Loggers for each module
loggers = {}


def _get_logger(module_name):
    if module_name in loggers:
        return loggers[module_name]
    
    logger = logging.getLogger(module_name)
    logger.setLevel(LOGGING_LEVEL)
    
    loggers[module_name] = logger
    return logger


def _setup_logger():
    os.makedirs(os.path.dirname(LOGGING_FILE), exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)-8s] %(name)-15s - %(message)s',
        filename=LOGGING_FILE,
        encoding='utf-8',
        level=LOGGING_LEVEL
    )
_setup_logger()

def debug(module_name, msg):
    _get_logger(module_name).debug(msg)
    
def info(module_name, msg):
    _get_logger(module_name).info(msg)
    
def warning(module_name, msg):
    _get_logger(module_name).warning(msg)
    
def error(module_name, msg):
    _get_logger(module_name).error(msg)
    
def critical(module_name, msg):
    _get_logger(module_name).critical(msg)
    
    