from pymongo import MongoClient

MONGODB_HOSTNAME = "localhost"
MONGODB_PORT = 27017

DATABASE_NAME = "designerdrugdatabase"

class Substances:
    COLLECTION_NAME = "substances"

    def __init__(self) -> None:
        self.connection = MongoClient(MONGODB_HOSTNAME, MONGODB_PORT)
        self.collection = self.connection[DATABASE_NAME][self.COLLECTION_NAME]

        return None
    
    def __del__(self) -> None:
        self.connection.close()

        return None

    def insert_substance (self, substance) -> None:
        self.collection.insert_one(substance)

        return None

    def insert_substances (self, substances) -> None:
        self.collection.insert_many(substances)

        return None
    
    def update_substance (self, substance) -> None:
        self.collection.replace_one(
            filter = {
                "_id": substance['_id']
            },
            replacement = substance
        )

        return None

    def update_substances (self, substances) -> None:
        for substance in substances:
            self.update_substance(substance)

        return None
    
    def update_substance_by_id(self, id, substance) -> None:
        searchCriterias = {
            "_id": id
        }

        self.collection.replace_one(searchCriterias, substance)

        return None
    
    def get_substances (self, searchCriteria) -> list[dict]:
        substances = self.collection.find(searchCriteria)

        result = []

        for substance in substances:
            result.append(substance)

        return result