from webscraper.caymanchemAPI import CaymanchemAPI
from database import database
from substance_manager import substance_manager
from validator import validator
from logger import logger
from concurrent.futures import ProcessPoolExecutor

from datetime import datetime
import debugpy


def _validate_substance(substance, fix_substances):
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
        

def import_data_from_caymanchem(fix_substances: bool = False):
    # Get all substances with smiles from Caymanchem
    # Substances with no smiles are ignored because these only contain null values.
    scraped_substances = CaymanchemAPI.get_substances()
    scraped_substances = [substance for substance in scraped_substances if substance['smiles'] is not None]
    
    # When multiple substances have the same smiles, only the first substance is kept.
    unique_substances = { substance['smiles']: substance for substance in reversed(scraped_substances) }
    scraped_substances = list(unique_substances.values())
    

    with ProcessPoolExecutor(max_workers=12) as executor:
        result = list(executor.map(
            _validate_substance,
            scraped_substances,
            [fix_substances] * len(scraped_substances)
        ))
        # Remove invalid substances, start at end to avoid index issues
        for index, valid in zip(range(len(result)-1, -1, -1), reversed(result)):
            if not valid:
                scraped_substances.pop(index)
        
    
    # Create a dictionary of existing substances for easier comparison
    existing_substances = database.get_activeSubstances_by_sourceName("Caymanchem")
    existing_substances = dict((substance['smiles'], substance) for substance in existing_substances)
    
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


if __name__ == "__main__":
    start = datetime.now()
    
    import_data_from_caymanchem(fix_substances=False)
    
    elapsed = datetime.now() - start
    
    print(f"Data import completed, elapsed time: {elapsed}")
    
    pass