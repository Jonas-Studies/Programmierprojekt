import logging
import sys
import os

from settings import LOGGING_LEVEL


# Log uncaught exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
sys.excepthook = handle_exception


# Configure logging
path = os.path.join(os.path.dirname(__file__), '../../Logs/log.log')
os.makedirs(os.path.dirname(path), exist_ok=True)
logging.basicConfig(
    format='%(asctime)s [%(levelname)-8s] %(name)-15s - %(message)s',
    filename=path,
    encoding='utf-8',
    level=LOGGING_LEVEL
)
logging.getLogger().setLevel(LOGGING_LEVEL)
