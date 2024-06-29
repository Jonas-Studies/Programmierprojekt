from Source.database import mongoDB

def insert_substances(substances) -> None:
    database = mongoDB.Substances()

    database.insert_substances(substances)

    return None

def update_substances(substances) -> None:
    database = mongoDB.Substances()

    database.update_substances(substances)

    return None

def get_activeSubstances_by_sourceName (sourceName: str) -> list[dict]:
    substances = mongoDB.Substances()

    result = substances.get_substances(
        searchCriteria = {
            "source.name": sourceName,
            "deleted": False
        }
    )

    return result