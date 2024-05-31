from Source.database import mongoDB

def set_substances (substances) -> None:
    database = mongoDB.Substances()

    new_substances = []
    changed_substances = []

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
            changed_substances.append(substance)

    database.insert_substances(new_substances)
    database.update_substances(changed_substances)

    return None

def insert_substances(substances) -> None:
    database = mongoDB.Substances()

    database.insert_substances(substances)

    return None

def update_substances(substances) -> None:
    database = mongoDB.Substances()

    database.update_substances(substances)

    return None

def get_substances (searchCriteria) -> list:
    database = mongoDB.Substances()

    result = database.get_substances(searchCriteria)

    return result