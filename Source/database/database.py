from datetime import datetime

from Source.database import mongoDB

def set_substances (substances) -> None:
    database = mongoDB.Substances()

    new_substances = []
    changed_substances = []
    deleted_substances = []

    found_substances_urls = []

    for substance in substances:
        existing_substances = database.get_substances(
            searchCriteria = {
                "source": substance['source'],
                "deleted": False
            }
        )

        if existing_substances.__len__() == 0:
            new_substances.append(substance)
        
        else:
            found_substances_urls.append( substance['source']['url'] )

            if existing_substances.__len__() == 1:
                # ToDo: Wann Update?

                pass
            
            else:
                # ToDo: Wass wenn mehrere Ergebnisse?

                pass

    deleted_substances = database.get_substances(
        searchCriteria = {
            "source": {
                # Setzt vorraus das alle Substanzen von derselben Quelle stammen
                "name": substances[0]['source']['name'],
                "url": { "$nin": found_substances_urls }
            },
            "deleted": False
        }
    )

    for deleted_substance in deleted_substances:
        deleted_substance['deleted'] = True
        deleted_substance['last_modified'] = datetime.now().isoformat()

        changed_substances.append(deleted_substance)

    database.insert_substances(new_substances)
    database.update_substances(changed_substances)

    return None

def get_substances (searchCriteria) -> list:
    database = mongoDB.Substances()

    result = database.get_substances(searchCriteria)

    return result