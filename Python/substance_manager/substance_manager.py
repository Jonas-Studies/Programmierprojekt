from datetime import datetime

def get_new_substance (
        smiles: str,
        names: list[str],
        iupac_names: list[str],
        formula: str,
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
        "formula": formula,
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

def are_substances_equal(substance1, substance2):
    return (
        substance1['version'] == substance2['version'] and
        substance1['smiles'] == substance2['smiles'] and
        substance1['names'] == substance2['names'] and
        substance1['iupac_names'] == substance2['iupac_names'] and
        substance1['formula'] == substance2['formula'] and
        substance1['inchi'] == substance2['inchi'] and
        substance1['inchi_key'] == substance2['inchi_key'] and
        substance1['molecular_mass'] == substance2['molecular_mass'] and
        substance1['cas_num'] == substance2['cas_num'] and
        substance1['categories'] == substance2['categories'] and
        substance1['source']['name'] == substance2['source']['name'] and
        substance1['source']['url'] == substance2['source']['url'] and
        substance1['validated'] == substance2['validated'] and
        substance1['deleted'] == substance2['deleted'] and
        substance1['details'] == substance2['details']
    )
    