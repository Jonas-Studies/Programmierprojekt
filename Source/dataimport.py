from Source.webscraper import webscraper
from Source.database import database

def import_data_from_caymanchem() -> None:
    scraped_substances = webscraper.get_substances_from_caymenchem()
    existing_substances = database.get_substances(
        searchCriteria = {
            "source.name":  "Caymanchem",
            "deleted": False
        }
    )

    new_substances = []
    changed_substances = []

    # Eingeschränktes for-statement für tests
    for scraped_substances_index in range(0, 12):
        scraped_substance = scraped_substances[scraped_substances_index]
    
    # For-statement für fertige Anwendung
    # for scraped_substance in scraped_substances:

        existing_substances_index = next((i for i, substance in enumerate(existing_substances) if substance['smiles'] == scraped_substance['smiles']), None)

        if existing_substances_index == None:
            new_substances.append(scraped_substance)
        
        else:
            existing_substance = existing_substances[existing_substances_index]

            if existing_substance['version'] != scraped_substance['version'] or existing_substance['names'] != scraped_substance['names'] or existing_substance['iupac_names'] != scraped_substance['iupac_names'] or existing_substance['formula'] != scraped_substance['formula'] or existing_substance['inchi'] != scraped_substance['inchi'] or existing_substance['inchi_key'] != scraped_substance['inchi_key'] or existing_substance['molecular_mass'] != scraped_substance['molecular_mass'] or existing_substance['cas_num'] != scraped_substance['cas_num'] or existing_substance['categories'] != scraped_substance['categories'] or existing_substance['source']['url'] != scraped_substance['source']['url']:
                changed_substances.append(existing_substance)
            
            existing_substances.pop(existing_substances_index)

    # All substances that were found in the database but not processed by the scraper must be deleted ones
    for remaining_substance in existing_substances:
        remaining_substance['deleted'] = True

        changed_substances.append(remaining_substance)

    if len(new_substances) != 0:
        database.insert_substances(new_substances)
    
    if len(changed_substances) != 0:
        database.update_substances(changed_substances)
    
    return None