"""Validates substance schemas and validates or fixes substance properties.
"""

from collections import Counter
import jsonschema
import json
import re
import os


from rdkit import Chem, RDLogger
from rdkit.Chem.rdmolfiles import MolFromSmiles, MolToSmiles
from rdkit.Chem.rdMolDescriptors import CalcExactMolWt


MAX_MASS_ERROR = 0.1

    
def _count_molecules(formula) -> Counter:
    element_pattern = re.compile(r'^([A-Z][a-z]*)(\d*)')
    multiplier_pattern = re.compile(r'^(\d+)')
    
    open_brackets = '({['
    close_brackets = ')}]'
    
    def multiply_counter(counter, multiplier):
        return Counter({element: count * multiplier for element, count in counter.items()})
    
    def parse_group(group):
        counter = Counter()
        i = 0
        while i < len(group):
            if group[i] in open_brackets:
                # Find closing bracket
                open_bracket_count = 1
                for j in range(i + 1, len(group)):
                    if group[j] in open_brackets:
                        open_bracket_count += 1
                    elif group[j] in close_brackets:
                        open_bracket_count -= 1
                        if open_bracket_count == 0:
                            break
                        
                # Parse group
                group_counter = parse_group(group[i + 1:j])
                
                # Apply multiplier if exists
                i = j + 1
                count_match = multiplier_pattern.match(group[i:])
                if count_match:
                    group_counter = multiply_counter(group_counter, int(count_match.group(0)))
                    i += len(count_match.group(0))
                    
                # Add group to counter
                counter += group_counter
            else:
                # Find element
                element_match = element_pattern.match(group[i:])
                if not element_match:
                    raise ValueError('Invalid formula')
                
                element = element_match.group(1)
                count = int(element_match.group(2)) if element_match.group(2) else 1
                counter[element] += count
                i += len(element_match.group(0))
                
        return counter
    
    return parse_group(formula)


def _smiles_equal_molecular_formula(smiles, molecular_formula):
    chem = MolFromSmiles(smiles)
    if chem is None:
        return False
    
    formula = Chem.rdMolDescriptors.CalcMolFormula(chem)
    
    # Count molecules in both
    rdkit_counter = _count_molecules(formula)
    formula_counter = _count_molecules(molecular_formula)
    
    return rdkit_counter == formula_counter
    

def validate_substance(substance):
    validate_substance_schema(substance)
    validate_substance_properties(substance)


substance_schema = None
with open(os.path.join(os.path.dirname(__file__), 'schema.json')) as f:
    substance_schema = json.load(f)
    
def validate_substance_schema(substance):
    global substance_schema        
    jsonschema.validate(substance, substance_schema)


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
      - formula
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
    if abs(molecular_mass - substance['molecular_mass']) > MAX_MASS_ERROR:
        raise ValueError('Molecular mass is not correct')
    
    
    # Compare molecular formula with rdkit
    if not _smiles_equal_molecular_formula(canonical_smiles, substance['formula']):
        raise ValueError('Chemical formula is not correct')


def fix_substance(substance):
    """
    Fixed Properties:
      - version
      - smiles
      - inchi
      - inchi_key
      - molecular_mass
      
    Unfixed Properties:
      - names
      - iupac_names
      - source
      - categories
      - cas_number
      - formula
    """
    
    # Fix smiles
    chem = MolFromSmiles(substance['smiles'])
    if chem is None:
        raise ValueError('Invalid smiles')
    
    # Get canonical smiles
    substance['smiles'] = MolToSmiles(chem, canonical=True)
    
    # Fix inchi and inchi key
    substance['inchi'] = Chem.MolToInchi(chem)
    substance['inchi_key'] = Chem.InchiToInchiKey(substance['inchi'])
    
    # Fix molecular mass
    substance['molecular_mass'] = CalcExactMolWt(chem)
    
    # Fix chemical formula
    formula = Chem.rdMolDescriptors.CalcMolFormula(chem)
    substance['formula'] = formula
    
    return substance


def _setup_rdkit_logger():
    lg = RDLogger.logger()
    lg.setLevel(RDLogger.CRITICAL)
_setup_rdkit_logger()