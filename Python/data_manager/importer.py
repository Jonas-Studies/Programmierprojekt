from webscraper.caymanchemAPI import CaymanchemAPI
from database import database
from substance_manager import substance_manager
from validator import validator
from concurrent.futures import ProcessPoolExecutor
from logger import logger
from settings import CPU_CORES

from datetime import datetime
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
    logging.info(f"Importing {len(scraped_substances)} substances.")
    
    # Substances with no smiles are ignored because these only contain null values.
    substance_count = len(scraped_substances)
    scraped_substances = [substance for substance in scraped_substances if substance['smiles'] is not None]
    if len(scraped_substances) != substance_count:
        logging.warning(f"Discarded {substance_count - len(scraped_substances)} substances without SMILES.")
    

    # Validate substances
    with ProcessPoolExecutor(max_workers=CPU_CORES) as executor:
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
    
    
    # When multiple substances have the same smiles, only the first substance is kept.
    unique_substances = { substance['smiles']: substance for substance in reversed(scraped_substances) }
    if len(unique_substances) != len(scraped_substances):
        logging.warning(f"Discarded {len(scraped_substances) - len(unique_substances)} substances with duplicate SMILES.")
    scraped_substances = list(unique_substances.values())
        
    
    # Create a dictionary of existing substances for easier comparison
    existing_substances = { substance['smiles']: substance for substance in database.get_substances() }
    logging.info(f"Found {len(existing_substances)} existing substances in the database.")
    
    new_substances = []
    changed_substances = []
    unchanged_substance_smiles = set()
    
    for substance in scraped_substances:
        # Check if the substance is new
        if substance['smiles'] not in existing_substances:
            new_substances.append(substance)
            continue
        
        # Check if the substance has changed
        if not substance_manager.are_substances_equal(substance, existing_substances[substance['smiles']]):
            changed_substances.append(substance)
            continue
        
        # Add the substance to the deleted substances if it is from Caymanchem
        unchanged_substance_smiles.add(substance['smiles'])
    
    # Gather all substances that have been deleted from Caymanchem
    deleted_substances = [substance 
                          for substance in existing_substances.values() 
                          if substance['source']['name'] == "Caymanchem" and 
                             substance['smiles'] not in unchanged_substance_smiles]

    # Insert, update and delete substances
    if len(new_substances) != 0:
        start_time = datetime.now()
        database.insert_substances(new_substances)
        end_time = datetime.now()
        logging.info(f"Inserted new substances in {end_time - start_time} seconds.")

    if len(changed_substances) != 0:
        start_time = datetime.now()
        database.update_substances(changed_substances)
        end_time = datetime.now()
        logging.info(f"Updated changed substances in {end_time - start_time} seconds.")

    if len(deleted_substances) != 0:
        start_time = datetime.now()
        for substance in deleted_substances:
            substance['deleted'] = True
        database.update_substances(deleted_substances)
        end_time = datetime.now()
        logging.info(f"Marked substances as deleted and updated in {end_time - start_time} seconds.")
        
    logging.info(f"Inserted {len(new_substances)}, updated {len(changed_substances)} and deleted {len(deleted_substances)} substances.")
