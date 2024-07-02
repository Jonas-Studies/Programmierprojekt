from database import database
from settings import FORMAT_EXPORT
from logger import logger

import logging
import json
import os


def export_data(path: str, only_from_caymanchem: bool = False):
    """Export substances to a JSON file in the 'Exports' folder.
    """
    if only_from_caymanchem:
        substances = database.get_activeSubstances_by_sourceName("Caymanchem")
    else:
        substances = database.get_substances()
        
    logging.info(f"Got {len(substances)} substances from the database.")
    
    # Remove _id field from substances
    for substance in substances:
        substance.pop("_id")
        
    # Sort substances by SMILES
    substances.sort(key=lambda x: x["smiles"])
        
    # Export substances to a file
    path = f"./Exports/substances.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        indent = 4 if FORMAT_EXPORT else None
        json.dump(substances, file, indent=indent)
        
    logging.info(f"Exported {len(substances)} substances to '{path}'.")
    