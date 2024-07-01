import logging
import sys
import os

from settings import LOGGING_FILE, LOGGING_LEVEL

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
sys.excepthook = handle_exception


os.makedirs(os.path.dirname(LOGGING_FILE), exist_ok=True)
logging.basicConfig(
    format='%(asctime)s [%(levelname)-8s] %(name)-15s - %(message)s',
    filename=LOGGING_FILE,
    encoding='utf-8',
    level=LOGGING_LEVEL
)
logging.getLogger().setLevel(LOGGING_LEVEL)
