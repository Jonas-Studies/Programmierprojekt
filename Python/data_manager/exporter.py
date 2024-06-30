from database import database

from datetime import datetime
import logging
import json
import os


def export_data(only_from_caymanchem: bool = False):
    if only_from_caymanchem:
        substances = database.get_activeSubstances_by_sourceName("Caymanchem")
    else:
        substances = database.get_substances()
        
    logging.info(f"Got {len(substances)} substances from the database.")
    
    # Remove _id field from substances
    for substance in substances:
        substance.pop("_id")
        
    # Export substances to a file
    path = f"./exports/substances.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(substances, file, indent=4)
        