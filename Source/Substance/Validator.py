import json
import jsonschema

import os

def SubstancesAreValid (substances_to_validate) -> bool:
    result = False

    schema_path = os.path.dirname(__file__)

    with open(schema_path + "\\Schema.json", "r") as schema_file:
        schema = json.load(schema_file)

        try:
            jsonschema.validate(instance = substances_to_validate, schema = schema)
            
            result = True
        
        except:
            pass # ToDo: Fehlerbehandlung

    return result