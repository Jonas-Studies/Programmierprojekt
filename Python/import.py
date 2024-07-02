from data_manager import importer
from settings import FIX_SUBSTANCES

import os

if __name__ == "__main__":
    if os.path.exists("./Imports"):
        files = sorted(os.listdir("./Imports"))
        for file in files:
            if file.endswith(".json"):
                importer.import_data_from_file(f"./Imports/{file}", FIX_SUBSTANCES)
            
    importer.import_data_from_caymanchem(FIX_SUBSTANCES)
    