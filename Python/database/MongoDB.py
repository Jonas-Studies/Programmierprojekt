from pymongo import MongoClient

from settings import MONGODB_HOSTNAME, MONGODB_PORT, DATABASE_NAME


class Substances:
    COLLECTION_NAME = "substances"

    def __init__(self) -> None:
        self.connection = MongoClient(MONGODB_HOSTNAME, MONGODB_PORT)
        self.collection = self.connection[DATABASE_NAME][self.COLLECTION_NAME]

        return None
    
    def __del__(self) -> None:
        self.connection.close()

        return None

    def insert_substances (self, substances: list[dict]) -> None:
        self.collection.insert_many(substances)

        return None

    def update_substances (self, substances: list[dict]) -> None:
        for substance in substances:
            id = substance.get('id', None)

            if id is not None:
                self.update_substance_by_id(substance, id)

        return None
    
    def update_substances_by_smiles (self, substances: list[dict]) -> None:
        for substance in substances:
            smiles = substance.get('smiles', None)

            if smiles is not None:
                self.update_substance_by_smiles(substance, smiles)

        return None
    
    def update_substance_by_id(self, substance: dict, id: str) -> None:
        self.collection.replace_one(
            filter = { "_id": id }, replacement = substance
        )

        return None
    
    def update_substance_by_smiles(self, substance: dict, smiles: str) -> None:
        self.collection.replace_one(
            filter = { "smiles": smiles }, replacement = substance
        )

        return None
    
    def get_substances (self, searchCriteria: dict) -> list[dict]:
        result = []

        substances = self.collection.find(searchCriteria)

        for substance in substances:
            result.append(substance)

        return result
    
    def clear_substances (self) -> None:
        self.collection.delete_many({})

        return None
    