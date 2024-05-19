import json

from Source.Substance import Validator as SubstanceValidator

def SetSubstances (substances):
    if SubstanceValidator.SubstancesAreValid(substances) == True:
        pass
    
    else:
        pass

    return

def GetSubstances (searchCriteria) -> json:
    return