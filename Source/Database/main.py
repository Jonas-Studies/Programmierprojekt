import json

from Source.Substance import Validator as SubstanceValidator
from Source.Database import MongoDB

def SetSubstances (substances):
    if SubstanceValidator.SubstancesAreValid(substances) == True:
        pass
    
    else:
        pass

    return

def GetSubstances (searchCriteria) -> json:
    Database = MongoDB.Substances()

    result = Database.GetSubstances(searchCriteria)

    return result