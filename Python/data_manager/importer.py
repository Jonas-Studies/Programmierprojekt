from webscraper.caymanchemAPI import CaymanchemAPI
from database import database
from substance_manager import substance_manager
from validator import validator
from concurrent.futures import ProcessPoolExecutor
from logger import logger

import logging
import json


def _validate_substance(substance, fix_substances) -> bool:
    """Sets the 'validated' key of the substance to True if the substance is valid, False otherwise.
    If fix_substances is True, the substance is fixed if possible.
    
    If the substance has an invalid schema, the function returns False.

    Returns:
        bool: Schema validation success
    """
    try:
        validator.validate_substance_schema(substance)
    except Exception as e:
        return False
    
    try:
        if fix_substances:
            validator.fix_substance(substance)
        else:
            validator.validate_substance_properties(substance)
            
        substance['validated'] = True
    except ValueError as e:
        substance['validated'] = False
    
    return True


def import_data_from_file(path: str, fix_substances: bool = False):
    with open(path, 'r') as file:
        substances = json.load(file)
    if not isinstance(substances, list):
        raise ValueError(f"The file '{path}' does not contain a list of substances.")
    
    logging.info(f"Read {len(substances)} substances from '{path}'.")
    
    import_data(substances, fix_substances)
    

def import_data_from_caymanchem(fix_substances: bool = False):
    # Get all substances with smiles from Caymanchem
    substances = CaymanchemAPI.get_substances()
    logging.info(f"Scraped {len(substances)} substances from Caymanchem API.")
    import_data(substances, fix_substances)
    
    
def import_data(scraped_substances: list[dict], fix_substances: bool = False):
    """Imports substances into the database.
    """
    
    # Substances with no smiles are ignored because these only contain null values.
    substance_count = len(scraped_substances)
    scraped_substances = [substance for substance in scraped_substances if substance['smiles'] is not None]
    if len(scraped_substances) != substance_count:
        logging.warning(f"Discarded {substance_count - len(scraped_substances)} substances without SMILES.")
    
    # When multiple substances have the same smiles, only the first substance is kept.
    unique_substances = { substance['smiles']: substance for substance in reversed(scraped_substances) }
    if len(unique_substances) != len(scraped_substances):
        logging.warning(f"Discarded {len(scraped_substances) - len(unique_substances)} substances with duplicate SMILES.")
    scraped_substances = list(unique_substances.values())
    

    with ProcessPoolExecutor() as executor:
        result = list(executor.map(
            _validate_substance,
            scraped_substances,
            [fix_substances] * len(scraped_substances)
        ))
        # Remove invalid substances, start at end to avoid index issues
        for index, valid in zip(range(len(result)-1, -1, -1), reversed(result)):
            if not valid:
                scraped_substances.pop(index)
        if len(result) == len(scraped_substances):
            logging.info(f"Validated {len(scraped_substances)} substances.")
        else:
            logging.warning(f"Discarded {len(result) - len(scraped_substances)} substances with invalid format. Remaining: {len(scraped_substances)}.")
        
    
    # Create a dictionary of existing substances for easier comparison
    existing_substances = database.get_substances_by_sourceName("Caymanchem")
    existing_substances = dict((substance['smiles'], substance) for substance in existing_substances)
    logging.info(f"Found {len(existing_substances)} existing substances in the database.")
    
    new_substances = []
    changed_substances = []
    
    for substance in scraped_substances:
        # Check if the substance is new
        if substance['smiles'] not in existing_substances:
            new_substances.append(substance)
            continue
        
        # Check if the substance has changed
        if not substance_manager.are_substances_equal(substance, existing_substances[substance['smiles']]):
            changed_substances.append(substance)
        
        # Remove the substance from the dictionary
        existing_substances.pop(substance['smiles'])
    
    # Gather all remaining substances in the dictionary
    deleted_substances = list(existing_substances.values())

    # Insert, update and delete substances
    if len(new_substances) != 0:
        database.insert_substances(new_substances)
    if len(changed_substances) != 0:
        database.update_substances(changed_substances)
    if len(deleted_substances) != 0:
        for substance in deleted_substances:
            substance['deleted'] = True
        database.update_substances(deleted_substances)
        
    logging.info(f"Inserted {len(new_substances)}, updated {len(changed_substances)} and deleted {len(deleted_substances)} substances.")
