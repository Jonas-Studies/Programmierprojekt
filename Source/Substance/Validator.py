import json
import jsonschema

def SubstancesAreValid (substances_to_validate) -> bool:
    result = False

    with open("C:\\Users\\Studies\\Programmierprojekt\\Source\\Substance\\Schema.json", "r") as schema_file:
        schema = json.load(schema_file)

        try:
            jsonschema.validate(instance = substances_to_validate, schema = schema)
            
            result = True
        
        except:
            pass # ToDo: Fehlerbehandlung

    return result