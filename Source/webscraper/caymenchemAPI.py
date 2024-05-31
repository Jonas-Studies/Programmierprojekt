import aiohttp
from datetime import datetime
import json
from bs4 import BeautifulSoup
import requests

class Rapta:
    def __init__(self, id: str, parent_id: str, root_id: str, text: str):
        self.id = id
        self.parent_id = parent_id
        self.root_id = root_id
        self.text = text
        

class Chemical:
    def __init__(self, smiles: str,
                 names: list[str],
                 iupac_names: list[str],
                 chemical_formula: str,
                 inchi: str, inchikey: str,
                 molecular_mass: float,
                 cas_number: str | None,
                 raptas: list[Rapta],
                 source_url: str,
                 source_name: str,
                 deleted: bool,
                 last_modified: datetime):
        
        self.smiles = smiles
        self.names = names
        self.iupac_names = iupac_names
        self.chemical_formula = chemical_formula
        self.inchi = inchi
        self.inchikey = inchikey
        self.molecular_mass = molecular_mass
        self.cas_number = cas_number
        self.raptas = raptas
        self.source_url = source_url
        self.source_name = source_name
        self.deleted = deleted
        self.last_modified = last_modified
        
    def to_json_obj(self):
        return {
            "version": "1.0",       
            "smiles": self.smiles,  # SMILES wird im validator zu kanonischer Form gebracht
            "names": self.names,
            "iupac_names": self.iupac_names,
            "formula": self.chemical_formula,
            "inchi": self.inchi,
            "inchi_key": self.inchikey,
            "molecular_mass": self.molecular_mass,
            "cas_num": self.cas_number,
            "categories": [rapta.text for rapta in self.raptas],
            "source": {
                "name": self.source_name,
                "url": self.source_url
            },
            "validated": None,  # Noch nicht validiert
            "deleted": self.deleted,
            "last_modified": self.last_modified.isoformat(),
            "details": {}  # Bisher keine Details
        }


class CaymanChemAPI:
    def __init__(self):
        self.client = aiohttp.ClientSession()
        
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.client.close()
        
    async def close(self):
        await self.client.close()
        
    
    async def _fetch_raptas(self):
        url = r'https://www.caymanchem.com/solr/cchRAPTA/select?q=*:*&rows=999999&wt=json'
        
        async with self.client.get(url) as response:
            result = json.loads(await response.text())
            
        raptas = []
        for doc in result['response']['docs']:
            raptas.append(Rapta(doc['id'], doc['parent'], doc['rootId'], doc['text']))
        return raptas
    
    
    async def _fetch_chemicals(self):
        # Read url from fetch_chemicals_url.txt
        with open('./src/caymanchemapi/fetch_chemicals_url.txt') as f:
            url = f.read()
        
        raptas = { rapta.id: rapta for rapta in await self._fetch_raptas() }
        
        async with self.client.get(url) as response:
            result = json.loads(await response.text())
            
        chemicals = []
        for doc in result['response']['docs']:
            chem_raptas = [raptas[rapta_id] for rapta_id in doc['raptas'] if rapta_id in raptas]
            
            names = doc['exactname'][1:] + doc.get('synonyms', [])
            
            print(len(chemicals))
            chemicals.append(Chemical(smiles=doc.get('smiles', None),
                                      names=names,
                                      iupac_names=[doc.get('formalNamePlain', None)],
                                      chemical_formula=BeautifulSoup(doc.get('molecularFormula', ''), 'html.parser').get_text(),
                                      inchi=doc.get('inchi', None),
                                      inchikey=doc.get('inchiKey', None),
                                      molecular_mass=doc.get('formulaWeight', None),
                                      cas_number=doc.get('casNumber', None),
                                      raptas=chem_raptas,
                                      source_url="",
                                      source_name="Caymanchem",
                                      deleted=False,
                                      last_modified=datetime.now()))
        return chemicals

def get_raptas() -> list[dict]:
    URL = 'https://www.caymanchem.com/solr/cchRAPTA/select?q=*:*&rows=999999&wt=json'

    raptas = []

    response = requests.request("GET", URL)

    if response.status_code == 200:
        response = json.loads(response.text)

        raptas = response['response']['docs']

    return raptas

def get_products() -> list[dict]:
    with open('./src/caymanchemapi/fetch_chemicals_url.txt') as f:
        URL = f.read()

    products = []

    response = requests.request("GET", URL)

    if response.status_code == 200:
        response = json.loads(response.text)

        products = response['response']['docs']

    return products