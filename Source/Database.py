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
    Database = MongoDB.Substances()

    searchCriteria = {
        "source": substance["source"],
        "deleted": False
    }

    existingSubstances = Database.GetSubstances(searchCriteria)

    if existingSubstances.__len__() == 0:
        Database.InsertSubstance(substance)
    
    else:
        if existingSubstances.__len__() == 1:
            existingSubstance = existingSubstances[0]
            
            if existingSubstance["last_modified"] != substance["last_modified"]:
                Database.UpdateSubstanceByID(existingSubstance["_id"], substance)

            else:
                # Wenn last_modified unverändert ist, sollte die Substanz in der Datenbank die erhaltene wie die Übergebene aussehen
                pass

        else:
            pass # ToDo: Was wenn zu einer Quelle + Smiles mehr als ein Datensatz existiert?

    return

def get_substances (searchCriteria) -> list:
    Database = MongoDB.Substances()

    result = Database.GetSubstances(searchCriteria)

    return result