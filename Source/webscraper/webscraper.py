from bs4 import BeautifulSoup

import caymenchemAPI
from Source.substance import substance

def get_substances_from_caymenchem() -> list[dict]:
    substances = []

    raptas = caymenchemAPI.get_raptas()
    products = caymenchemAPI.get_products()

    for product in products:
        names = []

        names.append(product['exactname'][1])

        for synonym in product.get('synonyms', []):
            names.append(BeautifulSoup(synonym, 'html.parser').get_text())

        categories = []

        # Laden der Kategorien mittels binary-search
        for rapta in product['raptas']:
            rapta_full = get_rapta_from_raptas(raptas = raptas, id = rapta)

            if rapta_full is not None:
                categories.append(rapta_full['text'])

        # Laden der Kategorien mittels linear-search, beides sau langsam
        #for rapta in raptas:
            #if rapta['id'] in product['raptas']:
                #categories.append(rapta['text'])
        
        product_url = 'https://www.caymanchem.com/product/' + product['catalogNum']

        substances.append(substance.get_new_substance(
            smiles = product.get('smiles', None),
            names = names,
            iupac_names = [ product.get('formalNamePlain', None) ],
            chemical_formula = BeautifulSoup(product.get('molecularFormula', ''), 'html.parser').get_text(),
            inchi = product.get('inchi', None),
            inchi_key = product.get('inchiKey', None),
            molecular_mass = product.get('formulaWeight', None),
            cas_number = product.get('casNumber', None),
            categories = categories,
            source_url = product_url,
            source_name = 'Caymanchem'
        ))
    
    return substances

def get_rapta_from_raptas(raptas: list[dict], id: str):
    first = 0
    last = len(raptas) - 1
    mid = 0

    result = None

    while first <= last:
        mid = (first + last) // 2

        if raptas[mid]['id'] < id:
            first = mid + 1
        
        elif raptas[mid]['id'] > id:
            last = mid - 1
        
        else:
            result = raptas[mid]

            break
    
    return result