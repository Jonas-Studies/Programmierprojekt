import os
import re
import json
import requests
from concurrent.futures import ThreadPoolExecutor

from Substance.substance import get_new_substance

class CaymanchemAPI:
    tags = set()
    
    def _clean_formatted_text(text: str) -> str:
        # Remove html tags with regex
        text = re.sub(r'<[^>]*>', '', text)
    
    def _clean_url(url: str) -> str:
        return url.replace('\n', '')
    
    def get_caymanchem_substances() -> list[dict]:
        # Read url from ./fetch_substances_url.txt
        with open(os.path.join(os.path.dirname(__file__), './fetch_substances_url.txt')) as f:
            url = CaymanchemAPI._clean_url(f.read())
            
        # Get substances from Caymanchem and parse json result
        response = requests.request("GET", url)
        if response.status_code == 200:
            response = json.loads(response.text)
            substances = response['response']['docs']
        else:
            substances = []
            
        return substances
    
    def get_caymanchem_raptas() -> list[dict]:
        # Read url from ./fetch_raptas_url.txt
        with open(os.path.join(os.path.dirname(__file__), './fetch_raptas_url.txt')) as f:
            url = CaymanchemAPI._clean_url(f.read())
            
        # Get raptas from Caymanchem and parse json result
        response = requests.request("GET", url)
        if response.status_code == 200:
            response = json.loads(response.text)
            raptas = response['response']['docs']
        else:
            raptas = []
            
        return raptas
    
    def get_substances() -> list[dict]:
        # Get substances and raptas from Caymanchem
        with ThreadPoolExecutor(max_workers=2) as executor:
            substances_future = executor.submit(CaymanchemAPI.get_caymanchem_substances)
            raptas_future = executor.submit(CaymanchemAPI.get_caymanchem_raptas)

        # Parse substances and raptas
        raptas = raptas_future.result()
        raptas = {rapta['id']: rapta for rapta in raptas}
        
        substances = substances_future.result()
        
        substances = [
            get_new_substance(
                smiles= substance.get('smiles', None),
                names= [CaymanchemAPI._clean_formatted_text(name) for name in substance['exactname'][1:] + substance.get('synonyms', [])],
                iupac_names= [substance.get('formalNamePlain', None)],
                chemical_formula= CaymanchemAPI._clean_formatted_text(substance.get('molecularFormula', '')),
                inchi= substance.get('inchi', None),
                inchi_key= substance.get('inchiKey', None),
                molecular_mass= substance.get('formulaWeight', None),
                cas_number= substance.get('casNumber', None),
                categories= [raptas[rapta_id]['text'] for rapta_id in substance['raptas'] if rapta_id in raptas],
                source_url= 'https://www.caymanchem.com/product/' + substance['catalogNum'],
                source_name= 'Caymanchem',
            )
            for substance in substances
        ]
        
        return substances
    