from Source.Substance import Validator as SubstanceValidator
from Source.Database import MongoDB

def set_substances (substances):
    if SubstanceValidator.SubstancesAreValid(substances) == True:
        for substance in substances:
            set_substance(substance)

    else:
        pass

    return

def set_substance (substance):
    database = MongoDB.Substances()

    searchCriteria = {
        "source": substance["source"],
        "deleted": False
    }

    existingSubstances = database.get_substances(searchCriteria)

    if existingSubstances.__len__() == 0:
        database.insert_substances(substance)
    
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
    database = MongoDB.Substances()

    result = database.get_substances(searchCriteria)

    return result