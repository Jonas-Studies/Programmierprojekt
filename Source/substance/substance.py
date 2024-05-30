from datetime import datetime

def get_new_substance (
        smiles: str,
        names: list[str],
        iupac_names: list[str],
        chemical_formula: str,
        inchi: str,
        inchi_key: str,
        molecular_mass: float,
        cas_number: str,
        categories: list[str],
        source_name: str,
        source_url: str
    ):

    return {
        "version": "1.0",       
        "smiles": smiles,
        "names": names,
        "iupac_names": iupac_names,
        "formula": chemical_formula,
        "inchi": inchi,
        "inchi_key": inchi_key,
        "molecular_mass": molecular_mass,
        "cas_num": cas_number,
        "categories": categories,
        "source": {
            "name": source_name,
            "url": source_url
        },
        "validated": None,
        "deleted": False,
        "last_modified": datetime.now().isoformat(),
        "details": {}
    }