from data_manager import importer
from settings import FIX_SUBSTANCES

import os

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Imports')
    if os.path.exists(path):
        files = sorted(os.listdir(path))
        for file in files:
            if file.endswith(".json"):
                importer.import_data_from_file(os.path.join(path, file), FIX_SUBSTANCES)
            
    importer.import_data_from_caymanchem(FIX_SUBSTANCES)
    