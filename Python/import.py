from data_manager import importer

import os


FIX_SUBSTANCES = True


if __name__ == "__main__":
    files = os.listdir("./Imports")
    for file in files:
        if file.endswith(".json"):
            importer.import_data_from_file(f"./Imports/{file}", FIX_SUBSTANCES)
            
    importer.import_data_from_caymanchem(FIX_SUBSTANCES)
    