from Source.database import mongoDB

def set_substances (substances):
    for substance in substances:
        set_substance(substance)

    return

def set_substance (substance):
    database = mongoDB.Substances()

    searchCriteria = {
        "source": substance["source"],
        "deleted": False
    }

    existingSubstances = database.get_substances(searchCriteria)

    if existingSubstances.__len__() == 0:
        database.insert_substance(substance)
    
    else:
        if existingSubstances.__len__() == 1:
            existingSubstance = existingSubstances[0]
            
            if existingSubstance["last_modified"] != substance["last_modified"]:
                database.update_substance_by_id(existingSubstance["_id"], substance)

            else:
                # Wenn last_modified unverändert ist, sollte die Substanz in der Datenbank die erhaltene wie die Übergebene aussehen
                pass

        else:
            pass # ToDo: Was wenn zu einer Quelle + Smiles mehr als ein Datensatz existiert?

    return

def get_substances (searchCriteria) -> list:
    database = mongoDB.Substances()

    result = database.get_substances(searchCriteria)

    return result