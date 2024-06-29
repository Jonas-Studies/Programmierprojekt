from .Webscraper.caymanchemAPI import CaymanchemAPI
from .Database import database
from .substance_manager import substance_manager
from .Validator import validator


def import_data_from_caymanchem(fix_substances: bool = False):
    scraped_substances = CaymanchemAPI.get_substances()
    
    if fix_substances:
        for substance in scraped_substances:
            validator.fix_substance(substance)
    
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
        