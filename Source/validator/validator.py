import json
import jsonschema

from rdkit import Chem
from rdkit.Chem.rdmolfiles import MolFromSmiles, MolToSmiles
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt


def validate_substance(substance):
    validate_substance_schema(substance)
    validate_substance_properties(substance)


def validate_substance_schema(substance):
    with open('schema.json') as f:
        schema = json.load(f)
        
    jsonschema.validate(substance, schema)


def validate_substance_properties(substance):
    """
    Checked Properties:
      - version
      - smiles
      - inchi
      - inchi_key
      - molecular_mass
      
    Unchecked Properties:
      - names
      - iupac_names
      - source
      - categories
      - cas_number
      - chemical_formula
    """
    
    # Check if version is correct
    if substance['version'] != '1.0':
        raise ValueError('Invalid version')
    
    
    # Check if smiles is valid
    chem = MolFromSmiles(substance['smiles'])
    if chem is None:
        raise ValueError('Invalid smiles')
    
    
    # Get canonical smiles from chem and compare with substance['smiles']
    canonical_smiles = MolToSmiles(chem, canonical=True)
    if canonical_smiles != substance['smiles']:
        # raise ValueError('Smiles is not canonical')
        pass
    
    
    # Generate inchi and inchi key and comapre
    inchi = Chem.MolToInchi(chem)
    inchi_key = Chem.InchiToInchiKey(inchi)
    if inchi != substance['inchi']:
        raise ValueError('Inchi is not correct')
    if inchi_key != substance['inchi_key']:
        raise ValueError('Inchi key is not correct')
    
    
    # Get molecular mass and compare with 0.1 precision
    molecular_mass = CalcExactMolWt(chem)
    if abs(molecular_mass - substance['molecular_mass']) > 0.1:
        raise ValueError('Molecular mass is not correct')
    