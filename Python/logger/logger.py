import logging
import os

from settings import LOGGING_FILE, LOGGING_LEVEL

def setup_logger():
    os.makedirs(os.path.dirname(LOGGING_FILE), exist_ok=True)
    logging.basicConfig(
        format='%(asctime)s [%(levelname)-8s] %(name)-15s - %(message)s',
        filename=LOGGING_FILE,
        encoding='utf-8',
        level=LOGGING_LEVEL
    )
    logging.getLogger().setLevel(LOGGING_LEVEL)
setup_logger()
