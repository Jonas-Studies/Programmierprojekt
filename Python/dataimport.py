from webscraper.caymanchemAPI import CaymanchemAPI
from database import database
from substance_manager import substance_manager
from validator import validator
from logger import logger
from concurrent.futures import ThreadPoolExecutor
import functools


def import_data_from_caymanchem(fix_substances: bool = False):
    # Get all substances with smiles from Caymanchem
    # Substances with no smiles are ignored because these only contain null values.
    scraped_substances = CaymanchemAPI.get_substances()
    scraped_substances = [substance for substance in scraped_substances if substance['smiles'] is not None]
    
    def _validate_substance_schema(s):
        try:
            validator.validate_substance_schema(s)
        except Exception as e:
            print(f"Schema validation failed on substance {s['smiles']}")
            scraped_substances.remove(s)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(_validate_substance_schema, scraped_substances)
        
    for substance in scraped_substances:
        try:
            if fix_substances:
                validator.fix_substance(substance)
            else:
                validator.validate_substance_properties(substance)
                
            substance['validated'] = True
        except ValueError as e:
            substance['validated'] = False
    
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
    import_data_from_caymanchem(fix_substances=True)
    
    print("Data import completed")
    
    substances = database.get_activeSubstances_by_sourceName("Caymanchem")
    pass